from typing import Literal
from pydantic import BaseModel, field_validator, ValidationError


class JobOffer(BaseModel):
    title : str
    company : str | None
    location : str
    salary : str | None
    skills : list[str]
    contract_type : Literal["CDI", "CDD", "stage", "alternance", "freelance", "autre"]

    @field_validator('salary')
    @classmethod
    def is_salary_valid(cls, salary : str) -> str | None:
        if salary is not None:
            for c in range(ord("0"), ord("9") + 1):
                if chr(c) in salary:
                    return salary
            raise ValueError(f'{salary} is not a valid salary')
        return None

    @field_validator('skills')
    @classmethod
    def is_skills_valid(cls, skills : list[str]) -> list[str]:
        if skills is None or len(skills) <= 0:
            raise ValueError("Skills cannot be empty")
        return skills


if __name__ == "__main__":
    try:
        JobOffer(title="Engineer", company="Company", location="Location", salary="67", skills=[], contract_type="CDI")
    except ValueError as e:
        print(e)