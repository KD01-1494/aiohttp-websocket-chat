from aiohttp import web
from aiohttp import WSMsgType
from asyncio import gather

from json import dumps, loads
from random import randrange

from setting import ChatSetting


class Handler:

    async def chat_register_handler(self, request):
        if request.method == 'GET':
            with open('./web/register.html', 'r', encoding='utf-8') as f:
                html_file = f.read() 
            return web.Response(text=html_file, content_type='text/html')

        response = web.HTTPSeeOther('/')
        data = dict(await request.post())

        if 'user-id' in dict(request.cookies).keys():
            return response

        if not data['user-name']:
            return web.Response(status=400)

        # Задаем случайный ID пользователя в cookies
        response.set_cookie('user-id', randrange(100000, 999999))
        response.set_cookie('user-name', data['user-name'])

        return response


    async def chat_handler(self, request):
        if 'user-id' not in dict(request.cookies).keys():
            return web.HTTPSeeOther('/register')

        with open('./web/chat.html', 'r', encoding='utf-8') as f:
            html_file = f.read() 
        return web.Response(text=html_file, content_type='text/html')


    async def websocket_chat_handler(self, request):
        if 'user-id' not in dict(request.cookies).keys():
            return web.Response(status=403)

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # - Отправка сообщений по всем клиентам
        async def chat_broadcast(ws, json):
            await ws.send_str(dumps(json))

        try:
            ChatSetting.CHAT_MEMBERS.append(
                (request.cookies['user-id'], request.cookies['user-name'], ws)
            )
            
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    message_text = msg.data
                    message = {'messageAuthor': request.cookies['user-name'], 'messageText': message_text}
                    await gather(*[chat_broadcast(member_data[2], message) \
                        for member_data in ChatSetting.CHAT_MEMBERS]
                    )

        except Exception as e:
            raise e

        finally:
            ChatSetting.CHAT_MEMBERS.remove(
                (request.cookies['user-id'], request.cookies['user-name'], ws)
            )