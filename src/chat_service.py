import logging
import os

import requests


API_URL = "https://ai.api.cloud.yandex.net/v1/responses"
MODEL = os.getenv("YANDEX_MODEL", "deepseek-v4.1-flash")
SYSTEM_PROMPT = "Ты — искусственный интеллект, который помогает людям. Пиши ответы обычным текстом, без форматирования и разметки. Не используй HTML, Markdown, LaTeX или другие форматы. Не добавляй эмодзи в ответы."
logger = logging.getLogger(__name__)


def get_settings():
    api_key = os.getenv("YANDEX_API_KEY")
    folder_id = os.getenv("YANDEX_FOLDER_ID")

    if not api_key:
        raise RuntimeError("Не задан ключ YANDEX_API_KEY.")
    if not folder_id:
        raise RuntimeError("Не задан идентификатор каталога YANDEX_FOLDER_ID.")

    return api_key, folder_id


def _text_content(content):
    """Преобразует строку или список текстовых блоков Gradio в обычный текст."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                parts.append(block["text"])
        return "\n".join(parts)

    return ""


def make_input(message, history):
    items = []

    for item in history or []:
        role = item.get("role")
        content = _text_content(item.get("content", ""))

        if role in {"user", "assistant"} and content.strip():
            items.append({"role": role, "content": content})

    items.append({"role": "user", "content": message})
    return items


def get_answer(message, history, language):
    try:
        api_key, folder_id = get_settings()
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Api-Key {api_key}",
                "OpenAI-Project": folder_id,
                "Content-Type": "application/json",
            },
            json={
                "model": f"gpt://{folder_id}/{MODEL}/latest",
                "instructions": f"{SYSTEM_PROMPT}, язык ответа: {language}",
                "input": make_input(message, history),
                "temperature": 0,
                "max_output_tokens": 4096,
                "truncation": "auto",
                "store": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data.get("output_text"), str):
            return data["output_text"]

        for item in data.get("output", []):
            for content in item.get("content", []):
                if content.get("type") == "output_text":
                    return content.get("text", "")

        raise RuntimeError("Yandex API вернул ответ без текста.")
    except Exception:
        logger.exception("Не удалось получить ответ от Yandex Cloud")
        return "Не удалось получить ответ. Проверьте подключение и настройки сервера."
