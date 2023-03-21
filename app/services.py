import openai
import json
from pathlib import Path
from requests.exceptions import ReadTimeout
from openai.error import RateLimitError, InvalidRequestError
from django.conf import settings


openai.api_key = settings.OPENAI_TOKEN
engine = "text-davinci-003"


def check_length(answer, list_of_answers):
    if len(answer) > 4090 and len(answer) < 409000:
        list_of_answers.append(answer[0:4090] + "...")
        check_length(answer[4091:], list_of_answers)
    else:
        list_of_answers.append(answer[0:])
        return list_of_answers


def send_request(messages_list: list):
    try:
        messages = [
            {"role": "system", "content": "Ты AikoGPT, используешь ChatGPT для того чтобы поомгать людям с их вопросами"}
        ]

        for msg in messages_list:
            messages.append(msg)

        return openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

    except (RateLimitError, ReadTimeout):
        return -1
    except InvalidRequestError:
        return -2


def get_user_history_dialog(user_id):
    try:
        with open(settings.BASE_DIR + f"/users/{user_id}.json", "r") as json_file:
            try:
                return json.load(json_file).get("history", [])
            except Exception as ex:
                return []
    except:
        with open(settings.BASE_DIR + f"/users/{user_id}.json", "w+") as json_file:
            try:
                return json.load(json_file).get("history", [])
            except Exception as ex:
                return []

def update_user_history_dialog(user_id, messages):
    json_output = {
        "history": messages
    }

    with open(settings.BASE_DIR + f"/users/{user_id}.json", "w+") as json_file:
        json_file.write(json.dumps(json_output))

