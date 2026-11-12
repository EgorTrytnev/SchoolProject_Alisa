import logging
import os

import requests


MODEL = "deepseek-v4.1-flash:free"
API_URL = "https://tokenharbor.ai/v1/chat/completions"
SYSTEM_PROMPT = "Ты — искусственный интеллект, который помогает людям. Пиши ответы обычным текстом, без форматирования и разметки. Не используй HTML, Markdown, LaTeX или другие форматы. Не добавляй эмодзи в ответы."
logger = logging.getLogger(__name__)


def get_api_key():
    api_key = os.getenv("TOKENHARBOR_API_KEY")
    if not api_key:
        raise RuntimeError("Не задан ключ TOKENHARBOR_API_KEY.")
    return api_key


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


def make_messages(message, history, language):
    messages = [
        {
            "role": "system",
            "content": f"{SYSTEM_PROMPT}, язык ответа: {language}",
        }
    ]

    for item in history or []:
        role = item.get("role")
        content = _text_content(item.get("content", ""))

        if role in {"user", "assistant"} and content.strip():
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": message})
    return messages


def get_answer(message, history, language):
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {get_api_key()}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": make_messages(message, history, language),
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        logger.exception("Не удалось получить ответ от TokenHarbor")
        return "Не удалось получить ответ. Проверьте подключение и настройки сервера."
