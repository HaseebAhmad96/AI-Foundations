import os

from config import CV_FOLDER, JOB_DESC_FILE
from models import RankedCandidate
from safety import is_safe
from extractor import extract_profile
from ranker import rank_candidate
from report import build_report, save_report
from logger import logger


def load_job_description() -> tuple[str, str]:
    with open(JOB_DESC_FILE, "r") as f:
        content = f.read()

    job_title = "Unknown Position"
    for line in content.splitlines():
        if line.lower().startswith("job title"):
            job_title = line.split(":", 1)[-1].strip()
            break

    return content, job_title


def load_cv_files() -> list[tuple[str, str]]:
    cv_files = []
    for filename in os.listdir(CV_FOLDER):
        if filename.endswith(".txt"):
            filepath = os.path.join(CV_FOLDER, filename)
            with open(filepath, "r") as f:
                text = f.read()
            cv_files.append((filename, text))
    return cv_files


def process_single_cv(args: dict) -> RankedCandidate | None:
    filename = args["filename"]
    cv_text = args["cv_text"]
    job_description = args["job_description"]

    if not is_safe(cv_text):
        logger.warning(f"Unsafe content detected in {filename} - skipping.")
        return None

    profile = extract_profile(cv_text, filename)
    if profile is None:
        return None

    ranked = rank_candidate(profile, job_description)
    return ranked


def run():
    logger.info("AI Job Screening Portal - Starting")

    job_description, job_title = load_job_description()
    logger.info(f"Job Title: {job_title}")

    cv_files = load_cv_files()
    logger.info(f"Found {len(cv_files)} CV(s) to process")

    ranked_candidates = []

    for filename, cv_text in cv_files:
        result = process_single_cv({
            "filename": filename,
            "cv_text": cv_text,
            "job_description": job_description,
        })
        if result is not None:
            ranked_candidates.append(result)

    if not ranked_candidates:
        logger.error("No candidates were successfully processed.")
        return

    report = build_report(ranked_candidates, job_title)
    filepath = save_report(report)

    logger.info(f"Screening complete.")
    logger.info(f"Screened: {report.total_screened}")
    logger.info(f"Shortlisted: {report.total_shortlisted}")
    logger.info(f"Avg Score: {report.average_score} / 10")
    logger.info(f"Report: {filepath}")