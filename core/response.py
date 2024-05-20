class Response:
    def __init__(self, model=None, message=None, errors=None):
        self.model = model
        self.message = message
        self.errors = errors

    def to_dict(self):
        return {
            "model": self.model,
            "message": self.message,
            "errors": self.errors
        }
