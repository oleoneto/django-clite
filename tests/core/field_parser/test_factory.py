import unittest
from django_clite.core.field_parser.factory import AttributeFactory


class FieldFactoryTestCase(unittest.TestCase):
    # Numeric

    def test_make_bigint_field(self):
        aliases = ["big", "bigint", "big-int"]
        attr_name = 'id'
        model_name = 'Album'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("BigIntegerField", field.kind)
            self.assertEqual("_('id')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_decimal_field(self):
        aliases = ["decimal"]
        attr_name = 'price'
        model_name = 'Album'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("DecimalField", field.kind)
            self.assertEqual("_('price')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_float_field(self):
        aliases = ["float"]
        attr_name = 'price'
        model_name = 'Album'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("FloatField", field.kind)
            self.assertEqual("_('price')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_integer_field(self):
        aliases = ["int", "integer"]
        attr_name = 'tracks'
        model_name = 'Album'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("IntegerField", field.kind)
            self.assertEqual("_('tracks')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # Boolean

    def test_make_boolean_field(self):
        aliases = ["bool", "boolean"]
        attr_name = 'is_compilation'
        model_name = 'Album'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("BooleanField", field.kind)
            self.assertEqual("_('is_compilation'), default=False", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # Text and Strings

    def test_make_char_field(self):
        aliases = ["char"]
        attr_name = 'title'
        model_name = 'Album'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("CharField", field.kind)
            self.assertEqual("_('title'), max_length=100, blank=False", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_slug_field(self):
        aliases = ["slug"]
        attr_name = "slug"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("SlugField", field.kind)
            self.assertEqual("_('slug'), unique=True", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_string_field(self):
        aliases = ["string", "text"]
        attr_name = "description"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("TextField", field.kind)
            self.assertEqual("_('description'), blank=False", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supports_admin)

    def test_make_uuid_field(self):
        aliases = ["uuid"]
        attr_name = "id"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("UUIDField", field.kind)
            self.assertEqual(
                "_('id'), default=uuid.uuid4, editable=False", field.field_options(attr_name, model_name)
            )

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # Files

    def test_make_file_field(self):
        aliases = ["file"]
        attr_name = "file"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("FileField", field.kind)
            self.assertEqual(
                "_('file'), blank=False, upload_to='uploads/albums/files/'",
                field.field_options(attr_name, model_name),
            )

            self.assertTrue(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supports_admin)

    def test_make_filepath_field(self):
        aliases = ["filepath", "file-path"]
        attr_name = "file"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("FilePathField", field.kind)
            self.assertEqual(
                "_('file'), blank=True, upload_to='uploads/albums/files/'",
                field.field_options(attr_name, model_name),
            )

            self.assertTrue(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supports_admin)

    def test_make_image_field(self):
        aliases = ["image", "photo"]
        attr_name = "image"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, "image")

            self.assertEqual("ImageField", field.kind)
            self.assertEqual(
                "_('image'), blank=False, upload_to='uploads/albums/images/'",
                field.field_options(attr_name, model_name),
            )

            self.assertTrue(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertFalse(field.supports_admin)

    # Internet

    def test_make_email_field(self):
        aliases = ["email"]
        attr_name = "email_address"
        model_name = "Person"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("EmailField", field.kind)
            self.assertEqual("_('email_address')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_url_field(self):
        aliases = ["url"]
        attr_name = "url"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("URLField", field.kind)
            self.assertEqual("_('url')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_ip_field(self):
        aliases = ["ip", "ipaddress", "ip-address"]
        attr_name = "ip"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("GenericIPAddressField", field.kind)
            self.assertEqual("_('ip')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # Dates and Time

    def test_make_date_field(self):
        aliases = ["date"]
        attr_name = "date"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("DateField", field.kind)
            self.assertEqual("_('date'), auto_now=True", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_datetime_field(self):
        aliases = ["datetime"]
        attr_name = "datetime"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("DateTimeField", field.kind)
            self.assertEqual("_('datetime'), auto_now=True", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_duration_field(self):
        aliases = ["duration"]
        attr_name = "duration"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("DurationField", field.kind)
            self.assertEqual("_('duration')", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    def test_make_time_field(self):
        aliases = ["time"]
        attr_name = "time"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("TimeField", field.kind)
            self.assertEqual("_('time'), auto_now=True", field.field_options(attr_name, model_name))

            self.assertFalse(field.is_media_field)
            self.assertFalse(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # Relationships
    # =============

    # Foreign Key
    def test_make_foreign_key_field(self):
        aliases = ["belongsto", "belongs-to", "fk", "foreignkey", "foreign-key"]
        attr_name = "singer"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("ForeignKey", field.kind)
            self.assertEqual(
                "Singer, _('singer'), blank=False, on_delete=models.DO_NOTHING, related_name='album'",
                field.field_options(attr_name, model_name),
            )

            self.assertFalse(field.is_media_field)
            self.assertTrue(field.is_relationship)
            self.assertTrue(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # One-To-One

    def test_make_one_to_one_field(self):
        aliases = ["one", "hasone", "has-one", "one-to-one"]
        attr_name = 'ssn'
        model_name = 'Person'

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("OneToOneField", field.kind)
            self.assertEqual(
                "Ssn, _('ssn'), blank=False, on_delete=models.CASCADE, primary_key=True, related_name='person'",
                field.field_options(attr_name, model_name),
            )

            self.assertFalse(field.is_media_field)
            self.assertTrue(field.is_relationship)
            self.assertTrue(field.is_fk_relationship)
            self.assertFalse(field.is_many_relationship)
            self.assertTrue(field.supports_admin)

    # Many

    def test_make_many_to_many_field(self):
        aliases = ["hasmany", "has-many", "many", "manytomany", "many-to-many"]
        attr_name = "songs"
        model_name = "Album"

        for alias in aliases:
            field = AttributeFactory().field_options(alias, attr_name)

            self.assertEqual("ManyToManyField", field.kind)
            self.assertEqual(
                "Song, _('songs'), blank=True, on_delete=models.DO_NOTHING, related_name='album'",
                field.field_options(attr_name, model_name),
            )

            self.assertFalse(field.is_media_field)
            self.assertTrue(field.is_relationship)
            self.assertFalse(field.is_fk_relationship)
            self.assertTrue(field.is_many_relationship)
            self.assertFalse(field.supports_admin)
