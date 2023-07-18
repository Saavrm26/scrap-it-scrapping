import scrapy
from scrapping.utils.color_printing import prYellow, prRed, prGreen
from scrapping.itemloaders.naukri import JobLoader
from scrapping.utils.types import JOB_TITLE, COMPANY_NAME, COMPANY_ABOUT_URL, SALARY, LOCATION, JOB_URL

meta = {
    "playwright": True
}


class NaukriSpider(scrapy.Spider):
    # * THOUGHT: COMPRESS AND STORE JOB DESCRIPTION IN AN ELASTIC SEARCH DATABASE, THIS WILL ELIMINATE THE NEED OF SCRAPING BENEFITS, JOB_TYPE
    name = "naukri"

    def __init__(self, title: str, location: str, *args, **kwargs):
        super(NaukriSpider, self).__init__(*args, **kwargs)
        self.title = title
        self.location = location
        self.url = f"https://www.naukri.com/{title.replace(' ','-')}-jobs-in-{location}"

    def start_requests(self):
        try:
            prYellow("Inside Naurkri spider start_requests")
            yield scrapy.Request(self.url, callback=self.parse_job_cards, meta=meta)
        except Exception as e:
            prRed(e)
            prRed("At Naurkri spider start_requests")

    def parse_job_cards(self, response):
        try:
            prYellow("Inside Naukri Spider's parse_job_cards")
            job_cards_list = response.css(".jobTuple")
            # For testing, limited results to 1
            for job_card in job_cards_list[0:1]:
                job_url = job_card.css('a.title::attr(href)').get()
                # prGreen(job_url)
                yield response.follow(job_url, callback=self.parse_job_page, meta=meta)

        except Exception as e:
            prRed(e)
            prYellow("At Naukri Spider's parse_job_cards")

    def parse_job_page(self, response):
        try:
            prYellow("Inside Naukri Spider parse_job_page")
            prGreen(response.url)
            jd_body = response.css(".jd-container .leftSec")
            scrapped_items = {}

            scrapped_items[JOB_TITLE] = jd_body.css(
                ".jd-header-title::text").get()

            scrapped_items[JOB_URL] = response.url

            scrapped_items[COMPANY_NAME] = jd_body.css(
                "div.jd-header-comp-name a::text").get()

            scrapped_items[COMPANY_ABOUT_URL] = jd_body.css(
                "div.jd-header-comp-name a::attr(href)").get()

            scrapped_items[SALARY] = jd_body.css(".salary span::text").get()

            scrapped_items[LOCATION] = jd_body.css(
                ".loc .location a::text").get()

            prGreen(scrapped_items)

            yield JobLoader(scrapped_items).load_item()()

        except Exception as e:
            prRed(e)
            prYellow("At Naukri Spider parse_job_page")
