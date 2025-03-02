from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Function to initialize Selenium WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless (without GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Function to perform Google search and fetch results
def google_search(query, num_results, start_page):
    driver = init_driver()
    
    # Navigate to Google
    driver.get("https://www.google.com")
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the page to load
    
    results = []
    
    # Collect results from multiple pages
    for page in range(start_page, start_page + (num_results // 10)):
        # Scrape results from the current page
        search_results = driver.find_elements_by_css_selector(".g")
        
        for result in search_results:
            title = result.find_element_by_css_selector("h3").text
            link = result.find_element_by_css_selector("a").get_attribute("href")
            results.append({"title": title, "link": link})
        
        # Go to the next page
        next_button = driver.find_element_by_id("pnnext")
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    
    driver.quit()
    return results

# Example usage:
query = "Lead generation techniques"
num_results = 30
start_page = 1
results = google_search(query, num_results, start_page)

# Print results
for idx, result in enumerate(results):
    print(f"{idx+1}. {result['title']} - {result['link']}")
