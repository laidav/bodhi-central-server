from schema import Schema, Or, Optional, Use, And

BASE_POST_SCHEMA = {
    "title": And(str, len, error="Invalid title"),
    "subjects": And(list,
                    lambda n: all(isinstance(item, int) and item > 0 for item in n) and n,
                    error="Invalid Subjects.  Should be an array of integers"),
    "description": And(str, len, error="Invalid description"),
    Optional("link"): Or(str, error="Invalid application should be a string type")
}

PostSchema = Schema(BASE_POST_SCHEMA)
