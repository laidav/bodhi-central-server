from schema import Schema, And
import re

ADD_USER_SCHEMA = {
    "username": And(str,
                    len,
                    lambda n: re.search("^[A-Za-z][A-Za-z0-9_.]*$", n),
                    error="Must be an non empty string")
}

AddUserSchema = Schema(ADD_USER_SCHEMA)
