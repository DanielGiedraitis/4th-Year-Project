import scrapy

class CourseSpider(scrapy.Spider):
    name = 'courses'
    start_urls = ['https://ingenic.ie/?page_id=384']

    custom_settings = {
        'DOWNLOAD_DELAY': 2  
    }

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
        elif institution.strip() == 'Dublin City University':
            description = response.css('.overview-full-section.flex-container p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('.course-structure-full-section.flex-container ::text, .course-structure-full-section.flex-container a::attr(href)').getall()
            course_content = [course.strip() for course in course_content if course.strip()] 
        elif institution.strip() == 'Dun Laoghaire Institute Of Art Design and Technology':
            if course_title.strip() == 'BSc in Creative Computing':
                description = response.css('div.intro::text, div.content-block.text-wrapper.wys-block h2:contains("What will I do?") + ul li::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            elif course_title.strip() == 'BSc in Creative Media Technologies':
                description = response.css('.content-block.text-wrapper.wys-block p::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]

            # Extract headings and module details
            headings = response.css('.content-block.expander-block.accordion.faq.list-faq.panel-group .item-faq.panel .question.panel-title a::text').getall()
            module_details = response.css('.content-block.expander-block.accordion.faq.list-faq.panel-group .item-faq.panel .panel-body p::text').getall()
            course_content = [f"{headings[i]}: {module_details[i]}" for i in range(len(headings))]
            course_content = [course.strip() for course in course_content if course.strip()] 
        elif institution.strip() == 'University College Dublin':
            description = response.css('div.row.queries div.col-xs-12.col-md-8.content p::text, div.row.queries div.col-xs-12.col-md-8.content p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()
            course_content = [course.strip() for course in course_content if course.strip()] 
        elif institution.strip() == 'Technological University Dublin - City Centre Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()
            
        description = ' '.join(description).strip()
        yield {
            'institution': institution,
            'level': level,
            'course_title': course_title,
            'description': description,
            'course_content': course_content
        }




