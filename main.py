import requests
from bs4 import BeautifulSoup

class LinkedInJobsScraper:
    def __init__(self):
        self.api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=python&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start='

    def fetch_jobs(self, start_page=0):
        url = self.api_url + str(start_page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve job listings: {response.status_code}")
            return None

    def parse_jobs(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = soup.find_all('li')

        job_list = []
        for job in jobs:
            job_item = {}
            job_item['job_title'] = job.find('h3').get_text(strip=True) if job.find('h3') else 'not-found'
            job_item['job_detail_url'] = job.find('a', {'class': 'base-card__full-link'})['href'].strip() if job.find('a', {'class': 'base-card__full-link'}) else 'not-found'
            job_item['job_listed'] = job.find('time').get_text(strip=True) if job.find('time') else 'not-found'
            job_item['company_name'] = job.find('h4').find('a').get_text(strip=True) if job.find('h4') and job.find('h4').find('a') else 'not-found'
            job_item['company_link'] = job.find('h4').find('a')['href'].strip() if job.find('h4') and job.find('a') else 'not-found'
            job_item['company_location'] = job.find('span', {'class': 'job-search-card__location'}).get_text(strip=True) if job.find('span', {'class': 'job-search-card__location'}) else 'not-found'
            job_list.append(job_item)
        
        return job_list

    def scrape_jobs(self, start_page=0):
        html_content = self.fetch_jobs(start_page)
        if html_content:
            job_list = self.parse_jobs(html_content)
            return job_list
        else:
            print("Failed to retrieve job listings")
            return None

if __name__ == '__main__':
    scraper = LinkedInJobsScraper()
    jobs = scraper.scrape_jobs(start_page=0)
    if jobs is not None:
        for job in jobs:
            print(f"Job Title: {job['job_title']}")
            print(f"Job Detail URL: {job['job_detail_url']}")
            print(f"Job Listed: {job['job_listed']}")
            print(f"Company Name: {job['company_name']}")
            print(f"Company Link: {job['company_link']}")
            print(f"Company Location: {job['company_location']}")
            print('----------------------------')
    else:
        print("No jobs found or failed to retrieve jobs.")
