"""Utility functions for parameter validation and providing helpful error messages."""
from typing import Any, Dict, List, Tuple

# Define valid values for different parameters
VALID_PARAMETERS = {
    "site_name": ["indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"],
    "job_type": ["fulltime", "parttime", "internship", "contract"],
    "description_format": ["markdown", "html"],
    "verbose": [0, 1, 2],
    "page_size": list(range(1, 101)),
    "paginate": [True, False],
}

# Define parameter type information to improve error messages
PARAMETER_TYPES = {
    "site_name": "string or list",
    "search_term": "string",
    "location": "string",
    "distance": "integer",
    "job_type": "string",
    "is_remote": "boolean",
    "results_wanted": "integer",
    "hours_old": "integer",
    "linkedin_fetch_description": "boolean",
    "linkedin_company_ids": "list of integers",
    "country_indeed": "string",
    "enforce_annual_salary": "boolean",
    "description_format": "string",
    "offset": "integer",
    "easy_apply": "boolean",
    "page": "integer",
    "page_size": "integer",
    "paginate": "boolean",
}

# Parameter descriptions for helpful error messages
PARAMETER_DESCRIPTIONS = {
    "site_name": "Job sites to search on (e.g., indeed, linkedin)",
    "search_term": "Job search term (e.g., 'software engineer')",
    "location": "Job location (e.g., 'San Francisco, CA')",
    "distance": "Distance in miles (default: 50)",
    "job_type": "Type of job (e.g., fulltime, parttime)",
    "is_remote": "Whether to include remote jobs (true or false)",
    "results_wanted": "Number of job results per site",
    "hours_old": "Filter jobs by hours since posting",
    "linkedin_fetch_description": "Fetch full LinkedIn descriptions",
    "linkedin_company_ids": "LinkedIn company IDs to filter by",
    "country_indeed": "Country filter for Indeed & Glassdoor",
    "enforce_annual_salary": "Convert wages to annual salary",
    "description_format": "Format of job description (markdown, html)",
    "offset": "Offset for pagination",
    "easy_apply": "Filter for easy apply jobs",
    "page": "Page number for paginated results",
    "page_size": "Number of results per page",
    "paginate": "Enable pagination",
}

# Parameter limitations and notes
PARAMETER_LIMITATIONS = {
    "hours_old": "Cannot be used with job_type, is_remote, or easy_apply for Indeed searches",
    "easy_apply": "Cannot be used with hours_old for LinkedIn and Indeed searches",
    "job_type": "Cannot be used with hours_old for Indeed searches when combined with is_remote",
    "page_size": "Must be between 1 and 100",
}

def get_parameter_suggestion(param_name: str, invalid_value: Any = None) -> Dict[str, Any]:
    """Generate helpful suggestions for invalid parameters."""
    suggestion = {
        "parameter": param_name,
        "message": f"Invalid value for {param_name}",
    }
    
    # Add information about the parameter type
    if param_name in PARAMETER_TYPES:
        suggestion["expected_type"] = PARAMETER_TYPES[param_name]
    
    # Add description if available
    if param_name in PARAMETER_DESCRIPTIONS:
        suggestion["description"] = PARAMETER_DESCRIPTIONS[param_name]
    
    # Add valid values if available
    if param_name in VALID_PARAMETERS:
        suggestion["valid_values"] = VALID_PARAMETERS[param_name]
    
    # Add limitations if applicable
    if param_name in PARAMETER_LIMITATIONS:
        suggestion["limitation"] = PARAMETER_LIMITATIONS[param_name]
    
    # Add specific suggestions based on the parameter
    if param_name == "site_name" and invalid_value:
        suggestion["message"] = f"'{invalid_value}' is not a valid job site"
        suggestion["suggestion"] = f"Use one or more of the valid job sites: {', '.join(VALID_PARAMETERS['site_name'])}"
    elif param_name == "job_type" and invalid_value:
        suggestion["message"] = f"'{invalid_value}' is not a valid job type"
        suggestion["suggestion"] = f"Use one of: {', '.join(VALID_PARAMETERS['job_type'])}"
    elif param_name == "description_format" and invalid_value:
        suggestion["message"] = f"'{invalid_value}' is not a valid description format"
        suggestion["suggestion"] = f"Use one of: {', '.join(VALID_PARAMETERS['description_format'])}"
    elif param_name == "verbose" and invalid_value is not None:
        suggestion["message"] = f"'{invalid_value}' is not a valid verbosity level"
        suggestion["suggestion"] = f"Use one of: {', '.join(map(str, VALID_PARAMETERS['verbose']))}"
    elif param_name == "page_size" and invalid_value is not None:
        suggestion["message"] = f"'{invalid_value}' is not a valid page size"
        suggestion["suggestion"] = "Page size must be between 1 and 100"
    elif param_name == "paginate" and invalid_value is not None:
        suggestion["message"] = f"'{invalid_value}' is not a valid value for paginate"
        suggestion["suggestion"] = "Use true or false"
    
    return suggestion

def extract_validation_location(error_location: Tuple) -> str:
    """Extract the parameter name from the error location tuple."""
    if len(error_location) > 1:
        return error_location[1]
    return str(error_location[0])

def generate_error_suggestions(validation_errors: List[Dict]) -> List[Dict]:
    """Generate helpful suggestions for validation errors."""
    suggestions = []
    
    for error in validation_errors:
        error_type = error.get("type", "")
        error_loc = error.get("location", [])
        
        if not error_loc:
            continue
            
        param_name = extract_validation_location(error_loc)
        invalid_value = None
        
        # For value errors, extract the invalid value if possible
        if "value_error" in error_type and "msg" in error:
            # Try to extract the invalid value from the error message
            msg = error["message"]
            if "not a valid" in msg and "=" in msg:
                invalid_value = msg.split("=")[-1].strip().strip("'\"")
        
        suggestion = get_parameter_suggestion(param_name, invalid_value)
        suggestions.append(suggestion)
    
    return suggestions
