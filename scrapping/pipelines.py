import json
import time
import re
from itemadapter import ItemAdapter
from scrapping.utils.color_printing import prPurple
from scrapping.utils.types import STRING_FIELDS, LIST_FIELDS, SALARY

salary_parser = re.compile(r'\d+\.?\d*')


class JobPipeline:
    # writing to jsonl is only temporary
    def open_spider(self, spider):
        prPurple("Writing to jsonl")
        self.file = open(f"./results/{time.ctime()}.jsonl", "w")

    def close_spider(self, spider):
        prPurple("Closing")
        self.file.close()

    def extract_numbers(self, string):
        return salary_parser.findall(string)

    def process_item(self, item, spider):
        # TODO: Store results in redis
        prPurple("Processing Item")

        unsanitized_job_details = ItemAdapter(item).asdict()
        santized_job_details = {}

        for k in STRING_FIELDS:
            v = unsanitized_job_details[k].pop()
            if not v:
                continue
            santized_job_details[k] = v

        for k in LIST_FIELDS:
            if not unsanitized_job_details[k][0]:
                continue
            v = unsanitized_job_details[k]
            santized_job_details[k] = v

            if k == SALARY:
                v = v[0]
                v = v.replace(',', '')
                unit = 'month'
                if v.find('year') != -1:
                    unit = 'year'
                salary_range = self.extract_numbers(v)
                santized_job_details[k] = {
                    "salary_range": salary_range,
                    "unit": unit
                }

        line = json.dumps(santized_job_details) + "\n"
        self.file.write(line)
        return item
