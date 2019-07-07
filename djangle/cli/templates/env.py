from jinja2 import Template

env_template = Template("""# Example variables that could be in an environment file. 
# Commit only the .env.example file, not the .env file. Use the example file to illustrate 
# what variables your environment uses, but be sure to not commit this file with any sensitive information.

DEBUG=''
SECRET_KEY=''

SERVER_EMAIL=''
EMAIL_HOST=''
EMAIL_HOST_USER=''
EMAIL_PASSWORD=''

REDIS_URL=''
REDIS_PASSWORD=''

OTP_ISSUER=''

AWS_BUCKET_NAME=''
AWS_LOCATION=''
AWS_MEDIA_LOCATION=''
AWS_STATIC_LOCATION=''
AWS_REGION_NAME=''
AWS_ORIGIN=''
# ....

DB_HOST=''
DB_NAME=''
DB_USER=''
DB_PASSWORD=''

DOCKER_DB_HOST=''
DOCKER_DB_NAME=''
DOCKER_DB_USER=''
DOCKER_DB_PASSWORD=''
""")
