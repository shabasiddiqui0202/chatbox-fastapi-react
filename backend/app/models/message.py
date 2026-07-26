from datetime import datetime
class Message:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text
        self.time = datetime.now()
    def to_dict(self):
        return {"sender": self.sender, "text": self.text, "time": self.time}
