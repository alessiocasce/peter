import requests
import random
import string
import re
import time
from mitmproxy.tools.main import mitmweb # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import subprocess
import re
import time
import os

def extract_stewie_lines(script_file):
    peters_lines = []
    with open(script_file, 'r') as file:
        script = file.read()
    
    # Split the script into sections by looking for lines starting with [Peter]
    peters_lines = re.findall(r'(?s)\[Stewie\]\n(.*?)\n\n', script, re.DOTALL)
    #print([item for peters_lines.split('\n') in peters_lines for item in peters_lines.split('\n')])
    nested_list = [line.split('\n') for line in peters_lines]
    flattened_list = [item for sublist in nested_list for item in sublist]
    
    return flattened_list

def send_get_request(video_id):
    url = f"https://www.tryparrotai.com/video?id={video_id}"
    

    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    # Wait for the video tag to load (wait for up to 5 seconds)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        # Extract the video src attribute after the page has loaded
        page_source = driver.page_source
        pattern = r'<video[^>]*\s+src="([^"]+)"'
        match = re.search(pattern, page_source)
        
        if match:
            video_src = match.group(1)
            print(video_src)
            return video_src.replace("amp;","")
        else:
            print("No video src found")
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Close the driver after use
    driver.quit()


def generate_video_id():
    return "w_" + "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(9, 12)))

def send_post_request(user_text):
    proxy = {
        'http': 'socks5h://127.0.0.1:9050',  # SOCKS5 protocol (for Tor)
        'https': 'socks5h://127.0.0.1:9050'
    }
    video_id = generate_video_id()
    
    url = "https://www.tryparrotai.com/api/create"
    headers = {
        "Host": "www.tryparrotai.com",
        "User-Agent": "kingssa",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://www.tryparrotai.com",
        "Referer": "https://www.tryparrotai.com/ai-voice/stewie-griffin",
    }
    data = {
        "userId": "webAnon",
        "videoId": video_id,
        "actorId": "14992f96-5d18-48e3-96c4-7997996cd039",
        "text": user_text,
        "communityVoice": True,
        "communityVoiceId": "14992f96-5d18-48e3-96c4-7997996cd039"
    }
    response = requests.post(url, headers=headers, json=data, proxies=proxy)
    print("POST Response:", response.text)
    if "false" in response.text:
        exit()
    return video_id
    

def download_video(video_url, video_id, index):
    output_path = f"./Stewie{index}.mp4"
    #command = ["curl", "-o", output_path, f'"{video_url}"']
    os.system(f'curl -o {output_path} "{video_url}"')
    print(f"Video downloaded to {output_path}")
    # Run the curl command
    #subprocess.Popen(command, shell=True)
if __name__ == "__main__":
    # Extract all Peter's lines from the script file
    peters_lines = extract_stewie_lines('./script.txt')
    
    # For each line that Peter says, generate a video and download it
    for index, line in enumerate(peters_lines, 1):  # Start index from 1
        if line[:2]=="//":
            print("Skipping: ", line)
            continue 
        print(f"Processing: {line}")
        video_id = send_post_request(line)
        time.sleep(2)  # Wait before making the GET request
        video_url = send_get_request(video_id)
        download_video(video_url, video_id, index)