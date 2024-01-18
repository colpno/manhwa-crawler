import os
import scrapy
import base64
from fake_useragent import FakeUserAgent
from project.helpers.get_proxy import get_proxy
from project.helpers.function import extract_file_from_url, extract_filename_from_url
from project.items import Manhwa


class ManhwaSpider(scrapy.Spider):
    name = 'manhwa'
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'FEEDS': {
            'data/manhwa.json': {
                'format': 'json',
                'overwrite': True
            },
        },
    }

    def __init__(self, *args, **kwargs):
        self.ua = FakeUserAgent().random
        self.proxy = get_proxy()
        self.start_urls = [kwargs.get('start_url') or 'https://acomics.net/']

    def start_requests(self):
        callback = self.enter_novel_page if 'https://acomics.net/' in self.start_urls else self.parse

        yield scrapy.Request(
            url=self.start_urls[0],
            callback=callback,
            headers={
                "User-Agent": self.ua,
                'Referer': 'https://www.google.com/',
                'proxy': self.proxy
            }
        )

    def enter_novel_page(self, response):
        items = response.xpath(
            '//div[@class="list_wrap"]/ul[@class="slick_item"]/li/div[@class="item"]')

        for item in items:
            novel_link = item.xpath(
                './/div[@class="novel-cover"]/a/@href').get()

            yield response.follow(
                novel_link,
                callback=self.parse,
            )

    def parse(self, response):
        content_box = response.xpath(
            '//div[@class="title_content_box"]/div[@class="title_content"]')

        category_list = content_box.xpath('.//div[@class="categories"]/ul/li')
        categories = []
        is_forbidden = False
        for item in category_list:
            category = item.xpath(
                './a/text()').get().replace("\n", "").rstrip().replace("..", ".")
            if self.is_forbidden_category(category):
                is_forbidden = True
                break
            categories.append(category)
        if is_forbidden:
            return

        title = content_box.xpath(
            './div[@class="main-head"]/h1/text()').get().replace("\n", "").rstrip().replace("..", ".")

        about = content_box.xpath(
            'string(//div[@class="about"])').get().replace("\n", "").rstrip().replace("..", ".")

        manhwa = Manhwa()
        manhwa['title'] = title
        manhwa['about'] = about
        manhwa['categories'] = categories

        current_url = response.request.url
        image_folder = extract_filename_from_url(
            current_url) or extract_file_from_url(current_url)
        self.storage_path = f"{os.getcwd()}/data/images/{image_folder}"
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        cover = response.xpath(
            '//figure[@class="cover"]/img[@class="image-novel"]/@src').get()
        yield scrapy.Request(
            url=cover,
            callback=self.download_image,
            headers={
                "User-Agent": self.ua,
                'Referer': current_url,
                'proxy': self.proxy
            },
            meta={
                'file': extract_file_from_url(cover),
            }
        )

        first_episode = content_box.xpath(
            './/div[@class="episode_sns"]/a[@class="first_episode"]/@href').get()

        yield response.follow(
            first_episode,
            callback=self.parse_episode,
            meta={
                'manhwa': manhwa
            }
        )

    def parse_episode(self, response):
        items = response.xpath(
            '//div[@class="chapter-content"]/div')[:20]

        for item in items:
            image = item.xpath('./img/@src').get()

            yield scrapy.Request(
                url=image,
                callback=self.download_image,
                headers={
                    "User-Agent": self.ua,
                    'Referer': response.request.url,
                    'proxy': self.proxy
                },
                meta={
                    'file': extract_file_from_url(image),
                }
            )

        yield response.meta['manhwa']

    def download_image(self, response):
        base64_data = base64.b64encode(response.body).decode('utf-8')
        decoded_data = base64.b64decode(base64_data)
        file_path = f'{self.storage_path}/{response.meta["file"]}'

        with open(file_path, 'wb') as file:
            file.write(decoded_data)

    def is_forbidden_category(self, category: str) -> bool:
        forbidden_list = ['Yaoi', 'BoyLove', 'Soft Yaoi', 'Đam Mỹ',
                          'Gender Bender', 'Truyện tranh 18+', 'Adult', 'Smut']

        if category in forbidden_list:
            return True
        else:
            return False
