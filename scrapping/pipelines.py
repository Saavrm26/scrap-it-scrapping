import json
import time
import re
import os
from itemadapter import ItemAdapter
from scrapping.utils.color_printing import prPurple, prYellow
from scrapping.utils.types import STRING_FIELDS, LIST_FIELDS, SALARY
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import datetime

uri = os.environ.get("MONGODB_ATLAS_DB")
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["scrapit"]
jobs = db["jobs"]

salary_parser = re.compile(r"\d+\.?\d*")


class JobPipeline:
    # writing to jsonl is only temporary
    def open_spider(self, spider):
        prPurple("Starting")

    def close_spider(self, spider):
        prPurple("Closing")

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
                v = v.replace(",", "")
                unit = "month"
                if v.find("year") != -1:
                    unit = "year"
                salary_range = self.extract_numbers(v)
                santized_job_details[k] = {"salary_range": salary_range, "unit": unit}

        # line = json.dumps(santized_job_details) + "\n"
        # self.file.write(line)
        # return item
        santized_job_details['createdAt'] = datetime.datetime.now(tz=datetime.timezone.utc)
        id = jobs.insert_one(santized_job_details).inserted_id
        prYellow(f"inserted {id}")
