import datetime
from aiohttp import web, ClientSession
import aiohttp_session
from database import db

routes = web.RouteTableDef()
DISCORD_API_BASE = "https://discord.com/api/v10"

@routes.post('/api/beta/enroll')
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
        
    # Verify user has access to this server
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
        
    # Add to beta_servers collection
    await db.db.beta_servers.update_one(
        {"server_id": str(server_id)},
        {"$set": {
            "server_id": str(server_id),
            "server_name": target_guild.get("name"),
            "enrolled_by": user.get("id"),
            "enrolled_at": datetime.datetime.utcnow()
        }},
        upsert=True
    )
    
    return web.json_response({"success": True, "message": "Server enrolled successfully"})
