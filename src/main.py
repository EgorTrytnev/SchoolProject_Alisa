import os

from interface import APP_CSS, APP_THEME, build_interface


if __name__ == "__main__":
    app = build_interface()
    app.launch(
        server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
        theme=APP_THEME,
        css=APP_CSS,
    )
