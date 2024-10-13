# Assignment 3

import argparse
import requests
import csv
import re
from datetime import datetime

def download_web_log(url):
    """Download data from a given URL and returns it."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error dowloading log file: {e}")
        return None

def process_log_data(log_data):
    """Process the download data"""
    reader = csv.reader(log_data.splitlines())

    log_entries = []
    for row in reader:
        log_entries.append({
            "path": row[0],
            "datetime": row[1],
            "browser": row[2],
            "status": row[3],
            "size": row[4]
         })
    return (log_entries)

def analyze_image_requests(log_entries):
    """Calculates the percentage of images"""
    image_hits = 0
    total_hits = len(log_entries)

    for entry in log_entries:
        if re.search(r"\.(jpg|gif|png)$", entry ["path"], re.IGNORECASE):
            image_hits += 1

    image_percentage = (image_hits/ total_hits) * 100
    print(f"Image requests account for {image_percentage:.1f}% of all requests")

def find_most_popular_browser(log_entries):
    """Finds the most popular browser"""
    browser_counts = {}
    for entry in log_entries:
        if "Firefox" in entry["browser"]:
            browser_counts["Firefox"] = browser_counts.get("Firefox" , 0) + 1
        elif "Chrome" in entry ["browser"]:
            browser_counts ["Chrome"] = browser_counts.get ("Chrome", 0) + 1
        elif "Internet Explorer" in entry ["browser"]:
            browser_counts ["Internet Explorer"] = browser_counts.get ("Internet Explorer", 0) + 1
        elif "Safari" in entry ["browser"]:
            browser_counts ["Safari"] = browser_counts.get ("Safari", 0) + 1

    most_popular_browser = max(browser_counts, key=browser_counts.get)
    print(f"The most popular browser is {most_popular_browser}")

def analyze_hourly_hits(log_entries):
    """Calculates the numbers of hist per hour"""
    hourly_hits = {}
    for entry in log_entries:
        hour = datetime.strptime(entry["datetime"], "%Y-%m-%d %H:%M:%S").hour
        hourly_hits[hour] = hourly_hits.get(hour, 0) + 1

    for hour, hits in sorted(hourly_hits.items(), key=lambda item: item[1], reverse=True):
        print(f"Hour {hour:02d} has {hits} hits")

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description="Process a web log file.")
    parser.add_argument("url", help="URL of the web log file")
    args = parser.parse_args()

    log_data = download_web_log(args.url)
    if log_data:
        log_entries = process_log_data(log_data)

        analyze_image_requests(log_entries)
        find_most_popular_browser(log_entries)
        analyze_hourly_hits(log_entries)

# I added the URL under script parameters (http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv)
