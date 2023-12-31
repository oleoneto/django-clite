import unittest
from cli.core.field_parser.factory import make_field


class FieldFactoryTestCase(unittest.TestCase):
    # Numeric

    def test_make_bigint_field(self):
        aliases = ["big", "bigint", "big-int"]

        for alias in aliases:
            field = make_field(alias, "id", "Album")

            self.assertEqual("BigIntegerField", field.kind)
            self.assertEqual("id", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('id')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_decimal_field(self):
        aliases = ["decimal"]

        for alias in aliases:
            field = make_field(alias, "price", "Album")

            self.assertEqual("DecimalField", field.kind)
            self.assertEqual("price", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('price')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_float_field(self):
        aliases = ["float"]

        for alias in aliases:
            field = make_field(alias, "price", "Album")

            self.assertEqual("FloatField", field.kind)
            self.assertEqual("price", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('price')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_integer_field(self):
        aliases = ["int", "integer"]

        for alias in aliases:
            field = make_field(alias, "tracks", "Album")

            self.assertEqual("IntegerField", field.kind)
            self.assertEqual("tracks", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('tracks')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # Boolean

    def test_make_boolean_field(self):
        aliases = ["bool", "boolean"]

        for alias in aliases:
            field = make_field(alias, "is_compilation", "Album")

            self.assertEqual("BooleanField", field.kind)
            self.assertEqual("is_compilation", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('is_compilation'), default=False", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # Text and Strings

    def test_make_char_field(self):
        aliases = ["char"]

        for alias in aliases:
            field = make_field(alias, "title", "Album")

            self.assertEqual("CharField", field.kind)
            self.assertEqual("title", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('title'), max_length=100, blank=False", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_slug_field(self):
        aliases = ["slug"]

        for alias in aliases:
            field = make_field(alias, "slug", "Album")

            self.assertEqual("SlugField", field.kind)
            self.assertEqual("slug", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('slug'), unique=True", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_string_field(self):
        aliases = ["string", "text"]

        for alias in aliases:
            field = make_field(alias, "description", "Album")

            self.assertEqual("TextField", field.kind)
            self.assertEqual("description", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('description'), blank=False", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supported_in_admin)

    def test_make_uuid_field(self):
        aliases = ["uuid"]

        for alias in aliases:
            field = make_field(alias, "id", "Album")

            self.assertEqual("UUIDField", field.kind)
            self.assertEqual("id", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('id'), default=uuid.uuid4, editable=False", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # Files

    def test_make_file_field(self):
        aliases = ["file"]

        for alias in aliases:
            field = make_field(alias, "file", "Album")

            self.assertEqual("FileField", field.kind)
            self.assertEqual("file", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('file'), blank=False, upload_to='uploads/albums/files/'", field.options)

            self.assertTrue(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supported_in_admin)

    def test_make_filepath_field(self):
        aliases = ["filepath", "file-path"]

        for alias in aliases:
            field = make_field(alias, "file", "Album")

            self.assertEqual("FilePathField", field.kind)
            self.assertEqual("file", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('file'), blank=True, upload_to='uploads/albums/files/'", field.options)

            self.assertTrue(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supported_in_admin)

    def test_make_image_field(self):
        aliases = ["image", "photo"]

        for alias in aliases:
            field = make_field(alias, "image", "Album")

            self.assertEqual("ImageField", field.kind)
            self.assertEqual("image", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('image'), blank=False, upload_to='uploads/albums/images/'", field.options)

            self.assertTrue(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supported_in_admin)

    # Internet

    def test_make_email_field(self):
        aliases = ["email"]

        for alias in aliases:
            field = make_field(alias, "email_address", "Person")

            self.assertEqual("EmailField", field.kind)
            self.assertEqual("email_address", field.name)
            self.assertEqual("Person", field.model)
            self.assertEqual("_('email_address')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_url_field(self):
        aliases = ["url"]

        for alias in aliases:
            field = make_field(alias, "url", "Album")

            self.assertEqual("URLField", field.kind)
            self.assertEqual("url", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('url')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_ip_field(self):
        aliases = ["ip", "ipaddress", "ip-address"]

        for alias in aliases:
            field = make_field(alias, "ip", "Album")

            self.assertEqual("GenericIPAddressField", field.kind)
            self.assertEqual("ip", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('ip')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # Dates and Time

    def test_make_date_field(self):
        aliases = ["date"]

        for alias in aliases:
            field = make_field(alias, "date", "Album")

            self.assertEqual("DateField", field.kind)
            self.assertEqual("date", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('date'), auto_now=True", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_datetime_field(self):
        aliases = ["datetime"]

        for alias in aliases:
            field = make_field(alias, "datetime", "Album")

            self.assertEqual("DateTimeField", field.kind)
            self.assertEqual("datetime", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('datetime'), auto_now=True", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_duration_field(self):
        aliases = ["duration"]

        for alias in aliases:
            field = make_field(alias, "duration", "Album")

            self.assertEqual("DurationField", field.kind)
            self.assertEqual("duration", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('duration')", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    def test_make_time_field(self):
        aliases = ["time"]

        for alias in aliases:
            field = make_field(alias, "time", "Album")

            self.assertEqual("TimeField", field.kind)
            self.assertEqual("time", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual("_('time'), auto_now=True", field.options)

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # Relationships
    # =============

    # Foreign Key
    def test_make_foreign_key_field(self):
        aliases = ["belongsto", "belongs-to", "fk", "foreignkey", "foreign-key"]

        for alias in aliases:
            field = make_field(alias, "singer", "Album")

            self.assertEqual("ForeignKey", field.kind)
            self.assertEqual("singer", field.name)
            self.assertEqual("Album", field.model)
            self.assertEqual(
                "Singer, _('singer'), blank=False, on_delete=models.DO_NOTHING, related_name='album'",
                field.options,
            )

            self.assertFalse(field.is_media_field)
            self.assertTrue(field.is_relationship)
            self.assertTrue(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # One-To-One

    def test_make_one_to_one_field(self):
        aliases = ["one", "hasone", "has-one", "one-to-one"]

        for alias in aliases:
            field = make_field(alias, "ssn", "Person")

            self.assertEqual("OneToOneField", field.kind)
            self.assertEqual("Person", field.model)
            self.assertEqual("ssn", field.name)
            self.assertEqual(
                "Ssn, _('ssn'), blank=False, on_delete=models.CASCADE, primary_key=True, related_name='person'",
                field.options,
            )

            self.assertFalse(field.is_media_field)
            self.assertTrue(field.is_relationship)
            self.assertTrue(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supported_in_admin)

    # Many

    def test_make_many_to_many_field(self):
        aliases = ["hasmany", "has-many", "many", "manytomany", "many-to-many"]

        for alias in aliases:
            field = make_field(alias, "songs", "Album")

            self.assertEqual("ManyToManyField", field.kind)
            self.assertEqual("Album", field.model)
            self.assertEqual("songs", field.name)
            self.assertEqual(
                "Song, _('songs'), blank=True, on_delete=models.DO_NOTHING, related_name='album'",
                field.options,
            )

            self.assertFalse(field.is_media_field)
            self.assertTrue(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertTrue(field.is_many_relationship)
            self.assertFalse(field.supported_in_admin)
