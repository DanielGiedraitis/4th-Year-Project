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
            course_title_links = course_link.css('td:nth-child(3) p a')
            for course_title_link in course_title_links:
                course_title = course_title_link.css('::text').get().strip()
                course_link = course_title_link.css('::attr(href)').get()
                yield {
                    'institution': institution.strip(),
                    'level': level.strip(),
                    'course_title': course_title,
                    'course_link': course_link
                }


