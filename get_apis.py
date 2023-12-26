

from selenium import webdriver 
import time 
import json
from selenium.webdriver.chrome.service import Service


def get_apis(url):
    """
        Makes request to passed-in URL with Selenium and Chrome Driver
        then accesses performance logs to parse out logged network requests 
        and saves them to a JSON file. 
    """
  
    # Create the webdriver object and pass the arguments 
    options = webdriver.ChromeOptions() 
  
    # Chrome will start in Headless mode 
    options.add_argument('headless') 

    # Adds logging capability
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
  
    # Ignores any certificate errors if there is any 
    options.add_argument("--ignore-certificate-errors") 
  
    # Startup the chrome webdriver with executable path and 
    # pass the chrome options and desired capabilities as 
    # parameters. 
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    # Send a request to the website and let it load 
    driver.get(url) 
  
    # Sleeps for 10 seconds 
    time.sleep(10) 
  
    # Gets all the logs from performance in Chrome 
    logs = driver.get_log("performance") 
  
    # Opens a writable JSON file and writes the logs in it 
    with open("network_log.json", "w", encoding="utf-8") as f: 
        f.write("[") 
  
        # Iterates every logs and parses it using JSON 
        for log in logs: 
            network_log = json.loads(log["message"])["message"] 
  
            # Checks if the current 'method' key has any 
            # Network related value. 
            if("Network.response" in network_log["method"] 
                    or "Network.request" in network_log["method"] 
                    or "Network.webSocket" in network_log["method"]): 
  
                # Writes the network log to a JSON file by 
                # converting the dictionary to a JSON string 
                # using json.dumps(). 
                f.write(json.dumps(network_log)+",") 
        f.write("{}]") 
  
    print("Quitting Selenium WebDriver") 
    driver.quit() 

    # Call helper function to read network_logs file and parse out gtag requests
    get_gtag_requests()

def get_gtag_requests():
    """
        Read the JSON File and parse it using 
        json.loads() to find the urls containing Google Tag requests. 
        Write the whole request to a json file.
    """

    # Read in network log file created in function above 
    json_file_path = "network_log.json"
    with open(json_file_path, "r", encoding="utf-8") as f: 
        logs = json.loads(f.read()) 
  
    gtag = ''
    with open("gtag_requests.json", "w", encoding="utf-8") as g: 
        g.write("[") 
        # Iterate the logs 
        for log in logs: 
            # Except block will be accessed if any of the 
            # following keys are missing. 
                try: 
                    # URL is present inside the following keys 
                    url = log["params"]["request"]["url"] 
                    # If network request is calling gtm.js
                    if url.__contains__("gtm"):
                        gtag = log["params"]
                        g.write(json.dumps(gtag)+",")
                except Exception as e: 
                    pass
        g.write("{}]") 
