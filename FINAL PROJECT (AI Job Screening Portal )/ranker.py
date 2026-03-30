from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSequence

from config import GROQ_API_KEY, RANKING_MODEL, TEMPERATURE, MAX_TOKENS
from models import CandidateProfile, RankedCandidate
from logger import logger

import json


llm = ChatGroq( api_key=GROQ_API_KEY, model=RANKING_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, )

str_parser = StrOutputParser()


score_prompt = PromptTemplate(
    template=(
        "You are a senior technical recruiter.\n"
        "Score this candidate against the job description on a scale of 0 to 10.\n\n"
        "Job Description:\n{job_description}\n\n"
        "Candidate Profile:\n{candidate_summary}\n\n"
        "Think step by step:\n"
        "1. List matching skills\n"
        "2. Note missing requirements\n"
        "3. Consider years of experience\n"
        "4. Give a final score out of 10\n\n"
        "Reply in this exact JSON format:\n"
        "{{\n"
        '  "score": <number between 0 and 10>,\n'
        '  "reasoning": "<one paragraph explanation>"\n'
        "}}"
    ),
    input_variables=["job_description", "candidate_summary"],
)


def parse_score_output(raw_text: str) -> dict:
    start = raw_text.find("{")
    end   = raw_text.rfind("}") + 1
    json_str = raw_text[start:end]
    return json.loads(json_str)


score_chain = RunnableSequence( score_prompt, llm, str_parser, RunnableLambda(parse_score_output), )


def rank_candidate(profile: CandidateProfile, job_description: str) -> RankedCandidate | None:
    logger.info(f"Ranking candidate: {profile.full_name}")

    candidate_summary = (
        f"Name: {profile.full_name}\n"
        f"Experience: {profile.total_experience} years\n"
        f"Current Role: {profile.current_role}\n"
        f"Skills: {', '.join(profile.skills)}\n"
        f"Education: {profile.education}\n"
        f"Summary: {profile.summary}"
    )

    try:
        result = score_chain.invoke({
            "job_description":   job_description,
            "candidate_summary": candidate_summary,
        })

        ranked = RankedCandidate( profile=profile, score=float(result["score"]), reasoning=result["reasoning"], )

        logger.info(f"Score for {profile.full_name}: {ranked.score} - {ranked.score_label}")
        return ranked

    except Exception as e:
        logger.error(f"Ranking failed for {profile.full_name}: {e}")
        return None