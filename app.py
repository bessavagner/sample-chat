import os
import json
import uuid
import jinja2
import aiohttp
import aiohttp_jinja2
from aiohttp import web
from dotenv import load_dotenv
import aiohttp_cors

load_dotenv()

clients = {}
ALLOWED_ORIGINS = os.getenv(
        'ALLOWED_ORIGINS', 'http://0.0.0.0/8080'
    ).split(',')

@aiohttp_jinja2.template("index.html")
async def index(request):
    return {}

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    client_id = str(uuid.uuid4())
    clients[client_id] = ws
    welcome_message = {
        "type": "message",
        "content": "Welcome to a chat app demo!",
        "from": "Server"
    }
    await ws.send_str(json.dumps(welcome_message))

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                if data["type"] == "message":
                    # Prepare the message data to be sent
                    message_data = {
                        "type": "message",
                        "content": data["content"],
                        "from": client_id
                    }
                    
                    for cid, client in clients.items():
                        if cid != client_id:
                            await client.send_str(json.dumps(message_data))
    finally:
        clients.pop(client_id, None)
    
    return ws

async def get_messages(request):
    return web.json_response({})

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))

cors = aiohttp_cors.setup(app, defaults={
    origin: aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        max_age=3600,
    ) for origin in ALLOWED_ORIGINS
})

cors.add(app.router.add_static("/static/", path="static", name="static"))
cors.add(app.router.add_get("/", index))
cors.add(app.router.add_get("/ws", websocket_handler))
cors.add(app.router.add_get("/messages", get_messages))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    web.run_app(app, host=host, port=port)
