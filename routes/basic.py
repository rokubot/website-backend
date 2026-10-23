from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/health')
async def get_health(request):
    auth = request.headers.get('Authorization')
    if not auth or auth != "Rokurocks":
        return web.json_response({"error": "Unauthorized"}, status=401)

    return web.json_response({"status": "ok"})
