from flask.helpers import get_debug_flag

from application import create_app
from settings import DevConfig, ProductionConfig

is_debug_mode: bool = get_debug_flag()
config_object = DevConfig if is_debug_mode else ProductionConfig

application = create_app(config_object)

if __name__ == "__main__":
    application.run("localhost", port=5000, debug=is_debug_mode)
