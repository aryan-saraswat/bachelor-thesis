import scrapy
from ..items import Person, CourseCatalogItem, Category, Subject, TimeEntry, StudyProgram

class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["campus.uni-due.de"]
    start_urls = [
        'https://campus.uni-due.de/lsf/rds?state=wtree&search=1&trex=step&root120212=288350%7C292081%7C290850&P.vx=kurz'
    ]

    def parse(self, response):
        return self.extract_faculties(response)

    # def extract_faculties(self, response, current_directory = []):
    #     links = response.xpath("//a")
    #     try:
    #         layer = response.meta["layer"]
    #     except Exception:
    #         layer = 3
    #
    #
    #     current_directory = current_directory
    #
    #     filtered_links = self.filter_links_by_layer(links, "%7C", layer) # links that lead to the next level in the course tree -> could be lectures or sections of study courses
    #     filtered_lectures = self.filter_links_by_subjects(links) # each level in the course tree could contain lectures or links to further levels, this returns the lectures)
    #
    #     for link in filtered_links:
    #         current_branch = str(link.xpath("text()").get()).strip()
    #         current_link = str(link.xpath("@href").get())
    #         # print('study course:', current_branch, current_link)
    #         # print(layer)
    #         # print(current_directory)
    #         request = scrapy.Request(current_link, callback=self.extract_faculties)
    #         request.meta["layer"] = layer + 1
    #         print(current_branch)
    #         request.cb_kwargs["current_directory"] = current_directory
    #         yield Category(id=1, parent_id=1, url=current_link, name=current_branch)
    #         yield request

    def extract_faculties(self, response):
        # width = 60
        links = response.xpath('//a')
        filtered_links = self.filter_links_by_layer(links, "%7C", 2)
        for link in filtered_links:
            page = response.urljoin(link.attrib['href'])
            request = scrapy.Request(page, callback=self.extract_studyprograms)
            request.meta['faculty'] = link
            yield request

    def extract_studyprograms(self, response):
        link = response.meta['faculty'].attrib['href']
        number_of_layers = link.count('%7C')
        studyprograms = []

        links = response.xpath('//a')
        studyprograms_element = self.filter_links_by_layer(links, "%7C", number_of_layers + 1)

        # extrahiere informations for every strudyprogram
        for studyprogram in studyprograms_element:
            name = str(studyprogram.css('::text').get()).strip()
            self.log("extracting " + str(name))
            link = studyprogram.attrib['href']

            type = name
            # if "master " in name.lower():
            #     type = "Master"
            # elif "bachelor " in name.lower():
            #     type = "Bachelor"
            # else:
            #     type = "not empty"

            if type != "":
                program = StudyProgram(url=link, name=name, program_type=type, categories=[])
                program['id'] = self.extract_category_id(link)
                program['parent_id'] = None
                page = response.urljoin(link)
                request = scrapy.Request(page, callback=self.extract_studyprogram_content)
                request.meta['parent'] = program
                yield request
            else:
                self.log("No type for: "+name)
                page = response.urljoin(link)
                request = scrapy.Request(page, callback=self.extract_studyprograms)
                request.meta['faculty'] = studyprogram
                yield request

    def filter_links_by_layer(self, links, symbol, count):
        filtered_links = []
        link_elements_without_href = []
        for link in links:
            try:
                href = str(link.attrib['href'])
                if (href.count(symbol) >= count and href.endswith("&P.vx=kurz")):
                    filtered_links.append(link)
            except:
                # self.log('excluded link with no href')
                # do nothing
                link_elements_without_href.append(link)

        # self.log("links without href: " +str(len(link_elements_without_href)))
        return filtered_links

    def filter_links_by_subjects(self, link_elements):
        filtered_links = []
        link_elements_without_href = []
        for link in link_elements:
            try:
                href = str(link.attrib['href'])
                if(href.find("publishSubDir=veranstaltung")>0):
                    filtered_links.append(link)
            except:
                #self.log('excluded link with no href')
                link_elements_without_href.append(link)
                # do nothing

        return filtered_links

    def extract_categories(self, response):
        number = response.meta["number"]
        print("from function extract_faculties: attribute meta-number:", number)