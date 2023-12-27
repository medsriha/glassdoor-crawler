# Glassdoor-crawler

This script is designed to collect only data science-related jobs. In case you need to scrape Software Engineering jobs, you will have to navigate to glassdoor.com, type "software engineering" in the search box, and paste the search result URL into the appropriate function.

It is important to note that Glassdoor may block your IP if the spider runs too fast. To avoid this, a time sleep of 5 milliseconds has been added to the script. 

The spider will collect the following data for every job position it scrapes: 
- job_title: the title of the job
- company_name: the name of the company hiring through Glassdoor
- location: the location of the job
- salary_estimated: the estimated salary provided by Glassdoor for the specific position
- salary_min: the minimum estimated salary for the particular position provided by Glassdoor
- salary_max: the maximum estimated salary for the specific position provided by Glassdoor
- date_posted: the date when the job position was posted on Glassdoor
- job_description: the description of the job

I hope this helps!
