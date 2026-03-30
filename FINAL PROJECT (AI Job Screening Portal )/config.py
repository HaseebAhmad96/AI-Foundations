import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

EXTRACTION_MODEL = "llama-3.3-70b-versatile"   
RANKING_MODEL = "llama-3.1-8b-instant"               
SAFETY_MODEL = "llama-3.1-8b-instant"         

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_FOLDER = os.path.join(BASE_DIR,"inputs","cvs")
JOB_DESC_FILE = os.path.join(BASE_DIR,"inputs","job_description.txt")
OUTPUT_FOLDER = os.path.join(BASE_DIR,"outputs")
LOG_FILE = os.path.join(BASE_DIR,"outputs","activity.log")

TEMPERATURE = 0
MAX_TOKENS = 1024