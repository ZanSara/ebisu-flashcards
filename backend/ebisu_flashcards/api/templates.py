import os
import json

from flask import Response
from flask_restful import Resource
import flask_jwt_extended as jwt

from ebisu_flashcards.database.models import Template
from ebisu_flashcards.operations.templates import TemplateOps
from ebisu_flashcards.operations.serialization import Serializer


class TemplatesApi(TemplateOps, Serializer, Resource):
    
    @jwt.jwt_required
    def get(self):
        try:
            db_templates = self.get_template('all')
            templates = self.serialize_list(db_templates)
            return Response(templates, mimetype="application/json", status=200)

        except Template.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=200)


class TemplateApi(TemplateOps, Serializer, Resource):

    @jwt.jwt_required
    def get(self, template_id):
        try:
            db_template = self.get_template(template_id)
            template = self.serialize_one(db_template)
            return Response(template.to_json(), mimetype="application/json", status=200)

        except Template.DoesNotExist:
            return Response(json.dumps(None), mimetype="application/json", status=200)
