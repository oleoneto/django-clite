from .{{ model.lower() }}_{% if class_type == 'list' %}list{% else %}detail{% endif %} import {{ classname }}{% if class_type == 'list' %}ListView{% else %}DetailView{% endif %}