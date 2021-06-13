from datetime import datetime, timezone

class Emotion(dict):
    def __init__(self, icon: str = None, emotion: str = None, context: str = None):
        self.icon = icon
        self.emotion = emotion
        self.context = context
        self.time = None

    def set_time(self):
        time =  datetime.now(tz=timezone.utc)
        self.time = time.strftime("%m-%d-%Y %H:%M:%S.%f")