import argparse
import os
import sys

from .extract import client, extract, raw
from .models import JobOffer


def _read_input(arg: str) -> str:
    """Si arg est un chemin de fichier lisible, renvoie son contenu. Sinon, arg est le texte."""
    if os.path.isfile(arg):
        with open(arg, encoding="utf-8") as f:
            return f.read()
    return arg


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="extractor")
    parser.add_argument("source", help="chemin de fichier ou texte de l'annonce")
    parser.add_argument("--raw", action="store_true", help="affiche la sortie brute, sans validation")

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Erreur : ANTHROPIC_API_KEY absente. Vérifie ton .env.", file=sys.stderr)
        return 3

    text = _read_input(args.source)

    if args.raw:
        print(raw(text))
        return 0

    try:
        offer: JobOffer = extract(text, client=client)
    except ValueError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1

    print(offer.model_dump_json(indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
