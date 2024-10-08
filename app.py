# pylint: disable=w1203
import os
import json
import uuid
import logging
import jinja2
import aiohttp
import aiohttp_jinja2
from aiohttp import web
from dotenv import load_dotenv
import aiohttp_cors

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

clients = {}
MAX_MESSAGE_SIZE = int(os.getenv('MAX_MESSAGE_SIZE', '2048'))
ALLOWED_ORIGINS = os.getenv(
        'ALLOWED_ORIGINS', 'http://0.0.0.0/8080'
    ).split(',')

@aiohttp_jinja2.template("index.html")
async def index(request):
    logger.info("Index page accessed")
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
    logger.info(f"New WebSocket connection established with client_id: {client_id}")

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if len(msg.data) > MAX_MESSAGE_SIZE:
                    error_message = {
                        "type": "error",
                        "content": (
                            "Message too large! Limit is "
                            f"{MAX_MESSAGE_SIZE} bytes."
                        ),
                        "from": "Server"
                    }
                    await ws.send_str(json.dumps(error_message))
                    logger.warning(f"Message from client_id {client_id} exceeded size limit.")
                    continue
                data = json.loads(msg.data)
                if data["type"] == "message":
                    message_data = {
                        "type": "message",
                        "content": data["content"],
                        "from": client_id
                    }

                    for cid, client in clients.items():
                        if cid != client_id:
                            await client.send_str(json.dumps(message_data))
                    logger.info(f"Message from client_id {client_id}: {data['content']}")
    finally:
        clients.pop(client_id, None)
        logger.info(f"WebSocket connection closed for client_id: {client_id}")

    return ws

async def get_messages(request):
    return web.json_response({})

async def serve_css(request):
    filename = request.match_info['filename']
    return web.FileResponse(path=f'./static/css/{filename}', headers={
        'Content-Type': 'text/css'
    })

@web.middleware
async def security_headers_middleware(request, handler):
    response = await handler(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Frame-Options"] = "DENY"
    # response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["Referrer-Policy"] = "no-referrer"

    csp = (
        "default-src 'self'; "
        "connect-src 'self' wss:; "
        "img-src 'self' data:; "
    )
    # response.headers["Content-Security-Policy"] = csp

    return response

app = web.Application(middlewares=[security_headers_middleware])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))

cors = aiohttp_cors.setup(app, defaults={
    origin: aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        max_age=3600,
    ) for origin in ALLOWED_ORIGINS
})

cors.add(app.router.add_get("/", index))
cors.add(app.router.add_get("/ws", websocket_handler))
cors.add(app.router.add_get("/messages", get_messages))
cors.add(
    app.router.add_static(
        "/static", path="./static", name="static", append_version=True
    )
)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    logger.info(f"Starting server on {host}:{port}")
    web.run_app(app, host=host, port=port)
