from typing import List, Optional, Union, Dict, Any
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from jobspy import scrape_jobs
import pandas as pd

app = FastAPI(
    title="JobSpy Docker API",
    description="API for searching jobs across multiple platforms using JobSpy",
    version="1.0.0",
)

class JobSearchParams(BaseModel):
    site_name: Union[List[str], str] = Field(
        default=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"],
        description="Job sites to search on",
    )
    search_term: Optional[str] = Field(default=None, description="Job search term")
    google_search_term: Optional[str] = Field(default=None, description="Search term for Google jobs")
    location: Optional[str] = Field(default=None, description="Job location")
    distance: Optional[int] = Field(default=50, description="Distance in miles")
    job_type: Optional[str] = Field(default=None, description="Job type (fulltime, parttime, internship, contract)")
    proxies: Optional[List[str]] = Field(default=None, description="Proxies in format ['user:pass@host:port', 'localhost']")
    is_remote: Optional[bool] = Field(default=None, description="Remote job filter")
    results_wanted: Optional[int] = Field(default=20, description="Number of results per site")
    hours_old: Optional[int] = Field(default=None, description="Filter by hours since posting")
    easy_apply: Optional[bool] = Field(default=None, description="Filter for easy apply jobs")
    description_format: Optional[str] = Field(default="markdown", description="Format of job description")
    offset: Optional[int] = Field(default=0, description="Offset for pagination")
    verbose: Optional[int] = Field(default=2, description="Controls verbosity (0: errors only, 1: errors+warnings, 2: all logs)")
    linkedin_fetch_description: Optional[bool] = Field(default=False, description="Fetch full LinkedIn descriptions")
    linkedin_company_ids: Optional[List[int]] = Field(default=None, description="LinkedIn company IDs to filter by")
    country_indeed: Optional[str] = Field(default=None, description="Country filter for Indeed & Glassdoor")
    enforce_annual_salary: Optional[bool] = Field(default=False, description="Convert wages to annual salary")
    ca_cert: Optional[str] = Field(default=None, description="Path to CA Certificate file for proxies")

class JobResponse(BaseModel):
    count: int
    jobs: List[Dict[str, Any]]

@app.get("/", tags=["Info"])
def read_root():
    return {"message": "Welcome to JobSpy Docker API! Go to /docs for the API documentation."}

@app.post("/search_jobs", response_model=JobResponse, tags=["Jobs"])
def search_jobs(params: JobSearchParams):
    try:
        jobs_df = scrape_jobs(
            site_name=params.site_name,
            search_term=params.search_term,
            google_search_term=params.google_search_term,
            location=params.location,
            distance=params.distance,
            job_type=params.job_type,
            proxies=params.proxies,
            is_remote=params.is_remote,
            results_wanted=params.results_wanted,
            hours_old=params.hours_old,
            easy_apply=params.easy_apply,
            description_format=params.description_format,
            offset=params.offset,
            verbose=params.verbose,
            linkedin_fetch_description=params.linkedin_fetch_description,
            linkedin_company_ids=params.linkedin_company_ids,
            country_indeed=params.country_indeed,
            enforce_annual_salary=params.enforce_annual_salary,
            ca_cert=params.ca_cert,
        )
        
        # Convert DataFrame to dictionary format
        jobs_list = jobs_df.to_dict('records')
        
        return {
            "count": len(jobs_list),
            "jobs": jobs_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping jobs: {str(e)}")

@app.get("/search_jobs", response_model=JobResponse, tags=["Jobs"])
def search_jobs_get(
    site_name: List[str] = Query(["indeed", "linkedin", "zip_recruiter"], description="Job sites to search on"),
    search_term: str = Query(None, description="Job search term"),
    google_search_term: Optional[str] = Query(None, description="Search term for Google jobs"),
    location: str = Query(None, description="Job location"),
    distance: int = Query(50, description="Distance in miles"),
    job_type: Optional[str] = Query(None, description="Job type (fulltime, parttime, internship, contract)"),
    is_remote: Optional[bool] = Query(None, description="Remote job filter"),
    results_wanted: int = Query(10, description="Number of results per site"),
    hours_old: Optional[int] = Query(None, description="Filter by hours since posting"),
    easy_apply: Optional[bool] = Query(None, description="Filter for easy apply jobs"),
    description_format: str = Query("markdown", description="Format of job description"),
    offset: int = Query(0, description="Offset for pagination"),
    verbose: int = Query(2, description="Controls verbosity (0: errors only, 1: errors+warnings, 2: all logs)"),
    linkedin_fetch_description: bool = Query(False, description="Fetch full LinkedIn descriptions"),
    country_indeed: Optional[str] = Query(None, description="Country filter for Indeed & Glassdoor"),
    enforce_annual_salary: bool = Query(False, description="Convert wages to annual salary"),
):
    try:
        jobs_df = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            distance=distance,
            job_type=job_type,
            is_remote=is_remote,
            results_wanted=results_wanted,
            hours_old=hours_old,
            easy_apply=easy_apply,
            description_format=description_format,
            offset=offset,
            verbose=verbose,
            linkedin_fetch_description=linkedin_fetch_description,
            country_indeed=country_indeed,
            enforce_annual_salary=enforce_annual_salary,
            # Note: proxies, linkedin_company_ids, and ca_cert are omitted from GET request
            # for simplicity, use POST for these more complex parameters
        )
        
        # Convert DataFrame to dictionary format
        jobs_list = jobs_df.to_dict('records')
        
        return {
            "count": len(jobs_list),
            "jobs": jobs_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping jobs: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
