from jinja2 import Template

env_template = Template("""# Example variables that could be in an environment file.
# Commit only the .env-example file, not the .env file. Use the example file to illustrate
# what variables your environment uses, but be sure to not commit this file with any sensitive information.

DEBUG=True
IS_LOCAL=True
ADMINS=""# i.e (('Admin', 'admin@example.com'),)


SECRET_KEY=''


SERVER_EMAIL='' # i.e no-reply@example.com
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_RELAY_DOMAIN='relay.example.com'


SENDGRID_API_KEY = ''


STRIPE_LIVE_MODE=False
STRIPE_LIVE_PUBLIC_KEY=''
STRIPE_LIVE_SECRET_KEY=''
STRIPE_TEST_SECRET_KEY=''
STRIPE_TEST_PUBLISHABLE_KEY=''
STRIPE_WEBHOOK_SIGNING_SECRET=''


OTP_ISSUER='Organization Name'
TWILIO_SID=''
TWILIO_TOKEN=''
TWILIO_CALLER_ID=''


AWS_BUCKET_NAME=''
AWS_LOCATION=''
AWS_STATIC_LOCATION=''
AWS_MEDIA_LOCATION=''
AWS_PRIVATE_MEDIA_LOCATION=''
AWS_REGION_NAME=''
AWS_ORIGIN=''
AWS_ENDPOINT=''
AWS_ENDPOINT_URL=''
AWS_CUSTOM_DOMAIN=''
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''


CLOUDINARY_URL=""


REDIS_URL='' # i.e. redis://[:password]@127.0.0.1:6379


DOCKER_DB_NAME=''
DOCKER_DB_USER=''
DOCKER_DB_PASSWORD=''

LOCAL_DB_NAME=''
LOCAL_DB_USER=''
LOCAL_DB_PASSWORD=''
LOCAL_DB_HOST=localhost


SENTRY_DSN=''


GITHUB_WEBHOOKS_VERIFICATION_KEY=''
""")
