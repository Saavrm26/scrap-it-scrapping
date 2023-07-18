from typing import Any
from scrapy.loader import ItemLoader
from scrapping.items.Job import Job


class JobLoader:
    def add_values(self, dictionary: dict[str, Any]):
        for key, value in dictionary.items():
            if not value:
                continue

            if type(value) is list:
                value = tuple(value)

            if type(value) is str:
                value = value.strip()

            key = '_'.join(key.split(' '))

            self.Loader.replace_value(key, value)

    def load_item(self) -> ItemLoader.load_item:
        return self.Loader.load_item

    def __init__(self, scrapped_items: dict[str, Any]):
        self.Loader = ItemLoader(item=Job())
        self.add_values(scrapped_items)
