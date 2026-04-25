from aiohttp import web, ClientSession
import aiohttp_session
import config
import urllib.parse

routes = web.RouteTableDef()

DISCORD_API_BASE = "https://discord.com/api/v10"

@routes.get('/auth/login')
async def login(request):
    

    return_to = request.query.get('return_to', '/')
    if not return_to.startswith('/'):
        return_to = '/'

    redirect_uri = config.DISCORD_REDIRECT_URI
    if not redirect_uri:
        return web.json_response({"error": "DISCORD_REDIRECT_URI is not configured"}, status=500)

    params = urllib.parse.urlencode({
        "client_id": config.DISCORD_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "identify guilds",
        "state": return_to,
    })

    raise web.HTTPFound(f"https://discord.com/api/oauth2/authorize?{params}")

@routes.get('/auth/callback')
async def callback(request):
    code = request.query.get('code')
    state = request.query.get('state')
    if not code:
        return web.json_response({"error": "No code provided"}, status=400)
    
    # Exchange code for token
    data = {
        'client_id': config.DISCORD_CLIENT_ID,
        'client_secret': config.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config.DISCORD_REDIRECT_URI
    }
    
    async with ClientSession() as session:
        async with session.post(f"{DISCORD_API_BASE}/oauth2/token", data=data) as resp:
            if resp.status != 200:
                text = await resp.text()
                return web.json_response({"error": "Failed to authenticate with Discord", "details": text}, status=400)
            token_data = await resp.json()
            
        access_token = token_data.get('access_token')
        
        # Fetch user info
        headers = {"Authorization": f"Bearer {access_token}"}
        async with session.get(f"{DISCORD_API_BASE}/users/@me", headers=headers) as resp:
            if resp.status != 200:
                return web.json_response({"error": "Failed to fetch user data"}, status=400)
            user_data = await resp.json()
            
    # Save to session
    sess = await aiohttp_session.get_session(request)
    sess['access_token'] = access_token
    sess['user'] = user_data
    
    # Redirect back to frontend
    import urllib.parse
    return_path = urllib.parse.unquote(state) if state else '/'
    if not return_path.startswith('/'):
        return_path = '/'

    # Determine frontend base from the request Origin header.
    # Fall back to the first allowed URL if origin is missing or not whitelisted.
    origin = request.headers.get('Origin', '').rstrip('/')
    allowed = [url.rstrip('/') for url in config.FRONTEND_URLS]
    frontend_base = origin if origin in allowed else allowed[0]

    return web.HTTPFound(f"{frontend_base}{return_path}")

@routes.get('/auth/me')
async def get_me(request):
    sess = await aiohttp_session.get_session(request)
    user = sess.get('user')
    if not user:
        return web.json_response({"error": "Not authenticated"}, status=401)
    return web.json_response(user)

@routes.get('/auth/logout')
async def logout(request):
    sess = await aiohttp_session.get_session(request)
    sess.invalidate()
    return web.json_response({"message": "Logged out"})
