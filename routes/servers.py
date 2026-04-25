from aiohttp import web, ClientSession
import aiohttp_session

routes = web.RouteTableDef()
DISCORD_API_BASE = "https://discord.com/api/v10"

@routes.get('/servers')
async def get_servers(request):
    sess = await aiohttp_session.get_session(request)
    access_token = sess.get('access_token')
    if not access_token:
        return web.json_response({"error": "Not authenticated"}, status=401)
        
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession() as session:
        async with session.get(f"{DISCORD_API_BASE}/users/@me/guilds", headers=headers) as resp:
            if resp.status != 200:
                return web.json_response({"error": "Failed to fetch guilds"}, status=400)
            guilds = await resp.json()
            
    return web.json_response(guilds)

@routes.get('/servers/managed')
async def get_managed_servers(request):
    sess = await aiohttp_session.get_session(request)
    access_token = sess.get('access_token')
    if not access_token:
        return web.json_response({"error": "Not authenticated"}, status=401)
        
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession() as session:
        async with session.get(f"{DISCORD_API_BASE}/users/@me/guilds", headers=headers) as resp:
            if resp.status != 200:
                return web.json_response({"error": "Failed to fetch guilds"}, status=400)
            guilds = await resp.json()
            
    # Filter for MANAGE_GUILD (0x20) or ADMINISTRATOR (0x8)
    managed_guilds = []
    for guild in guilds:
        perms = int(guild.get('permissions', 0))
        if (perms & 0x20) == 0x20 or (perms & 0x8) == 0x8:
            managed_guilds.append(guild)
            
    return web.json_response(managed_guilds)

@routes.get('/servers/{server_id}')
async def get_server_info(request):
    server_id = request.match_info.get('server_id')
    return web.json_response({"message": "Not implemented yet"})
