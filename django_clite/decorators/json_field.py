# decorators:json_fields
from functools import wraps
from faker import Faker
from faker.providers import company, date_time, internet, misc

fake = Faker()
fake.add_provider(company)
fake.add_provider(date_time)
fake.add_provider(internet)
fake.add_provider(misc)


JSON_COMPATIBLE_FIELDS = dict()


def is_json_field(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        # print(f'added {function.__name__}')
        # function.fake = fake
        setattr(function, 'fake', fake)
        JSON_COMPATIBLE_FIELDS[function.__name__] = function
        return function  # (*args, **kwargs)
    return wrapper()


def json_field(field):
    # print(JSON_COMPATIBLE_FIELDS)
    if field in JSON_COMPATIBLE_FIELDS:
        return JSON_COMPATIBLE_FIELDS[field]()
