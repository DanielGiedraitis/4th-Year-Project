import scrapy

class CourseSpider(scrapy.Spider):
    name = 'courses'
    start_urls = ['https://ingenic.ie/?page_id=384']

    # custom_settings = {
    #     'DOWNLOAD_DELAY': 2  
    # }

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
                # Call parse_course method to extract descriptions
                yield scrapy.Request(course_link, callback=self.parse_course,
                                     meta={'institution': institution.strip(),
                                           'level': level.strip(),
                                           'course_title': course_title})

    def parse_course(self, response):
        institution = response.meta['institution']
        level = response.meta['level']
        course_title = response.meta['course_title']
        # Extract description based on institution
        if institution.strip() == 'Trinity College Dublin':
            description = response.css('.overview-full-section.flex-container p::text, .course-structure-full-section.flex-container p::text, .field--name-field-prospectus-about a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()] # Remove empty strings and strip whitespace
            course_content = response.css('ADD CSS SELECOR ::text').getall()


        description = ' '.join(description).strip()
        yield {
            'institution': institution,
            'level': level,
            'course_title': course_title,
            'description': description,
            'course_content': course_content
        }




