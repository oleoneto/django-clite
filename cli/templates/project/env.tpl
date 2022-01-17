# Example variables that could be in an environment file.
# Commit only the .env-example file, not the .env file. Use the example file to illustrate
# what variables your environment uses, but be sure to not commit this file with any sensitive information.

DEBUG=True

ADMINS=# i.e (('Admin', 'admin@example.com'),)

SECRET_KEY=

SERVER_EMAIL=# i.e no-reply@example.com
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

STRIPE_LIVE_MODE=False
STRIPE_LIVE_PUBLIC_KEY=
STRIPE_LIVE_SECRET_KEY=
STRIPE_TEST_SECRET_KEY=
STRIPE_TEST_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SIGNING_SECRET=

OTP_ISSUER="Your Organization Name"
TWILIO_SID=
TWILIO_TOKEN=
TWILIO_CALLER_ID=

AWS_BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

REDIS_URL=# i.e. redis://[:password]@127.0.0.1:6379

DATABASE_URL=postgres://u:p@service:5432/service

SENTRY_DSN=
