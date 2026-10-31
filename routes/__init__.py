from .auth import routes as auth_routes
from .basic import routes as basic_routes
from .beta import routes as beta_routes
from .servers import routes as servers_routes

routes = (
    *auth_routes,
    *basic_routes,
    *beta_routes,
    *servers_routes,
)
