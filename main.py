from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import time
import re
import datetime
from urllib.parse import urlparse

from utils import send_message_gmail

YOUR_GMAIL = "tech.guru.k.p@gmail.com"

if __name__ == '__main__':

    # url set
    url = input("Enter URL: ")
    # url = "https://www.betrush.com/tipster,1976.html"

    # Add a default scheme (e.g., "https://") if the URL doesn't have one
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Parse the URL
    parsed_url = urlparse(url)

    # Get the domain (including the scheme, e.g., "https://www.betrush.com")
    domain_with_scheme = parsed_url.netloc
    base_url = domain_with_scheme

    # Initialize the driver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    # driver.set_window_size(1366, 768)
    action = ActionChains(driver)

    prev_indic = []
    while True:
        driver.get(url)

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tipstername")))
        name = driver.find_element(By.CSS_SELECTOR, "div.tipstername").text
        trs = driver.find_elements(By.CSS_SELECTOR, 'div#bymonth table tbody tr')

        # for i in range(1, len(trs), 2):
        i = 1
        tds = trs[i].find_elements(By.TAG_NAME, 'td')
        pick = tds[len(tds) - 1].find_element(By.TAG_NAME, 'a')
        driver.execute_script("arguments[0].click();", pick)
        
        time.sleep(0.5)
        td_elements = trs[i + 1].find_elements(By.CSS_SELECTOR, "table.picks tbody tr td:first-child")
        picks = trs[i + 1].find_elements(By.CSS_SELECTOR, "table.picks tbody tr td.right_td span")

        new_indic = []
        for idx, td_element in enumerate(td_elements):

            if len(new_indic) >= 5:
                break

            inner_html = td_element.get_attribute('innerHTML')
            # Define a regex pattern to match text within double quotes
            pattern = r'>(.*?)<'
            # Use re.findall to find all matches in the input string
            matches = re.findall(pattern, inner_html)
            matches = [match for match in matches if match.strip()]

            # Append the extracted strings
            outer_html = trs[i + 1].find_element(By.CSS_SELECTOR, "table.picks tbody tr").get_attribute('outerHTML')
            # Step 1: Remove <br> tags using regex
            html_string_without_br = re.sub(r'<br\s*/*>', '', outer_html)
            # Step 2: Use regex to update URLs in the HTML string
            updated_html = re.sub(r'(src|href)="(?!https://)', r'\1="' + base_url + '/', html_string_without_br)

            # Send notification
            if picks[idx].text == '?':
                if len(matches) < 2:
                    continue
                is_new = not any(any(any(match == prev_match for prev_match in prev_idc) for prev_idc in prev_indic) for match in matches)
                
                if is_new:
                    html_content = f'''
<html>
<table>
<tbody>
{updated_html}
</tbody>
</table>
</html>
'''
                    # send_email(subject=name, html_content=html_content, email="tech.guru.k.p@gmail.com")
                    send_message_gmail (subject=name, msgHtml=html_content, to=YOUR_GMAIL, sender=YOUR_GMAIL, msgPlain="Betrush.com")
            
            new_indic.append(matches)
        if new_indic:
            prev_indic = new_indic
        time.sleep(5)
