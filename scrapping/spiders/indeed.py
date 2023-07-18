import scrapy

from scrapping.itemloaders.indeed import JobLoader

from scrapping.utils.color_printing import prRed, prYellow

from scrapping.utils.types import JOB_TITLE, JOB_URL, LOCATION, COMPANY_ABOUT_URL, COMPANY_NAME

meta = {
    "playwright": True
}


class IndeedSpider(scrapy.Spider):
    # TODO: Use Scrapper API to implement proxy
    # TODO: Create an pipeline for compression
    name = "indeed"

    def __init__(self, title: str, location: str, *args, **kwargs):
        super(IndeedSpider, self).__init__(*args, **kwargs)
        self.title = title
        self.location = location
        self.url = f"https://in.indeed.com/jobs?q={title.replace(' ', '+')}&l={location}"

    def start_requests(self):
        try:
            prYellow("Inside Indeed Spider's start_requests")
            yield scrapy.Request(self.url, callback=self.parse_job_cards, meta=meta)
        except Exception as e:
            prRed(e)
            prRed("At Indeed Spider's start_requests")

    def parse_job_cards(self, response):
        try:
            prYellow("Inside Indeed Spider's parse_job_cards")
            job_cards_list = response.css(
                ".jobsearch-ResultsList").css(".cardOutline")
            # For testing, limited results to 1
            for job_card in job_cards_list[0:1]:

                jk = job_card.css('a::attr(data-jk)').get()
                job_url = f"https://in.indeed.com/viewjob?jk={jk}"

                yield response.follow(job_url, callback=self.parse_job_page, meta=meta)

        except Exception as e:
            prRed(e)
            prYellow("At Indeed Spider's parse_job_cards")

    def parse_job_page(self, response):
        try:
            prYellow("Inside parse_job_page")
            scrapped_items = {}

            scrapped_items[JOB_TITLE] = response.css(
                'h1.jobsearch-JobInfoHeader-title span::text').get()

            scrapped_items[JOB_URL] = response.url

            scrapped_items[LOCATION] = response.css(
                'div[data-testid="inlineHeader-companyLocation"] div::text').get()

            scrapped_items[COMPANY_NAME] = response.css(
                'div[data-testid="inlineHeader-companyName"] a::text').get()

            scrapped_items[COMPANY_ABOUT_URL] = response.css(
                'div[data-testid="inlineHeader-companyName"] a::attr(href)').get()

            scrapped_items["job_details_html"] = response.css(
                '#jobDetailsSection').get()

            yield JobLoader(scrapped_items).load_item()()

        except Exception as e:
            prRed(e)
            prYellow("At parse_job_page")
            yield None
