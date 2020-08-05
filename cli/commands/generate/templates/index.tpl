from ..models import {{ classname }}
from haystack import indexes


class {{ classname }}Index(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True{% if template %}, template_name='{{ template }}'{% endif %})
    rendered = indexes.CharField(
        use_template=True,
        indexed=False,
        template_name='search/indexes/{{ app }}/{{ model.lower() }}_rendered.txt'
    )

    def get_model(self):
        return {{ classname }}
