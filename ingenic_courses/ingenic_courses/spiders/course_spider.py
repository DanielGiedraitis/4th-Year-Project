import scrapy

class CourseSpider(scrapy.Spider):
    name = 'courses'
    start_urls = ['https://ingenic.ie/?page_id=384']

    def parse(self, response):
        # Extract course links
        course_links = response.css('tbody tr')
        for course_link in course_links:
            institution = course_link.css('td:nth-child(1) a::text').get()
            level = course_link.css('td:nth-child(2) p::text').get()
            course_titles = course_link.css('td:nth-child(3) p a::text').getall()
            for course_title in course_titles:
                yield {
                    'institution': institution.strip(),
                    'level': level.strip(),
                    'course_title': course_title.strip()
                }

