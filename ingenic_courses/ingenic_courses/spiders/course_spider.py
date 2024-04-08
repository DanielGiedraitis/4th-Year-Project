import scrapy

class CourseSpider(scrapy.Spider):
    name = 'courses'
    start_urls = ['https://www.wit.ie/courses/type/undergraduate/#fifth', 'https://www.wit.ie/courses/type/postgraduate#sixth', 'https://ingenic.ie/?page_id=384']

    custom_settings = {
        'DOWNLOAD_DELAY': 2  
    }

    def parse(self, response):
        # Extract course links and relevant information
        if 'wit.ie' in response.url:
            if 'undergraduate' in response.url:
                level = 'Undergraduate'
            elif 'postgraduate' in response.url:
                level = 'Postgraduate'
                
            course_links = response.css('.item-course__title a')
            for course_link in course_links:
                course_title = course_link.css('::text').get().lower()
                if any(keyword in course_title for keyword in ['computer science', 'computer', 'computing', 'software', 'information technology', 'agile software', 'cloud architecture', 'data mining', 'mobile application', 'web development', 'user experience', 'digital animation', 'data analytics']):
                    yield response.follow(course_link, self.parse_course_wit, meta={'level': level})
        elif 'ingenic.ie' in response.url:
            course_links = response.css('tbody tr')
            for course_link in course_links:
                institution = course_link.css('td:nth-child(1) a::text').get()
                level = course_link.css('td:nth-child(2) p::text').get()
                course_title_links = course_link.css('td:nth-child(3) p a')
                for course_title_link in course_title_links:
                    course_title = course_title_link.css('::text').get().strip()
                    course_link = course_title_link.css('::attr(href)').get()
                    yield scrapy.Request(course_link, callback=self.parse_course_ingenic,
                                         meta={'institution': institution.strip(),
                                               'level': level.strip(),
                                               'course_title': course_title})


    def parse_course_wit(self, response):
        subtitle = response.css('h2.banner__subtitle::text').get()
        title = response.css('h1.banner__title::text').get()
        # Combine both subtitle and title into one line for the course title
        course_title = f"{subtitle} {title}"
        description = response.css('div.tab-panels__panel.active[data-tab-id="overview"] p::text').getall()
        description = [desc.strip() for desc in description if desc.strip()]
        level = response.meta['level']
        yield {
            'institution': 'Waterford Institute of Technology',
            'level': level,
            'course_title': course_title,
            'description': description
        }

    def parse_course_ingenic(self, response):
        institution = response.meta['institution']
        level = response.meta['level']
        course_title = response.meta['course_title']
        
        # Extract description based on institution
        # Trinity College Dublin
        if institution.strip() == 'Trinity College Dublin':
            description = response.css('.overview-full-section.flex-container p::text, .course-structure-full-section.flex-container p::text, .field--name-field-prospectus-about a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()] # Remove empty strings and strip whitespace


        # Dublin City University  
        elif institution.strip() == 'Dublin City University':
            if level.strip() == 'Undergrad':
                description = response.css('.overview-full-section.flex-container p::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            elif level.strip() == 'Postgrad':
                description = response.css('#collapse-prospectus-intro .field--item p::text, #collapse-prospectus-about .field--item p::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]


        # Dun Laoghaire Institute Of Art Design and Technology
        elif institution.strip() == 'Dun Laoghaire Institute Of Art Design and Technology':
            if course_title.strip() == 'BSc in Creative Computing':
                description = response.css('div.intro::text, div.content-block.text-wrapper.wys-block h2:contains("What will I do?") + ul li::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            elif course_title.strip() == 'BSc in Creative Media Technologies':
                description = response.css('.content-block.text-wrapper.wys-block p::text').getall()
                description = [desc.strip() for desc in description if desc.strip()]


        # University College Dublin   
        elif institution.strip() == 'University College Dublin':
            description = response.css('div.row.queries div.col-xs-12.col-md-8.content p::text, div.row.queries div.col-xs-12.col-md-8.content p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Technological University Dublin - City Centre Campus 
        elif institution.strip() == 'Technological University Dublin - City Centre Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Technological University Dublin - Tallaght Campus
        elif institution.strip() == 'Technological University Dublin - Tallaght Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Technological University Dublin - Blanchardstown Campus
        elif institution.strip() == 'Technological University Dublin - Blanchardstown Campus':
            description = response.css('.content-accordion__item #content-accordion__item1 .well.copy p::text').getall() + \
                          response.css('.content-accordion__item #content-accordion__item2 .well.copy p::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Institute of Technology Sligo
        elif institution.strip() == 'Institute of Technology Sligo':
            description = response.css('.course-tab-content[data-tab-title="Summary"] p::text, .course-tab-content[data-tab-title="Summary"] p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # University College Cork
        elif institution.strip() == 'University College Cork':
            description = response.css('ADD CSS SELECOR ::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # NUI Galway
        elif institution.strip() == 'NUI Galway':
            description = response.css('.tabsBody #course_overview p::text, .tabsBody #course_overview p a::attr(href)').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Institute of Technology Carlow
        elif institution.strip() == 'Institute of Technology Carlow':
            description = response.css('#tab-1 ::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Maynooth University
        elif institution.strip() == 'Maynooth University':
            if level.strip() == 'Undergrad':
                description = response.css('#content-tab__description ::text, #content-tab__description a::attr(href)').getall()
                description = [desc.strip() for desc in description if desc.strip()]
            elif level.strip() == 'Postgrad':
                description = response.css('#content-tab__overview ::text, #content-tab__overview a::attr(href), #content-tab__structure ::text, #content-tab__structure a::attr(href)').getall()
                description = [desc.strip() for desc in description if desc.strip()]


        # Munster Technological University - Cork Campus
        elif institution.strip() == 'Munster Technological University - Cork':
            description = response.css('').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Munster Technological University - Kerry Campus
        elif institution.strip() == 'Munster Technological University - Kerry Campus':
            description = response.css('ADD CSS SELECOR ::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]


        # Dundalk Institute of Technology
        elif institution.strip() == 'Dundalk Institute of Technology':
            description = response.css('#tab-summary + div.panel-collapse div.panel-body *::text, #headingDescription + div.panel-collapse div.panel-body *::text').getall()
            description = [desc.strip() for desc in description if desc.strip()]

        description = ' '.join(description).strip()
        yield {
            'institution': institution,
            'level': level,
            'course_title': course_title,
            'description': description
        }




