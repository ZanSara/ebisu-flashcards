import datetime

from flask import Response, request, render_template, jsonify
import flask_jwt_extended as jwt
from flask_restful import Resource

from services.mail_service import send_email
from database.models import User
from api_resources import errors


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user =  User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200


# class LoginApi(Resource):
#     # Use the set_access_cookie() and set_refresh_cookie() on a response
#     # object to set the JWTs in the response cookies. You can configure
#     # the cookie names and other settings via various app.config options
#     def post(self):
#         # Identify the user
#         body = request.get_json()
#         user = User.objects.get(email=body.get('email'))
#         authorized = user.check_password(body.get('password'))
#         if not authorized:
#             raise errors.UnauthorizedError

#         # Create the tokens we will be sending back to the user
#         access_token = jwt.create_access_token(identity=body.get('email'))
#         refresh_token = jwt.create_refresh_token(identity=body.get('email'))

#         # Set the JWT cookies in the response
#         resp = jsonify({'login': True})
#         jwt.set_access_cookies(resp, access_token)
#         jwt.set_refresh_cookies(resp, refresh_token)
#         return resp, 200


# class LogoutApi(Resource):
#     # Because the JWTs are stored in an httponly cookie now, we cannot
#     # log the user out by simply deleting the cookie in the frontend.
#     # We need the backend to send us a response to delete the cookies
#     # in order to logout. unset_jwt_cookies is a helper function to
#     # do just that.
#     def get(self):
#         resp = jsonify()
#         jwt.unset_jwt_cookies(resp)
#         return {'logout': True}


class RefreshTokenApi(Resource):
    # Same thing as login here, except we are only setting a new cookie
    # for the access token.
    @jwt.jwt_refresh_token_required
    def post(self):
        # Create the new access token
        current_user = jwt.get_jwt_identity()
        access_token = jwt.create_access_token(identity=current_user)

        # Set the JWT access cookie in the response
        resp = jsonify({'refresh': True})
        jwt.set_access_cookies(resp, access_token)
        return resp, 200


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        body = request.get_json()
        email = body.get('email')
        if not email:
            raise errors.SchemaValidationError

        user = User.objects.get(email=email)
        if not user:
            raise errors.EmailDoesnotExistsError

        expires = datetime.timedelta(hours=24)
        reset_token = jwt.create_access_token(str(user.id), expires_delta=expires)

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
            raise errors.SchemaValidationError

        user_id = jwt.decode_token(reset_token)['identity']

        user = User.objects.get(id=user_id)

        user.modify(password=password)
        user.hash_password()
        user.save()

        return send_email('[Ebisu-Flashcards] Password reset successful',
                            sender='support@movie-bag.com',
                            recipients=[user.email],
                            text_body='Password reset was successful',
                            html_body='<p>Password reset was successful</p>')

        