import gradio as gr

from chat_service import get_answer


APP_THEME = gr.themes.Base(primary_hue="slate", radius_size="sm")

APP_CSS = """
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
}

.page-header {
    padding: 16px 0 8px;
    border-bottom: 1px solid #d1d5db;
}

.page-header h1 {
    margin: 0 0 8px;
}

.page-header p {
    margin: 0 0 12px;
}

.footer-note {
    padding: 8px 0;
    font-size: 13px;
}

.submit-button {
    width: 40px !important;
    min-width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    border-radius: 2px !important;
}

@media (max-width: 600px) {
    .gradio-container {
        width: 100% !important;
        padding: 0 12px !important;
    }

    .page-header {
        padding: 12px 0 6px;
    }

    .page-header h1 {
        font-size: 26px;
    }

    .page-header p {
        font-size: 14px;
    }

    .chatbot {
        min-height: 55vh !important;
    }

    .footer-note {
        font-size: 12px;
    }
}
"""


def build_interface():
    with gr.Blocks(
        title="Ассистент — учебный помощник",
    ) as app:
        gr.Markdown(
            "# Ассистент\nЗадайте вопрос или попросите объяснить тему.",
            elem_classes="page-header",
        )

        gr.ChatInterface(
            fn=get_answer,
            chatbot=gr.Chatbot(
                height=440,
                elem_classes="chatbot",
                placeholder="Напишите сообщение, чтобы начать беседу.",
            ),
            textbox=gr.Textbox(
                placeholder="Напишите сообщение и нажмите Enter",
                label="Ваше сообщение",
                lines=1,
                max_lines=5,
                max_length=1000,
                submit_btn=True,
            ),
            additional_inputs=gr.Dropdown(
                choices=["Русский", "English"],
                value="Русский",
                label="Язык ответа",
            ),
            examples=[
                ["Объясни простыми словами, что такое нейросеть", "Русский"],
                ["Give me a fun fact about space", "English"],
            ],
        )

        gr.Markdown(
            "Ассистент может ошибаться — проверяйте важную информацию.",
            elem_classes="footer-note",
        )

    return app
