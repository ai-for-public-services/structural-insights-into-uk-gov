# Decision services index datasets

## TO DO 
1. **Get Variables to get for as many datasets as possible**:
   - Organisation
   - Topic
   - Verb (for 2012 data)
   

- **Analyse GDS transactions data**
    - digital volume


- **Analyse data on number of open central government websites over time** 


- **Analyse service 2 click transactions data**


- **Download, preprocess and analyse API and web scraping data on 2022 web-scraping-services** - using request_govuk_data.py
    - Find out how many of 361 X-GOV services are in GDS; and how many are different (based on URL and name)
        - Update variables (abbr, body, service_type, customer_type) based on GDS transactions spreadsheet and interpolate the rest by hand (i.e. using questionaire)
    - Collect data on services using web scraping and API for 'response time', 'digital (start now)'
    - https://dataingovernment.blog.gov.uk/2016/05/26/use-the-search-api-to-get-useful-information-about-gov-uk-content/
    - https://docs.publishing.service.gov.uk/repos/search-api.html
    - https://docs.publishing.service.gov.uk/repos.html
    - Variables to collect:
        - document_type
        - verb
        - priority
        - topic
     - Onces to potentially skip:
        - cost
        - time_to_complete
        - response_time
        
        
- **Preprocess and analyse SML questionnaire data of priority services (and others)**
    - Variables:
        - digital
        - service transaction type
    - Variables to check API data accuracy:
        - verb
        - document_type
        - service_name for priority services
    - Onces to potentially skip:
        - cost
        - time_to_complete
        - response_time
        
        
- **Download, preprocess and analyse data on civil service statistics**
   - Dataset: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/publicsectorpersonnel/datasets/publicsectoremploymentreferencetable Time: 2011-2022
   - Dataset: https://www.gov.uk/government/collections/civil-service-statistics  2006-2022
   - Dataset: https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/employmentandemployeetypes/methodologies/annualpopulationsurveyapsqmi#toc  Time: 2012-2022
   - Variables of interest:
      - 'headcount'?
      - 'Profession (e.g. operational delivery), Function (individual's role)'?
      - 'Occupation'?
      - 'Skill level'?
  


## Resources
- https://govuk-digital-services.herokuapp.com/domains
- https://www.instituteforgovernment.org.uk/explainers/professions-civil-service#:~:text=Civil%20servants%20undertake%20a%20wide,to%20people%20using%20public%20services.