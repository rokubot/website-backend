import aiohttp_cors
from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import config
from database import db
from routes.auth import routes as auth_routes
from routes.servers import routes as servers_routes
from routes.beta import routes as beta_routes

async def init_db(app):
    db.connect()

async def close_db(app):
    db.disconnect()

async def create_app():
    app = web.Application()
    
    # Setup session
    # aiohttp_session requires exactly 32 bytes for the secret key
    setup_session(app, EncryptedCookieStorage(config.SESSION_SECRET))
    
    # Add routes
    app.router.add_routes(auth_routes)
    app.router.add_routes(servers_routes)
    app.router.add_routes(beta_routes)
    
    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        url: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ) for url in config.FRONTEND_URLS
    })
    
    for route in list(app.router.routes()):
        cors.add(route)
        
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    
    return app

if __name__ == '__main__':
    web.run_app(create_app(), port=8080)
