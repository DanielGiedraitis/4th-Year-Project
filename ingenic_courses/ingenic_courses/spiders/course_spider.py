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
        # Trinity College Dublin
        if institution.strip() == 'Trinity College Dublin':
            description = response.css('.overview-full-section.flex-container p::text, .course-structure-full-section.flex-container p::text, .field--name-field-prospectus-about a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()] # Remove empty strings and strip whitespace
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Dublin City University  
        elif institution.strip() == 'Dublin City University':
            if level.strip() == 'Undergrad':
                description = response.css('.overview-full-section.flex-container p::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            elif level.strip() == 'Postgrad':
                description = response.css('#collapse-prospectus-intro .field--item p::text, #collapse-prospectus-about .field--item p::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            
            course_content = response.css('.course-structure-full-section.flex-container ::text, .course-structure-full-section.flex-container a::attr(href)').getall()
            course_content = [course.strip() for course in course_content if course.strip()] 

        # Dun Laoghaire Institute Of Art Design and Technology
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

        # University College Dublin   
        elif institution.strip() == 'University College Dublin':
            description = response.css('div.row.queries div.col-xs-12.col-md-8.content p::text, div.row.queries div.col-xs-12.col-md-8.content p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()
            course_content = [course.strip() for course in course_content if course.strip()] 

        # Technological University Dublin - City Centre Campus 
        elif institution.strip() == 'Technological University Dublin - City Centre Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Technological University Dublin - Tallaght Campus
        elif institution.strip() == 'Technological University Dublin - Tallaght Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Technological University Dublin - Blanchardstown Campus
        elif institution.strip() == 'Technological University Dublin - Blanchardstown Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Institute of Technology Sligo
        elif institution.strip() == 'Institute of Technology Sligo':
            description = response.css('.course-tab-content[data-tab-title="Summary"] p::text, .course-tab-content[data-tab-title="Summary"] p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # University College Cork
        elif institution.strip() == 'University College Cork':
            description = response.css('ADD CSS SELECOR ::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # NUI Galway
        elif institution.strip() == 'NUI Galway':
            description = response.css('.tabsBody #course_overview p::text, .tabsBody #course_overview p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Institute of Technology Carlow
        elif institution.strip() == 'Institute of Technology Carlow':
            description = response.css('#tab-1 ::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Maynooth University
        elif institution.strip() == 'Maynooth University':
            if level.strip() == 'Undergrad':
                description = response.css('#content-tab__description ::text, #content-tab__description a::attr(href)').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            elif level.strip() == 'Postgrad':
                description = response.css('#content-tab__overview ::text, #content-tab__overview a::attr(href), #content-tab__structure ::text, #content-tab__structure a::attr(href)').getall()
                description = [desc.strip() for desc in description if desc.strip()]

            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Munster Technological University - Cork Campus
        elif institution.strip() == 'Munster Technological University - Cork':
            description = response.css('').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Munster Technological University - Kerry Campus
        elif institution.strip() == 'Munster Technological University - Kerry Campus':
            description = response.css('ADD CSS SELECOR ::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            course_content = response.css('ADD CSS SELECOR ::text').getall()

        # Dundalk Institute of Technology
        elif institution.strip() == 'Dundalk Institute of Technology':
            description = response.css('#tab-summary + div.panel-collapse div.panel-body *::text, #headingDescription + div.panel-collapse div.panel-body *::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]
            # course_content = response.css('#headingContent + div.panel-collapse div.panel-body *::text').getall()
            course_content = [course.strip() for course in course_content if course.strip()]

        description = ' '.join(description).strip()
        yield {
            'institution': institution,
            'level': level,
            'course_title': course_title,
            'description': description,
            'course_content': course_content
        }




