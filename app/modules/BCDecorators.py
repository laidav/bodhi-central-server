def set_attributes_decorator(func):
    def func_wrapper(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

        return func(self, *initial_data, **kwargs)

    return func_wrapper


def update_from_json_decorator(func):
    def func_wrapper(self, data):
        for key, value in data.items():
            setattr(self, key, value)

        return func(self, data)

    return func_wrapper
