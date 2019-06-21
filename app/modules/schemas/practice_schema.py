from schema import Schema, Or, Optional, Use, And

BASE_PRACTICE_SCHEMA = {
    "teaching_point": And(str, len, error="Invalid teaching_point"),
    "subjects": And(list,
                    lambda n: all(isinstance(item, int)
                                  and item > 0 for item in n) and n,
                    error="Invalid Subjects.  Should be an array of integers"),
    Optional("application"): Or(str, error="Invalid application should be a string type"),
    Optional("post_id"): Use(int, error="Invalid Post Id.  Must be an integer.")
}

GET_PRACTICES_QSP_SCHEMA = {
    Optional("post_id"): And(list,
                             Use(lambda n: int(n[0])),
                             error="subject query string parameter must be positive integers"),
    Optional("subject_id[]"): And(list,
                                  Use(lambda n: [int(item) for item in n]),
                                  error="subject query string parameter must be positive integers")
}

PracticeSchema = Schema(BASE_PRACTICE_SCHEMA)
GetPracticesSchema = Schema(GET_PRACTICES_QSP_SCHEMA)
