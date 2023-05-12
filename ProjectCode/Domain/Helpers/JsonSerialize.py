import json


class JsonSerialize:
    @staticmethod
    def toJsonAttributes(attributes):
        data = {}
        for attribute_id, attribute_value in attributes.items():
            data[attribute_id] = attribute_value.toJson()
        return json.dumps(data)
