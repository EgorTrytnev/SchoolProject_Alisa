import logging
import os

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama


MODEL = "gpt-oss:120b"
OLLAMA_URL = "https://ollama.com"
SYSTEM_PROMPT = "Ты — искусственный интеллект, который помогает людям. Пиши ответы обычным текстом, без форматирования и разметки. Не используй HTML, Markdown, LaTeX или другие форматы. Не добавляй эмодзи в ответы."
logger = logging.getLogger(__name__)


def create_model():
    api_key = os.getenv("OLLAMA_API_KEY")
    if not api_key:
        raise RuntimeError("Не задан ключ OLLAMA_API_KEY.")

    return ChatOllama(
        model=MODEL,
        base_url=OLLAMA_URL,
        client_kwargs={"headers": {"Authorization": f"Bearer {api_key}"}},
    )


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
    system_prompt = f"{SYSTEM_PROMPT}, язык ответа: {language}"
    messages = [SystemMessage(content=system_prompt)]



    for item in history or []:
        role = item.get("role")
        content = _text_content(item.get("content", ""))

        if not isinstance(content, str) or not content.strip():
            continue

        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=message))
    return messages


def get_answer(message, history, language):
    try:
        model = create_model()
        response = model.invoke(make_messages(message, history, language))
        return _text_content(response.content)
    except Exception:
        logger.exception("Не удалось получить ответ от Ollama")
        return "Не удалось получить ответ. Проверьте подключение и настройки сервера."
