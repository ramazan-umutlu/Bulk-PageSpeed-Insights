import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

def speed(current_url): 
    api = 'YOURAPI'
    url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="+str(current_url)+"&strategy=desktop&key="+api
    try:
        getresponse = requests.get(url)
        js = getresponse.json()
        performance = str (js['lighthouseResult']['categories']['performance']['score']*100)
        fid = js['lighthouseResult']['audits']['max-potential-fid']['displayValue']
        speedindex =  js['lighthouseResult']['audits']['speed-index']['displayValue']
        fcp = js['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
        lcp =  js['lighthouseResult']['audits']['largest-contentful-paint']['displayValue']
        cls = js['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
        totalbt = js['lighthouseResult']['audits']['total-blocking-time']['displayValue']
        interactive = js['lighthouseResult']['audits']['interactive']['displayValue']
        return current_url, performance, fid, speedindex, fcp, lcp, cls, totalbt, interactive
    except:
        print("An error occurred while making the API request for URL:", url)
        return None

sitemap_url = "https://yourwebsite.com/category-sitemap.xml"
response = requests.get(sitemap_url)
sitemap_xml = response.text

# Parse the XML and extract all the URLs
soup = BeautifulSoup(sitemap_xml, 'xml')
urls = soup.find_all('loc')

# Make an API request for each URL and store the results in a list
results = []
for url in urls:
    print(url.text)
    res = speed(url.text)
    if res:
        results.append(res)
        print(results)

# Save the results to an Excel file
df = pd.DataFrame(results, columns=['URL','Performance', 'FID', 'Speed Index', 'FCP', 'LCP', 'CLS', 'Total BT', 'Interactive'])
df.to_excel('YOUR PATH/results.xlsx')
