# Datasets


#### Title: GOV.UK service pages
 - Source(s): gov  
 - Access: scrape
 - Variables of interest:
      - 'organisation', 'service task name', 'service description', 'task output', 'response time', 'type of task', 'task stimuli',  'digital service', 'cost'
  - IMPUTE: service_type
  - Time: 2022
  - Contact: Tara Stockford, GDS


#### Title: Open government websites
  - Source(s): gov (click [here](https://www.gov.uk/government/collections/central-government-websites) for info)
  - Access: download
  - Variables of interest:
      - 'existence of service'
  - Time: 2011-2018


#### Title: GOV.UK unique clicks
  - Source(s): gov, ind
  - Access: request
  - Variables of interest:
      - 'total volume', 'annual volume'
  - Time: 2022
  - Contact: Clifford Sheppard, GDS
  - Notes: where missing get website traffic trends from 3rd party site?


#### Title: Civil service statistics
  - Source(s): gov, ind
  - Access: download, request
  - Variables of interest:
      - 'headcount', 'profession (e.g. operational delivery)', 'function (individual's role)',  'occupation', 'skill level'
      
      
#### Title: Service transactions
  - Source: gov
  - Access: request
  - Variables of interest:
      - 'total volume', 'annual volume', 'digital volume'
 - Time: 2013-2018
 
#### Title: Search for service AI use
  - Source: web, ind
  - Access: scrape
   - Variables of interest:
      - 'ML present', 'decision/agent'
   - Time: 2022


**Professions and Functions**

The professions of civil servants were collected for the first time in 2007. Profession relates to the ‘post’ occupied by the person and is not dependent on any qualifications the individual may have. The range of professions includes economics, science and engineering, finance, human resources, legal, and tax. Employees can alternatively be assigned to operational delivery (delivering frontline services) or policy delivery (designing or enhancing services to the public). If a post could be considered operational delivery but also matches one of the specific professions, the person is assigned to the specific profession. It should not be assumed that those classified to operational delivery represent all those delivering frontline services.

For the first time in 2020, organisations were also required to provide data on the ‘Function’ within which an employee works. This differs from a ‘profession’ in that a function delivers a defined and cross-cutting set of services to a department – and the Civil Service as a whole – through a collection of roles, and can contain a mixture of professions.

Users should note the variable and high non-response rates for professions and functions for a number of organisations and should exercise appropriate caution when drawing conclusions from these statistics or when making comparisons between organisations or over time.

# Notes on GDS transactions data

Please note that many of the services listed here have never been available online, and many will probably have been closed, merged or renamed since the last data collection (in 2018). The data listed is not service-specific, and is limited to total transaction volumes and digital transaction volumes, with a small amount of cost-per-transaction data. Some smaller services didn't provide any data, but we still wanted them listed as a record of what services existed. Service-specific data and some more granular service data was captured elsewhere and doesn't seem to be available from the National Archives either.

The transactions include successful and unsuccessfull applications.

**Missing data**
- We filled out X missing data values for the column 'service_type'; this was done easily by looking at the service name and how related services in the same organisation and body had been categorised. 

**Remaining questions**:
- We can still investigate the individual services by going through all the comments


# Notes on 2022 GOV.UK data clicks

The data shows:
- Page: URL of the page on GOV.UK that has the link - some pages have multiple links
- Page title: as displayed on GOV.UK
- Link clicked: URL of the link clicked - links may be held on multiple GOV.UK pages
- First organisation: name of the first organisation listed as contributor to the GOV.UK page (usually, but not always, the principal owner of the content); if a service is linked from the page, the same organisation will often own that service too
- Unique clicks: number of GOV.UK sessions in which the link was clicked

Some notes on the data:
- although we see how often users clicked to access services, we don't have data on the number of transactions that were subsequently started or completed
- many services are accessible only from these GOV.UK pages, but some may also be accessed directly from other sites or from search engines
- only a small number of non-service links have been filtered out - e.g. links to YouTube, GOV.UK attachments (PDFs, CSVs etc)
- many links to services/content managed by local authorities are included - http://www.merton.gov.uk/bluebadge etc
- ditto for NHS services/content
- links with fewer than 100 unique clicks in those 12 months aren't included
- The 'service domains' tab lists many domains which host government services. Although they are 'service.gov.uk' they are not included in the GOV.UK domain, so we have no data on traffic. Some of these will need a www. prefix to work, and some may not be in use. 


# Notes on list of .gov.uk domain names

**Details**
The UK government manages the .gov.uk domain name.

Public sector bodies may register .gov.uk domain names for a variety of reasons. The rules governing which organisations can register for a .gov.uk domain names, how to choose appropriate names and manage them are set out in the apply for a .gov.uk domain name: step by step.

**About the list of .gov.uk domains**
The list of .gov.uk domain names is available in CSV format with 3 columns.

Domain name: the domain name registered for use, which should work with or without a preceding ‘www’.

Owner: the name of the organisation that owns the domain name, for example a central government department or local authority.

Representing: the organisation the domain name is registered for, often the same as the owner but could be an agency or other organisation the owner is registering the domain on behalf of.


# Notes on open government websites

**Background**
Number and list of central government open websites – 440 as at 31 October 2013.

The Cabinet Office committed to begin quarterly publication of the number of open websites starting in the financial year 2011.

**Definition of a website**
The definition used is a user-centric one. Something is counted as a separate website if it is active and either has a separate domain name or, when as a subdomain, the user cannot move freely between the subsite and parent site and there is no family likeness in the design. In other words, if the user experiences it as a separate site in their normal uses of browsing, search and interaction, it is counted as one.

**Definition of a closed website**
A website is considered closed when it ceases to be actively funded, run and managed by central government, either by packaging information and putting it in the right place for the intended audience on another website or digital channel, or by a third party taking and managing it and bearing the cost. Where appropriate, domains stay operational in order to redirect users to the UK Government Website Archive.

**Definition of the exemption process**
The GOV.UK exemption process began with a web rationalisation of the government’s Internet estate to reduce the number of obsolete websites and to establish the scale of the websites that the government owns.

**Exclusions from the central government list**
Not included in the number or list are:

websites of public corporations as listed on the Office for National Statistics website
partnerships more than half-funded by private sector
charities and national museums
specialist closed audience functions, such as the BIS Research Councils, BIS Sector Skills Councils and Industrial Training Boards, and the Defra Levy Boards and their websites
Finally, those public bodies set up by Parliament and reporting directly to the Speaker’s Committee are also excluded (for example, the Electoral Commission and IPSA).

As agreed in the quarterly report of February 2013, the following sites have been included in the list:

‘independent’ sites
National parks
Inclusion under department name
Websites are listed under the department name for which the minister in HMG has responsibility, either directly through their departmental activities, or indirectly through being the minister reporting to Parliament for independent bodies set up by statute.

**October 2013 report**
Government website domains have been procured from as early as the 1990’s and at this time, there was no requirement upon government departments to retain a formal record of ownership. With staff changes and new departments formed, it became apparent that departments did not have a complete view of all sites in their estate.

Government Digital Service (GDS) has worked closely with these departments to identify legacy websites which we were not originally aware of, by going through the complete list of gov.uk domains managed by Cabinet Office, under the second level domain (SLD), gov.uk. A full list of gov.uk domains can be viewed here. As well as websites on the gov.uk SLD, we had found that there are a number of legacy websites owned by departments under a .org.uk or co.uk SLD. Because we do not own these SLDs, information on whether a department has ownership was not so easily accessible, but a strong working relationship with department leads has since helped to identify the majority of these sites.

Previously, the Ministry of Defence conducted their own rationalisation of MOD and the armed forces sites. At the beginning of this report, we agreed to include these sites to ensure a consistent approach.

Since the last report of June 2013, 14 websites have closed and 15 have migrated to the government’s website, GOV.UK. As government websites migrate to GOV.UK, the responsibility for reporting a department’s content will become an overall GOV.UK reporting requirement.

The GOV.UK website, created and managed by the GDS in Cabinet Office, provides a single point of access to HM Government services in an easily accessible way. GDS works closely with departments to close existing websites and migrate their content where necessary to GOV.UK. The overall number of websites reported on has increased since last year as we have gained a better understanding of the government’s web estate. This is a positive message as it means that GDS is able to show transparency in reporting and a clearer, comprehensive picture concerning the management of government websites, whilst ensuring that data and information, vital and relevant to the public, becomes available on GOV.UK.

# Notes on govuk-unique-visitors

The 'External links' tab shows clicks from GOV.UK to other domains in the 12 months from 1 Oct 2021 to 30 Sep 2022. It will therefore give you an idea of traffic to most government services, although it also includes links to content hosted elsewhere (it's difficult to filter this out).

The data shows:
- Page: URL of the page on GOV.UK that has the link - some pages have multiple links
- Page title: as displayed on GOV.UK
- Link clicked: URL of the link clicked - links may be held on multiple GOV.UK pages
- First organisation: name of the first organisation listed as contributor to the GOV.UK page (usually, but not always, the principal owner of the content); if a service is linked from the page, the same organisation will often own that service too
- Unique clicks: number of GOV.UK sessions in which the link was clicked

Some notes on the data:
- although we see how often users clicked to access services, we don't have data on the number of transactions that were subsequently started or completed
- many services are accessible only from these GOV.UK pages, but some may also be accessed directly from other sites or from search engines
- only a small number of non-service links have been filtered out - e.g. links to YouTube, GOV.UK attachments (PDFs, CSVs etc)
- many links to services/content managed by local authorities are included - http://www.merton.gov.uk/bluebadge etc
- ditto for NHS services/content
- links with fewer than 100 unique clicks in those 12 months aren't included


