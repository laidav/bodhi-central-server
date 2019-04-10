from schema import Schema, Or, Use, Optional, And

BASE_POST_SCHEMA = {
    "title": And(str, len, error="Invalid title"),
    "subjects": And(list,
                    lambda n: all(isinstance(item, int) and item > 0 for item in n) and n,
                    error="Invalid Subjects.  Should be an array of integers"),
    "description": And(str, len, error="Invalid description"),
    Optional("link"): Or(str, error="Invalid application should be a string type")
}

GET_POSTS_QSP_SCHEMA = {
    Optional("subject_id"): And(list,
                                Use(lambda n: [int(item) for item in n]),
                                error="subject query string parameter must be positive integers")
}

PostSchema = Schema(BASE_POST_SCHEMA)
PostQSPSchema = Schema(GET_POSTS_QSP_SCHEMA)
