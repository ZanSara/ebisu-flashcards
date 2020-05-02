from flask import Response, request, render_template
from flask_jwt_extended import create_access_token, decode_token
from database.models import User
from flask_restful import Resource
import datetime
from services.mail_service import send_email


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user =  User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            raise UnauthorizedError

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        body = request.get_json()
        email = body.get('email')
        if not email:
            raise SchemaValidationError

        user = User.objects.get(email=email)
        if not user:
            raise EmailDoesnotExistsError

        expires = datetime.timedelta(hours=24)
        reset_token = create_access_token(str(user.id), expires_delta=expires)

        return send_email('[Ebisu-Flashcards] Reset Your Password',
                            sender='test@test.com',
                            recipients=[user.email],
                            text_body=render_template('email/reset_password.txt',
                                                    url=url + reset_token),
                            html_body=render_template('email/reset_password.html',
                                                    url=url + reset_token))


class ResetPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        body = request.get_json()
        reset_token = body.get('reset_token')
        password = body.get('password')

        if not reset_token or not password:
            raise SchemaValidationError

        user_id = decode_token(reset_token)['identity']

        user = User.objects.get(id=user_id)

        user.modify(password=password)
        user.hash_password()
        user.save()

        return send_email('[Ebisu-Flashcards] Password reset successful',
                            sender='support@movie-bag.com',
                            recipients=[user.email],
                            text_body='Password reset was successful',
                            html_body='<p>Password reset was successful</p>')

        