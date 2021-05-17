from datetime import datetime, timezone
class UserEmotionAtCheckIn:

    def __init__(self, icon: str = None, emotion: str = None, context: str = None):
        self.icon = icon
        self.emotion = emotion
        self.context = context
        self.time = None
        self.user = None

    def set_user(self, user):
        self.user = user

    def update_timestamp(self):
        self.time = datetime.now(tz=timezone.utc)

    def set_time(self, updated_time):
        self.time = updated_time