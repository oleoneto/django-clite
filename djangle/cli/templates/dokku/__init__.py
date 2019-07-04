from jinja2 import Template


app_template = Template("""{
  "scripts": {
    "dokku": {
      "predeploy": "/code/manage.py migrate --noinput",
      "postdeploy": "/code/./notify.sh"
    }
  }
}
""")


dokku_checks_template = Template("""DOKKU_CHECKS_WAIT={{ wait }}
DOKKU_CHECKS_TIMEOUT={{ timeout }}
""")


dokku_scale_template = Template("""web={{ web }}""")


procfile_template = Template("""release: ./release.sh
web: gunicorn {{ project }}.wsgi
""")
