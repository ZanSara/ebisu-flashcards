from typing import Any

import json 
import bson
import mongoengine as mongo


class Serializer:
    """
        Serializes database entities into JSON.
    """

    def serialize_list(self, entities: Any) -> str:
        """
            Given a list of entities, returns a JSON containing
            all the data of the list of entities.

            :param entities: List of cards to serialize
            :param server_side_rendering: A function that does the SSR, if present. 
                Defaults to an identity function.
            :returns: a JSON string representation of the input list.
        """
        json_list = []
        for entity in entities:
            entity_mongo = entity.to_mongo()
            json_list.append(entity_mongo)
        return bson.json_util.dumps(json_list)


    def serialize_one(self, entity: Any) -> str:
        """
            Given a database entity, returns a JSON containing
            all the data of the specified entity.

            :param entity: database entity to serialize
            :returns: a JSON string representation of the input entity.
        """
        return entity.to_json()
