"""
Aucun test de ce fichier n'appelle l'API Anthropic : le client est un faux objet,
construit à la main, qui rejoue des réponses déjà connues.
"""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from extractor.extract import extract
from extractor.models import JobOffer

VALID = {
    "title": "Ingénieur ML",
    "company": None,
    "location": "Lyon",
    "salary": "45000-55000 EUR",
    "skills": ["Python", "PyTorch"],
    "contract_type": "CDI",
}


def _invalid_offer_error() -> ValidationError:
    """Une vraie ValidationError, obtenue en violant volontairement un validator."""
    try:
        JobOffer.model_validate({**VALID, "skills": []})
    except ValidationError as e:
        return e
    raise AssertionError("la construction aurait dû échouer")


class FakeMessages:
    """Rejoue une séquence de résultats : une exception ou un objet .parsed_output."""

    def __init__(self, results):
        self.results = list(results)
        self.calls = 0

    def parse(self, **kwargs):
        self.calls += 1
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return SimpleNamespace(parsed_output=result)


class FakeClient:
    def __init__(self, results):
        self.messages = FakeMessages(results)


def test_extract_succeeds_on_first_attempt_without_retry():
    good = JobOffer(**VALID)
    client = FakeClient([good])

    result = extract("peu importe", client=client, max_attempts=2)

    assert result == good
    assert client.messages.calls == 1  # pas de second appel si le premier réussit


def test_extract_retries_once_then_succeeds():
    good = JobOffer(**VALID)
    client = FakeClient([_invalid_offer_error(), good])

    result = extract("peu importe", client=client, max_attempts=2)

    assert result == good
    assert client.messages.calls == 2


def test_extract_raises_after_exhausting_attempts():
    client = FakeClient([_invalid_offer_error(), _invalid_offer_error()])

    with pytest.raises(ValueError):
        extract("peu importe", client=client, max_attempts=2)

    assert client.messages.calls == 2
