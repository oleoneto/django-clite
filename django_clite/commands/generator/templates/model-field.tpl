{{ name }} = {% if not special %}models.{% endif %}{{ type }}({% if options %}{{ options }}, {% endif %}verbose_name=_('{{ lazy_name }}'))