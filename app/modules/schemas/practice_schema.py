from schema import Schema, Or, Optional, Use, And

BASE_PRACTICE_SCHEMA = {
    "teaching_point": Or(str, error="Invalid teaching_point"),
    "subjects": And(list,
                    lambda n: all(isinstance(item, int) and item > 0 for item in n),
                    error="Invalid Subjects.  Should be an array of integers"),
    Optional("application"): Or(str, error="Invalid application should be a string type"),
    Optional("post_id"): Use(int, error="Invalid Post Id.  Must be an integer.")
}

AddPracticeSchema = Schema(BASE_PRACTICE_SCHEMA)
