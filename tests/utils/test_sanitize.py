import unittest
from cli.utils.sanitize import sanitized_string, check_noun_inflection


class SanitizeTestCase(unittest.TestCase):
    def test_sanitize_string(self):
        string = ' Once-Upon a Time '
        sanitized = sanitized_string(string)
        self.assertEqual(sanitized, 'once_upon_a_time')

    def test_force_names_to_be_singular(self):
        names = [
            ('cars', 'car'),
            ('people', 'person'),
            ('vehicles', 'vehicle'),
            ('men', 'man'),
            ('women', 'woman'),
            ('children', 'child'),
            ('oxen', 'ox'),
        ]

        for name_pair in names:
            plural, singular = name_pair
            self.assertEqual(check_noun_inflection(plural, force_singular=True), singular)

    def test_force_names_to_be_plural(self):
        names = [
            ('cars', 'car'),
            ('people', 'person'),
            ('vehicles', 'vehicle'),
            ('men', 'man'),
            ('women', 'woman'),
            ('children', 'child'),
            ('oxen', 'ox'),
        ]

        for name_pair in names:
            plural, singular = name_pair
            self.assertEqual(check_noun_inflection(plural, force_plural=True), plural)

    def test_do_not_inflect_names(self):
        names = [
            'cars',
            'car',
            'people',
            'person',
            'vehicles',
            'vehicle',
            'men',
            'man',
            'women',
            'woman',
            'children',
            'child',
            'oxen',
            'ox'
        ]

        for name in names:
            self.assertEqual(check_noun_inflection(name), name)


if __name__ == '__main__':
    unittest.main()
