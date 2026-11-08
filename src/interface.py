import gradio as gr

from chat_service import get_answer


APP_CSS = """
.gradio-container {
    max-width: 1080px !important;
    margin: 0 auto !important;
}

.hero {
    margin: 22px auto 14px;
    padding: 30px 34px;
    border-radius: 24px;
    color: white;
    background: linear-gradient(120deg, #5546d7 0%, #7865e8 55%, #4e9de0 100%);
    box-shadow: 0 14px 34px rgba(77, 72, 170, 0.2);
}

.hero-tag {
    margin: 0 0 8px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    opacity: 0.85;
}

.hero h1 {
    margin: 0 0 8px;
    font-size: 34px;
    line-height: 1.2;
}

.hero p {
    margin: 0;
    font-size: 16px;
    opacity: 0.92;
}

.footer-note {
    padding: 8px 4px 18px;
    color: #77758b;
    text-align: center;
    font-size: 13px;
}

@media (max-width: 600px) {
    .hero { padding: 24px; border-radius: 18px; }
    .hero h1 { font-size: 28px; }
}
"""


def build_interface():
    with gr.Blocks(
        title="Алиса — AI-помощник",
        theme=gr.themes.Soft(primary_hue="violet", secondary_hue="blue"),
        css=APP_CSS,
    ) as app:
        gr.HTML(
            """
            <header class="hero">
                <div class="hero-tag">Ваш учебный AI-помощник</div>
                <h1>✨ Привет! Я Алиса</h1>
                <p>Задайте вопрос, попросите объяснить тему или просто начните разговор.</p>
            </header>
            """
        )

        gr.ChatInterface(
            fn=get_answer,
            chatbot=gr.Chatbot(
                height=440,
                placeholder="<div style='text-align:center'>Напишите сообщение, чтобы начать беседу </div>",
            ),
            textbox=gr.Textbox(
                placeholder="Напишите сообщение и нажмите Enter…",
                label="Ваше сообщение",
                lines=1,
                max_lines=5,
                max_length=1000,
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

        gr.HTML(
            "<div class='footer-note'>Алиса может ошибаться — проверяйте важную информацию.</div>"
        )

    return app



# import gradio as gr

# from chat_service import get_answer


# def build_interface():
#     return gr.ChatInterface(
#         fn=get_answer,
#         title="Помощник Алиса",
#         description="Задайте вопрос — Алиса постарается помочь.",
#         textbox=gr.Textbox(
#             placeholder="Напишите сообщение и нажмите Enter",
#             label="Сообщение",
#         ),
#         additional_inputs=gr.Dropdown(
#             choices=["Русский", "English"],
#             value="Русский",
#             label="Язык ответа",
#         ),
#     )