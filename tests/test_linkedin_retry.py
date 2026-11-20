"""LinkedIn job-detail fetches must retry 429s, or jobs are saved without a description."""
import app.services.job_service  # noqa: F401  (applies the retry patch)
from jobspy.linkedin import LinkedIn


def test_linkedin_session_retries_429():
    r = LinkedIn().session.get_adapter("https://www.linkedin.com/jobs/view/1").max_retries
    assert r.total == 3 and 429 in r.status_forcelist
