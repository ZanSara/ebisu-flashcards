from flask import Response

class CustomResponse(Response):
    def __init__(self, response, **kwargs):
        return super(CustomResponse, self).__init__(response, **kwargs)    

    
    @property
    def status_code(self):
        """The HTTP status code as a number."""
        return self._status_code

    @status_code.setter
    def status_code(self, code):
        self._status_code = code
        try:
            self._status = "%d %s" % (code, HTTP_STATUS_CODES[code].upper())
        except KeyError:
            self._status = "%d UNKNOWN" % code

    @property
    def status(self):
        """The HTTP status code as a string."""
        return self._status

    @status.setter
    def status(self, value):
        try:
            self._status = to_native(value)
        except AttributeError:
            raise TypeError("Invalid status argument")

        try:
            self._status_code = int(self._status.split(None, 1)[0])
        except ValueError:
            self._status_code = 0
            self._status = "0 %s" % self._status
        except IndexError:
            raise ValueError("Empty status argument")