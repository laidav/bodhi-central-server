from schema import Schema, And
import re

ADD_USER_SCHEMA = {
    "username": And(str,
                    len,
                    lambda n: re.search("^[A-Za-z][A-Za-z0-9_.]*$", n),
                    error="Must be an non empty string"),
    "email": And(str, len, error="Email is required"),
    "password": And(str, len, error="Password is required"),
    "password2": And(str, len, error="Confirm password is required"),
}

AddUserSchema = Schema(ADD_USER_SCHEMA)
