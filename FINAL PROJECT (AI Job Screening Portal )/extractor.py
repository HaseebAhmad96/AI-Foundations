from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

from config import GROQ_API_KEY, EXTRACTION_MODEL, TEMPERATURE, MAX_TOKENS
from models import CandidateProfile
from logger import logger


llm = ChatGroq( api_key=GROQ_API_KEY, model=EXTRACTION_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS, )

parser = PydanticOutputParser(pydantic_object=CandidateProfile)

prompt = PromptTemplate(
    template=(
        "You are a CV parser. Extract structured information from the CV text below.\n\n"
        "{format_instructions}\n\n"
        "CV Text:\n{cv_text}"
    ),
    input_variables=["cv_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser


def extract_profile(cv_text: str, filename: str) -> CandidateProfile | None:
    logger.info(f"Extracting profile from: {filename}")

    try:
        profile = chain.invoke({"cv_text": cv_text})
        logger.info(f"Extracted: {profile.full_name}")
        return profile

    except Exception as e:
        logger.error(f"Extraction failed for {filename}: {e}")
        return None