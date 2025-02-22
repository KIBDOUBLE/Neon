class Config:
    def __init__(self):
        self.debug = False
        self.only_return_results = False
        self.explain_mode = False
        self.hello_message = True
        self.build_args = ""

    def info(self) -> str: return f"debug={self.debug}, only_return_results={self.only_return_results}, explain_mode={self.explain_mode}, hello_message={self.hello_message}"
