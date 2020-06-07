class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass

class UsernameDoesnotExistsError(Exception):
    pass

class BadTokenError(Exception):
    pass

class UnauthorizedError(Exception):
    pass


class NoCardsToReviewError(Exception):
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