from datetime import datetime, timezone
class UserEmotionAtCheckIn:

    def __init__(self):
        self.time_of_last_checkin = None
        self.name = None
        self.userid = None
        self.emotions = [] # this will be a list of dict, each emotion will be it's own dict
        self.daily_checkin_time = None

    def set_username(self, user):
        self.name = user

    def set_userid(self, userid):
        self.userid = userid

    def add_emotion(self, emotion):
       self.emotions.append(vars(emotion))
       self.time_of_last_checkin = emotion.time

    def get_emotions(self):
        return self.emotions

