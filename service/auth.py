import jwt
import datetime
import calendar

from constants import SECRET_KEY, ALGORITHM


class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refrash=False):
        user = self.user_service.get_user_by_username(username)

        if not user:
            raise Exception()

        if not is_refrash:
            if not self.user_service.compare_passwords(user.password, password):
                raise Exception()

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(days130.timetuple())
        refrash_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'refrash_token': refrash_token,
        }

    def approve_refrash_token(self, refrash_token):
        data = jwt.decode(jwt=refrash_token, key=SECRET_KEY, algorithm=ALGORITHM)
        username = data['username']

        user = self.user_service.get_user_by_username(username)

        if not user:
            raise Exception()
        return self.generate_tokens(user.username, user.password, is_refrash=True)
