import os
import json
import openai
from logging import getLogger, INFO, StreamHandler

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
logger.propagate = False

openai.api_key = os.getenv("OPENAI_API_KEY")

def list_model():
    logger.info(openai.Model.list())

def completion_davinci():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Say this is a test",
        max_tokens=7,
        temperature=0
    )
    logger.info(response)


def completion_gpt(message_content="Say this is a test"):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message_content}
        ]
    )

    logger.info(response.choices[0].message.content)

def main():
    completion_gpt()

if __name__ == "__main__":
    main()
