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

REDIS_URL=# i.e. redis://[:password]@127.0.0.1:6379

DATABASE_URL=postgres://u:p@service:5432/service
