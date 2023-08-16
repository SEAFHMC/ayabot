class CardMessage:
    def __init__(self) -> None:
        self.modules = []
        self.card = [
            {
                "type": "card",
                "theme": "secondary",
                "size": "lg",
                "modules": self.modules,
            }
        ]
        return

    def add_plain_text(self, content: str):
        self.modules.append(
            {"type": "section", "text": {"type": "plain-text", "content": content}}
        )

    def add_kmarkdown(self, content: str):
        self.modules.append(
            {"type": "section", "text": {"type": "kmarkdown", "content": content}}
        )

    def add_image(self, src: str):
        self.modules.append(
            {"type": "container", "elements": [{"type": "image", "src": src}]}
        )

    def add_video(self, title: str, src: str):
        self.modules.append({"type": "video", "title": title, "src": src})
