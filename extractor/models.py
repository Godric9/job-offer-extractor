from typing import Literal

from pydantic import BaseModel


class JobOffer(BaseModel):
    title : str
    company : str | None
    location : str
    salary : str | None
    skills : list[str]
    contract_type : Literal["CDI", "CDD", "stage", "alternance", "freelance", "autre"]

