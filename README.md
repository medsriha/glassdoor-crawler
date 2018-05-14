# Glassdoor-crawler
A spider which scraps data related to data science jobs from glassdoor.com.

This spider will collect only data science-related jobs, if you would like for example to spider Software Engineering jobs you need to go to glassdoor.com, type software engineering in the search box, and past the URL of the search result into the appropriate function. You will be familiar with the process while reading the code documentation. 

> Glassdoor will block your IP if the spider runs very fast, therefore, I have added a time sleep for around 5 milliseconds. 

For every position, the following are the Data to be collected by this program:

- `job_title`: Job title.
- `company_name`: Company hiring through Glassdoor.
- `location`: The location of the job.
- `salary_estimated`: Salary estimation of the specific position provided by Glassdoor.
- `salary_min`: minimum salary estimation of the specific position provided by Glassdoor.
- `salary_max`: maximum salary estimation of the specific position provided by Glassdoor.
- `date_posted`: data when the job position was posted on Glassdoor.
- `job_description`: Job description.
