from pymongo import MongoClient

class MongoConnection:
    def __init__(self):
        self.db = self.connect()

    def connect(self):
        client = MongoClient("mongodb://127.0.0.1:27017/")
        return client.emotionData

    def persist(self, user_data):
        user_exists = self.check_userid_exists(user_data.userid)
        if user_exists.retrieved != 0: # just want to append to the existing user
            return self.update_user(user_data)
        else: # new user, we want to create new db object
            return self.create_new_user(user_data)

    def update_user(self, user_data):
        query = {"userid": user_data.userid}
        update = {
            '$push':  {
                'emotions': user_data.get_emotions()
            }
        }
        return self.db.users.update_one(query, update)

    def create_new_user(self, user_data):
        user_data_dict = vars(user_data)
        return self.db.users.insert_one(user_data_dict)

    def check_userid_exists(self, userid):
        query = {"userid": userid}
        return self.db.users.find(query)
