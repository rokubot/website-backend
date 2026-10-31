import aiohttp_cors
from aiohttp import web
from aiohttp_session import setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

import config
from database import db
from routes import routes


async def db_context(app):
    await db.connect()
    app['db'] = db
    
    yield  # Application runs here
    
    await db.disconnect()

async def create_app():
    app = web.Application()
    
    # Setup session
    # aiohttp_session requires exactly 32 bytes for the secret key
    setup_session(app, EncryptedCookieStorage(config.SESSION_SECRET))
    
    # Add routes
    app.add_routes(routes)
    
    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        url: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            allow_headers=("Content-Type", "Authorization", "X-Requested-With"),
            expose_headers=("Content-Type",),
        ) for url in config.FRONTEND_URLS
    })
    
    for route in list(app.router.routes()):
        cors.add(route)
        
    app.cleanup_ctx.append(db_context)
    
    return app
