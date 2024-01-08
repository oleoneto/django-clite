import unittest
from cli.utils import inflect, sanitized_string


class UtilsTestCase(unittest.TestCase):
    def test_inflection(self):
        singulars = {
            "woman": "women",
            "man": "men",
            "ox": "oxen",
            "car": "cars",
            "child": "children",
        }
        for word, plural in singulars.items():
            self.assertEqual(inflect(word, force_plural=True), plural)

        plurals = {
            "women": "woman",
            "men": "man",
            "oxen": "ox",
            "cars": "car",
            "children": "child",
        }
        for word, singular in plurals.items():
            self.assertEqual(inflect(word, force_singular=True), singular)

    def test_sanitized_string(self):
        string = " Once-Upon a Time "
        self.assertEqual(sanitized_string(string), "once_upon_a_time")

        string = "/my.example/site-1_/"
        self.assertEqual(sanitized_string(string), "my_example_site_1")
