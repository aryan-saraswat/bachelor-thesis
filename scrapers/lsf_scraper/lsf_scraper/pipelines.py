# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LsfPipeline:
    # def process_item(self, item, spider):
    #     # remove unwanted symbols
    #     if len(item['name'].split('\n')) >= 2:
    #         item['name'] = str(item['name']).split('\n')[1].strip(' ')
    #     return item

    def process_item(self, item, spider):
        if 'type' in item.keys() and item['type'] == 'Einzeltermine':
            einzeltermine = item['einzeltermine']
            einzeltermine_new = []
            for termin in einzeltermine:
                termin = termin.replace('<li>', '').replace('</li>', '').replace('\\n', '').replace('\\t', '').strip()
                einzeltermine_new.append(termin)
            item['einzeltermine'] = einzeltermine_new
            return item
        else:
            return item