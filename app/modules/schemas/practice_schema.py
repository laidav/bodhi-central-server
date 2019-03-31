from schema import Schema, Or, Optional

BASE_PRACTICE_SCHEMA = {
    "teaching_point": Or(str, error="Invalid teaching_point"),
    Optional("application"): Or(str, error="application should be a string type")
}

AddPracticeSchema = Schema(BASE_PRACTICE_SCHEMA)
