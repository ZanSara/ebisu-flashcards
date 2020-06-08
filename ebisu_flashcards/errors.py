from flask_restful import HTTPException


class InternalServerError(HTTPException):
    pass


class SchemaValidationError(HTTPException):
    pass


class UsernameAlreadyExistsError(HTTPException):
    pass

class UsernameDoesnotExistsError(HTTPException):
    pass

class BadTokenError(HTTPException):
    pass

class UnauthorizedError(HTTPException):
    pass


class NoCardsToReviewError(HTTPException):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },

     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },

     "UsernameAlreadyExistsError": {
         "message": "User with given email address already exists",
         "status": 400
     },
     "UsernameDoesnotExistsError": {
         "message": "Couldn't find the user with given email address",
         "status": 400
     },
     "BadTokenError": {
         "message": "Invalid token",
         "status": 403
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     },

     "NoCardsToReviewError": {
         "message": "No cards to review available for this deck",
         "status": 404
     },
}