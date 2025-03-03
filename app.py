from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Ensure Chrome is installed
CHROME_PATH = "/usr/bin/google-chrome"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# Function to initialize Selenium WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = CHROME_PATH  # Explicitly set Chrome binary location

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    return driver

# Google Search Function
def google_search(query, num_results, start_page):
    driver = init_driver()
    driver.get("https://www.google.com")
    search_box = driver.find_element("name", "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    results = []
    for page in range(start_page, start_page + (num_results // 10)):
        search_results = driver.find_elements("css selector", ".g")
        
        for result in search_results:
            try:
                title = result.find_element("css selector", "h3").text
                link = result.find_element("css selector", "a").get_attribute("href")
                results.append({"title": title, "link": link})
            except:
                continue

        try:
            next_button = driver.find_element("id", "pnnext")
            next_button.click()
            time.sleep(2)
        except:
            break

    driver.quit()
    return results

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    num_results = int(request.args.get('num_results', 10))
    start_page = int(request.args.get('start_page', 1))

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = google_search(query, num_results, start_page)
    return jsonify(results)

if __name__ == '__main__':
    from waitress import serve  # Production server for stability
    serve(app, host="0.0.0.0", port=8080)