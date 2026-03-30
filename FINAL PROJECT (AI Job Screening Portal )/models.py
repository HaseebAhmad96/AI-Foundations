from typing import Optional
from pydantic import BaseModel, Field, field_validator, computed_field, model_validator
from typing import Literal


class CandidateProfile(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    total_experience: float  = Field(ge=0, description="Years of experience")
    skills: list[str]
    education: str
    current_role: Optional[str] = None
    summary: str

    @field_validator("full_name", "education", "summary", mode="before")
    @classmethod
    def strip_whitespace(cls, v):
        return v.strip()

    @field_validator("skills", mode="before")
    @classmethod
    def clean_skills(cls, v):
        return [skill.strip() for skill in v]

    @field_validator("email", mode="before")
    @classmethod
    def lowercase_email(cls, v):
        return v.strip().lower()


class RankedCandidate(BaseModel):
    profile: CandidateProfile
    score: float = Field(ge=0, le=10, description="Match score out of 10")
    reasoning: str
    shortlisted: bool = False

    @model_validator(mode="after")
    def auto_shortlist(self):
        if self.score >= 7.0:
            self.shortlisted = True
        return self

    @computed_field
    def score_label(self) -> str:
        if self.score >= 8:
            return "Strong Match"
        elif self.score >= 6:
            return "Moderate Match"
        else:
            return "Weak Match"


class ShortlistReport(BaseModel):
    job_title: str
    generated_at: str
    total_screened: int
    total_shortlisted: int
    candidates: list[RankedCandidate]

    @computed_field
    def shortlisted_candidates(self) -> list[RankedCandidate]:
        return [c for c in self.candidates if c.shortlisted]

    @computed_field
    def average_score(self) -> float:
        if not self.candidates:
            return 0.0
        total = sum(c.score for c in self.candidates)
        return round(total / len(self.candidates), 2)
