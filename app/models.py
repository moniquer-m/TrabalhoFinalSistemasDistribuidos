from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    @staticmethod
    def get(user_id):
        from flask import current_app
        users = current_app.config['USERS']
        if user_id in users:
            user = User(user_id)
            return user
        return None