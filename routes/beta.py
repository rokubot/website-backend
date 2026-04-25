import datetime
from aiohttp import web, ClientSession
import aiohttp_session
from pymongo.errors import DuplicateKeyError
from database import db

routes = web.RouteTableDef()
DISCORD_API_BASE = "https://discord.com/api/v10"


@routes.post('/beta/enroll')
async def enroll_beta(request):
    sess = await aiohttp_session.get_session(request)
    access_token = sess.get('access_token')
    user = sess.get('user')
    if not access_token or not user:
        return web.json_response({"error": "Not authenticated"}, status=401)
        
    try:
        data = await request.json()
    except:
        return web.json_response({"error": "Invalid JSON"}, status=400)
        
    server_id = data.get('server_id')
    if not server_id:
        return web.json_response({"error": "server_id is required"}, status=400)
        
    headers = {"Authorization": f"Bearer {access_token}"}
    async with ClientSession() as session:
        async with session.get(f"{DISCORD_API_BASE}/users/@me/guilds", headers=headers) as resp:
            if resp.status != 200:
                return web.json_response({"error": "Failed to verify guilds"}, status=400)
            guilds = await resp.json()
            
    target_guild = next((g for g in guilds if g['id'] == str(server_id)), None)
    if not target_guild:
        return web.json_response({"error": "Server not found or you are not in it"}, status=403)
        
    perms = int(target_guild.get('permissions', 0))
    if (perms & 0x20) != 0x20 and (perms & 0x8) != 0x8:
        return web.json_response({"error": "You do not have permission to enroll this server"}, status=403)
        
    # Insert into beta_servers — _id is the server_id as int
    try:
        await db.beta_servers.insert_one({
            "_id": int(server_id),
            "server_name": target_guild.get("name"),
            "enrolled_by": int(user.get("id")),
            "enrolled_at": datetime.datetime.utcnow()
        })
    except DuplicateKeyError:
        return web.json_response({"error": "This server is already enrolled in beta"}, status=409)
    
    return web.json_response({"success": True, "message": "Server enrolled successfully"})
