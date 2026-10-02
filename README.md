# Job Offer Extractor

This project is a tool for extracting structured information from job offers. It uses the Anthropic API to process job offer text and extract relevant details such as job title, company name, location, salary, and more.

The purpose of this project was to learn how to use the Anthropic API and pydantic for data validation. It is not intended for production use and should be used with caution.


## Installation

1. Clone the repository:
    ```bash
    git clone git@github.com:Godric9/job-offer-extractor.git
    cd job-offer-extractor
    ```
2. Install dependencies (creates the `.venv` automatically):
    ```bash
    uv sync
    ```
3. Set up your API key:
    ```bash
    cp .env.example .env
    # then edit .env and paste your ANTHROPIC_API_KEY
    ```

## What I learned

How to use pydantic to define the shape a job offer extraction must have, and to reject a response that doesn't match it, even if the JSON itself is syntactically valid.

The model can find values for fields that we don't want or not in the right format. For example, if we ask for a salary, the model can return a string like "depending on experience", wich is not a valid salary. And pydantic enters here to reject this value and raise a validation error thanks to the `validate` method.

Sometimes the model will not find a value for a field, or will return a value that is not valid/that doesn't match the expected format. In these cases, we will loop and ask the model to try again with error messages and hints to help it find the right value. It will stop if it finds a valid value or if it reaches the maximum number of attempts.

And lastly, you need to explicitly put an argument `client` for your function, because if you want to test it in unit tests, you don't want to call the real API, you can just create a fake client that outputs what you want and just test your function and not the API itself.