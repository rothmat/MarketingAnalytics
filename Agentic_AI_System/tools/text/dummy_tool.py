class DummyTool:
    name = "dummy_tool"
    description = "Ein Testtool, das einfach Text bestätigt."

    def run(self, input_text: str) -> str:
        return f"📦 DummyTool hat folgende Eingabe erhalten: '{input_text}'"
