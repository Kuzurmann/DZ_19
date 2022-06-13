from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        users = User.query.all()
        return users

    def get_one(self, uid):
        users = User.query.get(uid)
        return users

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create_user(self, user):
        user_ent = User(**user)
        self.session.add(user_ent)
        self.session.commit()
        return user_ent

    def update(self, user):
        self.session.add(user)
        self.session.commit()
        self.session.close()

    def delete(self, user):
        self.session.delete(user)
        self.session.commit()
        self.session.close()
