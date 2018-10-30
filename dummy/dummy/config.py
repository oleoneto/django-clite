import cloudinary
from rest_framework.routers import SimpleRouter

class Config(object):

    def __init__(self, arg):
        super(Config, self).__init__()
        self.arg = arg
        self.__router = SimpleRouter(trailing_slash='/?')
        self.__cloudinary = cloudinary.config(
            cloud_name = "",
            api_key="",
            api_secret=""
        )

    def router(self):
        return self.__router

    def cloudinary(self):
        return self.__cloudinary
