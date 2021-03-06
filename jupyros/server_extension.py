from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import jupyros.version

import rospkg
import os

__version__ = _version.__version__

r = rospkg.RosPack()

class ROSStaticHandler(IPythonHandler):
    def get(self, *args, **kwargs):
        if not args:
            self.write("Error - no argument supplied")
        argslist = args[0].split('/')
        package, rest = argslist[0], '/'.join(argslist[1:])

        file = os.path.join(r.get_path(package), rest)
        try:
            with open(file, 'rb') as f:
                data = f.read()
                self.write(data)
        except:
            self.write("Error opening file %s" % file)
        self.finish()

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/rospkg/(.*)')
    web_app.add_handlers(host_pattern, [(route_pattern, ROSStaticHandler)])
