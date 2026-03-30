import os
import json
from datetime import datetime

from models import RankedCandidate, ShortlistReport
from config import OUTPUT_FOLDER
from logger import logger


def build_report(ranked_candidates: list[RankedCandidate], job_title: str) -> ShortlistReport:
    shortlisted_count = sum(1 for c in ranked_candidates if c.shortlisted)

    report = ShortlistReport(
        job_title=job_title,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_screened=len(ranked_candidates),
        total_shortlisted=shortlisted_count,
        candidates=ranked_candidates,
    )

    return report


def save_report(report: ShortlistReport):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"shortlist_report_{timestamp}.txt"
    filepath  = os.path.join(OUTPUT_FOLDER, filename)

    sorted_candidates = sorted(report.candidates, key=lambda c: c.score, reverse=True)

    lines = []
    lines.append("AI Job screening portal - Shortlist report")
    lines.append(f"Job Title: {report.job_title}")
    lines.append(f"Generated At: {report.generated_at}")
    lines.append(f"Total Screened: {report.total_screened}")
    lines.append(f"Total Shortlisted: {report.total_shortlisted}")
    lines.append(f"Average Score: {report.average_score} / 10")

    lines.append("\n All candidates (sorted by score) \n")

    for c in sorted_candidates:
        lines.append(f"Name: {c.profile.full_name}")
        lines.append(f"Email: {c.profile.email}")
        lines.append(f"Experience: {c.profile.total_experience} years")
        lines.append(f"Skills: {', '.join(c.profile.skills)}")
        lines.append(f"Score: {c.score} / 10  ({c.score_label})")
        lines.append(f"Shortlisted: {'YES' if c.shortlisted else 'NO'}")
        lines.append(f"Reasoning: {c.reasoning}")

    lines.append("\n Shortlisted Candidates \n")

    for c in report.shortlisted_candidates:
        lines.append(f"  {c.profile.full_name:30s}  Score: {c.score}  ->  {c.profile.email}")

    with open(filepath, "w") as f:
        f.write("\n".join(lines))

    logger.info(f"Report saved to: {filepath}")

    json_path = filepath.replace(".txt", ".json")
    with open(json_path, "w") as f:
        f.write(report.model_dump_json(indent=2))

    logger.info(f"JSON report saved to: {json_path}")

    return filepath