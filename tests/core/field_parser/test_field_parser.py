import unittest
from django_clite.core.field_parser.factory import AttributeFactory


class CallbackTestCase(unittest.TestCase):
    def test_field_parser(self):
        fields = AttributeFactory().parsed_fields(
            [
                "name:char",
                "title:char",
                "user:fk",
                "desc:char",
                "rating:int",
                "owner:fk",
                "total:int",
            ]
        )

        field_names = sorted(fields.keys())
        self.assertEqual(['desc', 'name', 'owner', 'rating', 'title', 'total', 'user'], field_names)

        field_values = list(map(lambda x: x.kind, fields.values()))
        self.assertEqual(['CharField', 'CharField', 'ForeignKey', 'CharField', 'IntegerField', 'ForeignKey', 'IntegerField'], field_values)
