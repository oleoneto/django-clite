# {{ project }}:{{ app }}:admin
from django.contrib import admin

admin.site.site_header = '{{ project }}'
admin.site.site_title = '{{ project }} Dashboard'
admin.site.index_title = '{{ project }} Dashboard'
admin.empty_value_display = '**Empty**'
