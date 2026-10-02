"""
Teste les codes de retour de la CLI. `extract` et `raw` sont remplacés par de faux
objets : aucun de ces tests n'appelle l'API Anthropic.
"""

from extractor import __main__ as cli
from extractor.models import JobOffer

VALID = {
    "title": "Ingénieur ML",
    "company": None,
    "location": "Lyon",
    "salary": "45000-55000 EUR",
    "skills": ["Python", "PyTorch"],
    "contract_type": "CDI",
}


def test_invalid_arguments_return_2():
    assert cli.main(["--toto"]) == 2
    assert cli.main([]) == 2


def test_missing_api_key_returns_3(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert cli.main(["un texte quelconque"]) == 3


def test_successful_extraction_returns_0(monkeypatch, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(cli, "extract", lambda text, client=None: JobOffer(**VALID))

    code = cli.main(["une annonce quelconque"])

    assert code == 0
    assert '"title": "Ingénieur ML"' in capsys.readouterr().out


def test_extraction_failure_returns_1(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")

    def _always_fails(text, client=None):
        raise ValueError("cannot obtain de correct json/informations")

    monkeypatch.setattr(cli, "extract", _always_fails)

    assert cli.main(["un texte qui ne donnera jamais une offre valide"]) == 1


def test_raw_mode_skips_validation(monkeypatch, capsys):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-test")
    monkeypatch.setattr(cli, "raw", lambda text: '{"title": "brut"}')

    code = cli.main(["--raw", "un texte"])

    assert code == 0
    assert capsys.readouterr().out.strip() == '{"title": "brut"}'
