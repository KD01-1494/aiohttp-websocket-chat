from aiohttp import web

# - Основной обработчик приложения
from handler import Handler

# -
app = web.Application()

# -
handler_controller = Handler()

# - Подключение путей
app.add_routes([
	web.get('/', handler_controller.chat_handler),
	web.get('/websocketChat', handler_controller.websocket_chat_handler),
	web.get('/register', handler_controller.chat_register_handler),
	web.post('/register', handler_controller.chat_register_handler),
	web.static('/static', 'web')
])