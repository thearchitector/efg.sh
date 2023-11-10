from blacksheep import Application
from blacksheep.server.templating import use_templates
from jinja2 import PackageLoader

from app.controllers import *  # noqa
from app.database import sessionmaker_factory
from app.environment import EnvironmentSingleton
from app.responses import GzipMiddleware

ENVIRONMENT = EnvironmentSingleton()

app = Application(
    show_error_details=ENVIRONMENT.is_development,
    debug=ENVIRONMENT.is_development,
)


# gzip html
app.middlewares.append(GzipMiddleware())

# every @route that defines a variable with the type EnvironmentSingleton will get this
# exact instance. useful for singletons, like environment-loaded settings
app.services.add_instance(ENVIRONMENT)
app.services.add_singleton_by_factory(sessionmaker_factory)

# initialize and configure the jinja templating engine
use_templates(app, loader=PackageLoader("app", "templates"), enable_async=True)
## configure jinja to strip out comments by default, since they're
## functional hints to prettier
app.jinja_environment.comment_start_string = "<!--"
app.jinja_environment.comment_end_string = "-->"
