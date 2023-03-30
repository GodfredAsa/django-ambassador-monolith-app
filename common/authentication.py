import datetime
from rest_framework.authentication import BaseAuthentication
import jwt
from app import settings
from rest_framework.authentication import exceptions
from core.models import User


class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        is_ambassador = 'api/ambassador' in request.path
        token = request.COOKIES.get('jwt')
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Unauthenticated")

        if (is_ambassador and payload['scope'] != 'ambassador') or (not is_ambassador and payload['scope'] != 'admin'):
            raise exceptions.AuthenticationFailed('Invalid Scope')

        user = User.objects.get(pk=payload['user_id'])
        if user is None:
            raise exceptions.AuthenticationFailed("User Not Found")
        return user, None

    @staticmethod
    def generate_jwt_token(user_id, scope):
        payload = {
            'user_id': user_id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
