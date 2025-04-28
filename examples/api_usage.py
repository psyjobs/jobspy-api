import requests
import json
import pandas as pd

# Base URL for the API
BASE_URL = "http://localhost:8000"

def search_jobs_simple():
    """
    Simple job search using the consolidated GET endpoint
    """
    params = {
        "site_name": ["indeed", "linkedin"],
        "search_term": "software engineer",
        "location": "San Francisco, CA",
        "results_wanted": 5
    }
    
    response = requests.get(f"{BASE_URL}/api/v1/search_jobs", params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} jobs")
        
        # Convert to pandas DataFrame for easier viewing
        df = pd.DataFrame(data['jobs'])
        print(df.head())
        
        # Save to CSV
        df.to_csv("jobs_simple.csv", index=False)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def search_jobs_advanced():
    """
    Advanced job search using GET endpoint with all parameters
    """
    params = {
        "site_name": ["indeed", "linkedin", "zip_recruiter"],
        "search_term": "data scientist",
        "google_search_term": "data scientist jobs near New York, NY since yesterday",
        "location": "New York, NY",
        "distance": 25,
        "job_type": "fulltime",
        "is_remote": True,
        "results_wanted": 10,
        "hours_old": 48,
        "description_format": "markdown",
        "country_indeed": "USA",
        "enforce_annual_salary": True,
        "linkedin_fetch_description": True
    }
    
    response = requests.get(
        f"{BASE_URL}/api/v1/search_jobs",
        params=params
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} jobs")
        
        # Convert to pandas DataFrame for easier viewing
        df = pd.DataFrame(data['jobs'])
        print(df.head())
        
        # Save to CSV
        df.to_csv("jobs_advanced.csv", index=False)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def search_jobs_paginated():
    """
    Paginated job search using GET endpoint
    """
    params = {
        "paginate": True,
        "page": 1,
        "page_size": 5,
        "site_name": ["indeed", "linkedin"],
        "search_term": "software engineer",
        "location": "San Francisco, CA",
        "results_wanted": 20
    }
    
    response = requests.get(f"{BASE_URL}/api/v1/search_jobs", params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Found {data['count']} total jobs, showing page {data['current_page']} of {data['total_pages']}")
        print(f"Page size: {data['page_size']}, showing {len(data['jobs'])} jobs")
        
        # Convert to pandas DataFrame for easier viewing
        df = pd.DataFrame(data['jobs'])
        print(df.head())
        
        # Check if there's a next page
        if data['next_page']:
            print(f"Next page URL: {data['next_page']}")
        
        # Save to CSV
        df.to_csv("jobs_paginated.csv", index=False)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print("Running simple job search...")
    search_jobs_simple()
    
    print("\nRunning advanced job search...")
    search_jobs_advanced()
    
    print("\nRunning paginated job search...")
    search_jobs_paginated()
