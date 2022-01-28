from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

page_url = 'https://www.uni-due.de/vdb/en_EN/studiengang/liste'

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

studyProgramContainers = page_soup.findAll("div", {"class": "highlight-blue"})
# name the output file to write to local disk
out_filename = "Courses_data.csv"
# header of csv file to be written
headers = "Study Program,Courses,Description\n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

studyProgramContainer = studyProgramContainers[0]
courseKeywords = ['applied cognitive and media science', 'applied computer sience', 'computer engineering']
for studyProgram in studyProgramContainer.select("a"):
    for courseKeyword in courseKeywords:
        if(str(courseKeyword) in str(studyProgram.text.lower())):
            page_url = 'https://www.uni-due.de' + studyProgram['href']

            # opens the connection and downloads html page from url
            uClient = uReq(page_url)

            # parses html into a soup data structure to traverse html
            # as if it were a json data type.
            page_soup = soup(uClient.read(), "html.parser")
            uClient.close()

            # finds each product from the store page
            containers = page_soup.findAll("fieldset", {"class": "highlight-yellow"})
            for container in containers:
                for courses in container.select("a"):
                    course = courses.text
                    if(courses.text.find("Dr.") != -1 or courses.text.find("M.Sc.") != -1 or courses.text.find("Prof.") != -1 ):
                        continue
                    else:
                        print('study program: ', studyProgram.text, ' , lecture: ', course)
                        page_url = 'https://www.uni-due.de' + courses['href']
                        uClient = uReq(page_url)
                        page_soup = soup(uClient.read(), "html.parser")
                        uClient.close()
                        coursesContainers= page_soup.findAll("div", {"class": "highlight-blue"})
                        coursesContainer = coursesContainers[1].findAll("td")
                        description = coursesContainer[1].text
                        if(description != ""):
                            f.write(studyProgram.text.replace(",", " ") +"," +course.replace(",", " ") +","+ description.replace(",", " ").replace('\n', ' ')  +"\n")
        else:
            continue


f.close()  # Close the file
