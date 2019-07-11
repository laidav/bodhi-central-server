from schema import Schema, And
import re

ADD_USER_SCHEMA = {
    "username": And(str,
                    len,
                    lambda n: re.search("^[A-Za-z][A-Za-z0-9_.]*$", n),
                    error="Must be an non empty string, and contain only letters, numbers, underscores and dots"),
    "email": And(str,
                 len,
                 lambda n: re.search(
                     "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", n),
                 error="Email is required and be of valid format"),
    "password": And(str, len, error="Password is required"),
    "password2": And(str, len, error="Confirm password is required"),
}

AddUserSchema = Schema(ADD_USER_SCHEMA)
