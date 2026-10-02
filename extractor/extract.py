import json
import os

from anthropic import Anthropic, APIResponseValidationError
from dotenv import load_dotenv

from .models import JobOffer

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

def structured(offer : str) -> JobOffer:
    schema = json.dumps(JobOffer.model_json_schema(), indent=4, ensure_ascii=False)
    response = client.messages.parse(
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
            output_format=JobOffer
        )
    return response.parsed_output

def extract(text: str, client: Anthropic | None = None, max_attempts: int = 2) -> JobOffer:
    schema = json.dumps(JobOffer.model_json_schema(), indent=4, ensure_ascii=False)
    messages=[
                                {
                                    "role": "user",
                                    "content": (
                                        "Extract the key information from this job offer: "
                                        f'{text}. '
                                        f"The output should be a JSON object that conforms to the following schema: {schema}"
                                    )
                                }
                    
                            ]
    for attempt in range(max_attempts):
        try:
            response = client.messages.parse(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=1024,
                        messages=messages,
                        output_format=JobOffer
                    )
            return response.parsed_output
        except (APIResponseValidationError, ValueError) as error:
            if attempt == max_attempts - 1:
                raise ValueError("cannot obtain de correct json/informations")

            messages.append({
                "role": "user",
                "content": f"Votre réponse précédente a échoué à la validation avec l'erreur suivante : {error.json()}. Veuillez corriger le JSON en respectant strictement le schéma requis."
            })
    return response.parsed_output
    
    
    

if __name__ == "__main__":
    exmple = """
            Nous recherchons quelqu'un (H/F) pour rejoindre notre équipe à
            Lyon. CDI, démarrage dès que possible. Rémunération selon
            profil. 
            """
    print(extract(text=exmple, client=client, max_attempts=2))


    
    