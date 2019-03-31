from schema import Schema, Or, Optional, Use

BASE_PRACTICE_SCHEMA = {
    "teaching_point": Or(str, error="Invalid teaching_point"),
    Optional("application"): Or(str, error="Invalid application should be a string type"),
    Optional("post_id"): Use(int, error="Invalid Post Id.  Must be an integer.")
}

AddPracticeSchema = Schema(BASE_PRACTICE_SCHEMA)
