from functools import wraps
import datetime
from django_clite.decorators.json_field import is_json_field, json_field
from django_clite.decorators.lazy import lazy
from faker import Faker
from faker.providers import company, date_time, internet, misc

fake = Faker()
fake.add_provider(company)
fake.add_provider(date_time)
fake.add_provider(internet)
fake.add_provider(misc)


@is_json_field
def BigIntegerField():
    return fake.pyint()


@is_json_field
def BooleanField():
    return fake.pybool()


@is_json_field
def CharField(length=50):
    return f'"{fake.text(length)}"'


class FieldFactory:

    def __init__(self):
        self.fake = Faker()

    def BigIntegerField(self):
        return self.fake.pyint()

    def BooleanField(self):
        return self.fake.pybool()

    def CharField(self, length=50):
        return f'"{self.fake.text(length)}"'

    def DateField(self):
        return f'"{self.fake.future_date()}"'

    def DateTimeField(self):
        return f'"{self.fake.iso8601()}"'

    def DecimalField(self):
        return self.fake.pydecimal()

    def DurationField(self):
        return f'"{datetime.timedelta(days=0, seconds=60)}"'

    def EmailField(self):
        return f'"{self.fake.safe_email()}"'

    def GenericIPAddressField(self):
        return f'"{self.fake.ipv4()}"'

    def FileField(self):
        return f'"{self.fake.file_path()}"'

    def FilePathField(self):
        return f'"{self.fake.file_path()}"'

    def FloatField(self):
        return self.fake.pyfloat()

    def ImageField(self):
        return f'"{self.fake.image_url()}"'

    def IntegerField(self):
        return self.fake.pyint()

    def SlugField(self):
        return f'"{self.fake.slug()}"'

    def TextField(self):
        return f'"{self.fake.text(100)}"'

    def TimeField(self):
        return f'"{self.fake.time()}"'

    def URLField(self):
        return f'"{self.fake.url()}"'

    @is_json_field
    def UUIDField(self):
        return f'"{self.fake.uuid4()}"'
