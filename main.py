import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
from fake_useragent import UserAgent

class LinkedInJobsScraper:
    def __init__(self):
        self.api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=python&location=United%2BStates&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&start=0'
        self.user_agent = UserAgent()  

    def fetch_jobs(self):
        headers = {
            'User-Agent': self.user_agent.random  
        }
        try:
            response = requests.get(self.api_url, headers=headers)
            response.raise_for_status()  
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve job listings: {e}")
            return None

    def parse_jobs(self, html_content):
        try:
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
        except Exception as e:
            print(f"Failed to parse job listings: {e}")
            return []

    def scrape_jobs(self):
        html_content = self.fetch_jobs()
        if html_content:
            job_list = self.parse_jobs(html_content)
            return job_list
        else:
            print("Failed to retrieve job listings")
            return None

def start_scraping():
    scraper = LinkedInJobsScraper()
    jobs = scraper.scrape_jobs()  
    if jobs is not None:
        text_area.delete('1.0', tk.END)  
        for job in jobs:
            text_area.insert(tk.END, f"Job Title: {job['job_title']}\n")
            text_area.insert(tk.END, f"Job Detail URL: {job['job_detail_url']}\n")
            text_area.insert(tk.END, f"Job Listed: {job['job_listed']}\n")
            text_area.insert(tk.END, f"Company Name: {job['company_name']}\n")
            text_area.insert(tk.END, f"Company Link: {job['company_link']}\n")
            text_area.insert(tk.END, f"Company Location: {job['company_location']}\n")
            text_area.insert(tk.END, '----------------------------\n')
    else:
        text_area.insert(tk.END, "No jobs found or failed to retrieve jobs.\n")

root = tk.Tk()
root.title("LinkedIn Jobs Scraper")

text_area = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
text_area.pack(padx=10, pady=10)

scrape_button = tk.Button(root, text="Scrape", command=start_scraping)
scrape_button.pack(pady=10)

root.mainloop()
