"""Load testing script for the JobSpy Docker API."""
import argparse
import asyncio
import random
import statistics
import time
from typing import Any, Dict, List

import aiohttp

# Job titles and locations for random queries
JOB_TITLES = ["software engineer", "data scientist", "product manager", "devops engineer", "full stack developer"]
LOCATIONS = ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA"]

async def make_request(session, url, api_key, params=None, json_data=None):
    """Make an HTTP request and measure response time."""
    headers = {"x-api-key": api_key, "accept": "application/json"}
    
    start_time = time.time()
    
    if json_data:
        async with session.post(url, headers=headers, json=json_data) as response:
            data = await response.json()
            status = response.status
    else:
        async with session.get(url, headers=headers, params=params) as response:
            data = await response.json()
            status = response.status
            
    end_time = time.time()
    response_time = end_time - start_time
    
    return {
        "status": status,
        "response_time": response_time,
        "data": data
    }

async def run_load_test(base_url, api_key, num_requests, concurrency):
    """Run a load test with the specified number of concurrent requests."""
    print(f"Starting load test with {num_requests} total requests, {concurrency} concurrent")
    
    # Create a connection pool
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        
        for _ in range(num_requests):
            # Generate random query parameters
            job_title = random.choice(JOB_TITLES)
            location = random.choice(LOCATIONS)
            
            # Randomly choose between GET and POST
            if random.choice([True, False]):
                # GET request
                params = {
                    "site_name": random.sample(["indeed", "linkedin", "zip_recruiter"], 1),
                    "search_term": job_title,
                    "location": location,
                    "results_wanted": 5
                }
                tasks.append(make_request(session, f"{base_url}/api/v1/search_jobs", api_key, params=params))
            else:
                # POST request
                json_data = {
                    "site_name": random.sample(["indeed", "linkedin", "zip_recruiter"], 2),
                    "search_term": job_title,
                    "location": location,
                    "results_wanted": 5
                }
                tasks.append(make_request(session, f"{base_url}/api/v1/search_jobs", api_key, json_data=json_data))
        
        # Execute requests with limited concurrency
        results = []
        for i in range(0, len(tasks), concurrency):
            batch = tasks[i:i+concurrency]
            batch_results = await asyncio.gather(*batch)
            results.extend(batch_results)
            print(f"Completed {min(i+concurrency, len(tasks))}/{len(tasks)} requests")
        
        return results

def analyze_results(results):
    """Analyze load test results."""
    response_times = [r["response_time"] for r in results]
    statuses = [r["status"] for r in results]
    
    # Calculate statistics
    avg_time = statistics.mean(response_times)
    median_time = statistics.median(response_times)
    min_time = min(response_times)
    max_time = max(response_times)
    p95_time = sorted(response_times)[int(len(response_times) * 0.95)]
    
    success_count = statuses.count(200)
    error_count = len(statuses) - success_count
    
    # Print results
    print("\n=== Load Test Results ===")
    print(f"Total Requests: {len(results)}")
    print(f"Success Rate: {success_count/len(results)*100:.2f}% ({success_count}/{len(results)})")
    print(f"Average Response Time: {avg_time:.4f} seconds")
    print(f"Median Response Time: {median_time:.4f} seconds")
    print(f"Min Response Time: {min_time:.4f} seconds")
    print(f"Max Response Time: {max_time:.4f} seconds")
    print(f"95th Percentile Response Time: {p95_time:.4f} seconds")
    
    # Count status codes
    status_counts = {}
    for status in statuses:
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nStatus Code Distribution:")
    for status, count in status_counts.items():
        print(f"  {status}: {count} ({count/len(results)*100:.2f}%)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load test the JobSpy Docker API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    parser.add_argument("--api-key", required=True, help="API key for authentication")
    parser.add_argument("--requests", type=int, default=10, help="Total number of requests to make")
    parser.add_argument("--concurrency", type=int, default=2, help="Number of concurrent requests")
    args = parser.parse_args()
    
    results = asyncio.run(run_load_test(args.url, args.api_key, args.requests, args.concurrency))
    analyze_results(results)
