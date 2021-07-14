import os
import json

from flask import Response
from flask_restful import Resource
import flask_jwt_extended as jwt

from ebisu_flashcards.database import algorithms


class AlgorithmsApi(Resource):
    
    @jwt.jwt_required
    def get(self):
        names = []
        for name, klass in algorithms.ALGORITHM_MAPPING.items():
            algorithm = {'name': name}
            names.append(algorithm)
        return Response(json.dumps(names), mimetype="application/json", status=200)
