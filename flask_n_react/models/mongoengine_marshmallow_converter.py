import inspect
import mongoengine as mongo
import marshmallow as marsh
# from base import *
# from ebisu import *

from .base import *
from .ebisu import *


MO_MA_MAPPING = {
    mongo.fields.BooleanField: marsh.fields.Bool,
    mongo.fields.StringField: marsh.fields.Str,
    mongo.fields.DecimalField: marsh.fields.Float,
    mongo.fields.DateTimeField: marsh.fields.DateTime,
    mongo.fields.EmailField: marsh.fields.Email,
    mongo.fields.BinaryField: marsh.fields.Str,  # FIXME
    mongo.fields.ImageField: marsh.fields.Str,  # FIXME
    # Watch out:
    mongo.fields.ObjectIdField: marsh.fields.Str,  
    mongo.fields.ListField: marsh.fields.Nested,
    mongo.fields.EmbeddedDocumentField: marsh.fields.Nested,
    mongo.fields.EmbeddedDocumentListField: marsh.fields.Nested,
    mongo.fields.ReferenceField: marsh.fields.Nested,
    
}


def mongo_to_marsh(mongo_class):
    # mongo_members = inspect.getmembers(mongo_class, lambda a:not(inspect.isroutine(a)))
    
    mongo_class_name = None
    if isinstance(mongo_class, str):
        mongo_class_name = mongo_class
        if mongo_class_name in globals() and isinstance(globals()[mongo_class_name], type):
           mongo_class = globals()[mongo_class_name]
    if isinstance(mongo_class, type):
        mongo_class_name = mongo_class._class_name.split(".")[-1]  # If there is a superclass, this field will be SuperClass.Class
    else:
        mongo_class_name = mongo_class.__class__.__name__.split(".")[-1]  # If there is a superclass, this field will be SuperClass.Class
        mongo_class = mongo_class.__class__

    mongo_fields = mongo_class._fields
    marsh_fields = {}
    for name, member in mongo_fields.items():

        marsh_field = MO_MA_MAPPING[member.__class__]

        print()
        print(name)
        #print(vars(member))
        # print(vars(marsh_field))

        if member.__class__ == mongo.fields.ListField:
            nested_class_name = member.field
            # Convert string to class
            #print(nested_class_name)
            # if nested_class_name in globals() and isinstance(globals()[nested_class_name], type):
            #    nested_class = globals()[nested_class_name]

            # Loop
            print("--------> ListField: Recursion on:", nested_class_name)
            nested_class_schema = mongo_to_marsh(nested_class_name)
            print("--------> Back from recursion to ", mongo_class_name)
            # Instantiate 
            marsh_fields[name] = marsh_field(nested=nested_class_schema(), many=True)
            
        elif member.__class__ == mongo.fields.EmbeddedDocumentListField:
            nested_class_name = member.field.document_type_obj
            # Convert string to class
            #print(nested_class_name)
            # if nested_class_name in globals() and isinstance(globals()[nested_class_name], type):
            #    nested_class = globals()[nested_class_name]

            # Loop
            print("--------> ListField: Recursion on:", nested_class_name)
            nested_class_schema = mongo_to_marsh(nested_class_name)
            print("--------> Back from recursion to ", mongo_class_name)
            # Instantiate 
            marsh_fields[name] = marsh_field(nested=nested_class_schema(), many=True)

        elif member.__class__ == mongo.fields.EmbeddedDocumentField:
            nested_class_name = member.field
            # Convert string to class
            # if nested_class_name in globals() and isinstance(globals()[nested_class_name], type):
            #     nested_class = globals()[nested_class_name]
            # Loop
            print("--------> EmbeddedDocumentField: Recursion on:", nested_class_name)
            nested_class_schema = mongo_to_marsh(nested_class_name)
            print("--------> Back from recursion to ", mongo_class_name)
            # Instantiate 
            marsh_fields[name] = marsh_field(nested=nested_class_schema())

        elif member.__class__ == mongo.fields.ReferenceField:
            nested_class_name = member.document_type_obj
            # Convert string to class
            # if nested_class_name in globals() and isinstance(globals()[nested_class_name], type):
            #     nested_class = globals()[nested_class_name]

            # Loop
            print("--------> ReferenceField: Recursion on :", nested_class_name)
            nested_class_schema = mongo_to_marsh(nested_class_name)
            print("--------> Back from recursion to ", mongo_class_name)
            # Instantiate 
            marsh_fields[name] = marsh_field(nested=nested_class_schema())
        else:    
            marsh_fields[name] = marsh_field()
        
    # print(marsh_fields)
    Schema = type('{}Schema'.format(mongo_class_name), (marsh.Schema, ), marsh_fields)
    return Schema



def marsh_to_mongo(marsh_schema):
    pass





if __name__ == '__main__':
    mongo.connect('ebisu-db')

    output = mongo_to_marsh(EbisuCard)

    print(output)