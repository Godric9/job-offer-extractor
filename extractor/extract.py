import os
import json

from models import JobOffer
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

def raw(offer : str) -> str:
    schema = json.dumps(JobOffer.model_json_schema(), indent=4, ensure_ascii=False)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": (
                    "Extract the key information from this job offer: "
                    f'{offer}. '
                    f"The output should be a JSON object that conforms to the following schema: {schema}"
                )
            }

        ],
    )
    return response.content[0].text


if __name__ == "__main__":
    exmple = """
            Nous recherchons un Ingénieur Machine Learning (H/F) pour rejoindre notre équipe à
            Lyon. CDI, démarrage dès que possible. Rémunération entre 45 000 et 55 000 € selon
            profil. Vous maîtrisez Python, PyTorch et avez une expérience du déploiement en
            production (Docker, CI/CD).
            """
    print(raw(exmple))


    
    