from functools import wraps

from flask import abort
import flask_jwt_extended as jwt

from ebisu_flashcards.database.models import User
from ebisu_flashcards import errors



def unauth_goes_to_login(func):
    """
        Decorator for protected pages. 
        Sends unauthorized users to /login.
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not jwt.get_jwt_identity():
            raise abort(401)
        return func(*args, **kwargs)

    return wrapped



def login(username, password):
    """
        Given username and credentials, returns the proper JWT tokens.

        :param username: the user's username.
        :param password: the supplied password.
        :returns: two JWT tokens if the login is successful.
        :raises: UnauthorizedError if the login fails.
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise errors.UnauthorizedError

    authorized = user.check_password(password)
    if not authorized:
        raise errors.UnauthorizedError

    # Create the tokens we will be sending back to the user
    access_token = jwt.create_access_token(identity=str(user.id))
    refresh_token = jwt.create_refresh_token(identity=str(user.id))

    return access_token, refresh_token


def signup(user_data):
    """
        Signs up a new user. Can raise DB errors if username or emails are not unique.
        FIXME: such errors are not handled very well!

        :param user_data: the content of the signup form fields as a dictionary.
        :returns: the ID of the newly generated user.
    """
    user = User(**user_data)
    user.hash_password()
    user.save()
    return user.id
