from cerberus import Validator
import yaml


def json_schema_validate(resp_json, schema: str):
    v = Validator(yaml.full_load(schema))
    if not v.validate(resp_json):
        raise AssertionError(v.errors)
