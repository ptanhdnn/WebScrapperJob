from requests import get
from bs4 import BeautifulSoup
import re

import pandas as pd

base_url = "https://itviec.com/viec-lam-it/"
search_terms = ["python", "java"]

for search_term in search_terms:
    response = get(f"{base_url}{search_term}")

    if response.status_code != 200:
        print("can't request website")

    else:
        soup = BeautifulSoup(response.text, "html.parser")

        # Get number of jobs of searching and calculate number of page
        count = soup.find("h1").text.strip()
        number = re.findall(r'\d+', count)                      
        last_page_no = int(int(number[0])/20+1)

        data = []
        for i in range(1, last_page_no, 1):
            response_page = get(f"{base_url}{search_term}?locale=vi&page={i}&source=search_job")
            a_soup = BeautifulSoup(response_page.text, "html.parser")
            a_jobs = a_soup.find_all("h3", class_="title job-details-link-wrapper")
            a_adrs = a_soup.find_all("div", class_="text")
            a_time = a_soup.find_all("span", class_="distance-time")

            # Get title name, company name, address, time, link to access:
            for i in range(20):
                sub_details = []
                title = a_jobs[i].find("a").string
                link = base_url[:-13] + a_jobs[i].find("a").get("href")
                address = a_adrs[i].string
                time = a_time[i].string.split("\n")

                # Access page for more detals
                respone_inside = get(f"{link}")
                i_soup = BeautifulSoup(respone_inside.text, "html.parser")
                a_comp = i_soup.find_all("h3", class_="employer-long-overview__name hidden-xs d-none d-sm-block")
                i_comp = a_comp[0].find("a").string

                i_country = i_soup.find_all("div", class_="svg-icon__text")[-2].string



                sub_details.extend([title, i_comp, i_country, address, time[1], link])
                data.append(sub_details)
    
    data = pd.DataFrame(data, columns = ['job', 'company', 'country', 'address', 'time', 'link'])
    data.to_csv(f"job_{search_term}.csv")
print("done!!!")