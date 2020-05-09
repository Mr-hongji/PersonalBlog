# __author__ = itsneo1990
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ENV(object):
    def __init__(self):
        try:
            env = os.environ.get("perblog_env", "local")
            print('...............................')
            print(env)
            print('...............................')
            file_name = env + "_settings"
            base_settings = __import__("PersonalBlog", fromlist=[file_name])
            self.settings = getattr(base_settings, file_name)
            f = open('opt/log.txt', 'w+')
            f.write(file_name)
            f.close()
            settingsJsPath = os.path.join(BASE_DIR, 'static/js/settings.js')
            # print(settingsJsPath)

            f = open(settingsJsPath, 'w')
            if env == 'local':
                f.write(
                    'var doc_root_path="e:/";\nvar video_root_path="h:/";\nvar uploadImageRootLoaction = "http://127.0.0.1:8000/static/uploadfiles/articleImages/";')
            else:
                f.write(
                    'var doc_root_path="/opt/files/docfile/";\nvar video_root_path="/opt/files/videofile/";\nvar uploadImageRootLoaction = "http://perblog.natapp1.cc/articleImg/";')
            f.close()
        except Exception as e:
            f = open('opt/errorlog.txt', 'w+')
            f.write(str(e))
            f.close()

    def get_config(self, value):
        nn = getattr(self.settings, 'DATABASES', None)['default']['NAME']
        f = open('/opt/arrtlog.txt', 'w+')
        f.write(str(nn))
        f.close()
        return getattr(self.settings, value, None)

