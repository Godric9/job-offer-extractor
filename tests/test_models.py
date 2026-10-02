import pytest
from pydantic import ValidationError

from extractor.models import JobOffer

VALID = {
    "title": "Ingénieur ML",
    "company": None,
    "location": "Lyon",
    "salary": "45000-55000 EUR",
    "skills": ["Python", "PyTorch"],
    "contract_type": "CDI",
}


def test_valid_offer_passes():
    offer = JobOffer(**VALID)
    assert offer.salary == "45000-55000 EUR"


def test_salary_none_passes():
    offer = JobOffer(**{**VALID, "salary": None})
    assert offer.salary is None


def test_salary_without_digit_rejected():
    with pytest.raises(ValidationError):
        JobOffer(**{**VALID, "salary": "selon profil"})


def test_skills_empty_rejected():
    with pytest.raises(ValidationError):
        JobOffer(**{**VALID, "skills": []})


def test_contract_type_must_be_in_literal():
    with pytest.raises(ValidationError):
        JobOffer(**{**VALID, "contract_type": "CDI à vie"})
