# __author__ = itsneo1990
import os


class ENV(object):
    def __init__(self):
        env = os.environ.get("perblog_env", "local")
        print('...............................')
        print(env)
        print('...............................')
        file_name = env + "_settings"
        base_settings = __import__("PersonalBlog", fromlist=[file_name])
        self.settings = getattr(base_settings, file_name)

    def get_config(self, value):
        return getattr(self.settings, value, None)
