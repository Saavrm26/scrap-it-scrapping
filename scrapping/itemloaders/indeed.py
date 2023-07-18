from typing import Any
from scrapy.loader import ItemLoader
from scrapping.items.Job import Job
from scrapping.utils.types import SALARY, JOB_TYPE, SHIFT_AND_SCHEDULE, BENEFITS_AND_PERKS, COMPANY_ABOUT_URL
import html2text


def extract_job_details(job_details_section: str) -> dict[str, Any]:
    html_converter = html2text.HTML2Text()
    html_converter.ignore_links = True

    job_details_text = html_converter.handle(job_details_section)

    lines = job_details_text.split('\n')
    keys = [SALARY, JOB_TYPE,
            SHIFT_AND_SCHEDULE, BENEFITS_AND_PERKS]
    job_details = {}
    for key in keys:
        job_details[key] = ['']
    current_key = None

    for line in lines:
        if not line:
            continue
        line = line.lower()
        for key in keys:
            if key in line:
                current_key = key
                job_details[current_key] = []
                break

        if current_key:
            if line.strip().lower() != current_key:
                job_details[current_key].append(line.strip())
            else:
                job_details[current_key] = []

    return job_details


class JobLoader:
    def add_values(self, dictionary: dict[str, Any]):
        for key, value in dictionary.items():
            if not value:
                continue

            if key == "job_details_html":
                job_details = extract_job_details(dictionary[key])
                self.add_values(job_details)
                continue

            if key == COMPANY_ABOUT_URL:
                value = value.split('?')[0]

            if type(value) is list:
                value = tuple(value)

            if type(value) is str:
                value = value.strip()

            if key == "benefits & perks":
                key = 'and'.split(key.split('&'))

            key = '_'.join(key.split(' '))

            self.Loader.replace_value(key, value)

    def load_item(self) -> ItemLoader.load_item:
        return self.Loader.load_item

    def __init__(self, scrapped_items: dict[str, Any]):
        self.Loader = ItemLoader(item=Job())
        self.add_values(scrapped_items)

