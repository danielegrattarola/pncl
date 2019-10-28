import asyncio
import json
import os
from multiprocessing import Process

from aiohttp import web
from aiohttp_sse import sse_response

from pncl import STATIC_DIR


class Server:
    def __init__(self, port=8080, host='0.0.0.0', events_per_second=1):
        """
        Creates the backend server.
        :param port: port on which aiohttp listens for requests.
        :param host: host on which to deploy the aiohttp app.
        :param events_per_second: how many times per second to check for new SSE
        event requests.
        """
        # Config
        self.port = port
        self.host = host
        self.events_per_second = events_per_second

        # Multiprocessing
        self._p = None
        self._event_queue = None
        self._config_queue = None
        self._config = None

        # App
        self._app = web.Application()
        self._app.add_routes([
            web.get('/config', self._get_config),  # Endpoint for getting config
            web.get('/event', self._event),        # Endpoint for EventSource
            web.get('/', self._index),             # Called by View to get index
            web.static('/', STATIC_DIR),           # Serves static files (.js, .png, .css, etc)
        ])

    def _main(self, event_queue, config_queue):
        """
        Main runner for the backend.
        """
        self._event_queue = event_queue
        self._config_queue = config_queue
        web.run_app(self._app, host=self.host, port=self.port)

    async def _index(self, request):
        """
        Callback for GET on /
        """
        return web.FileResponse(os.path.join(STATIC_DIR, 'index.html'))

    async def _get_config(self, request):
        """
        Calback for GET on /config
        """
        return web.Response(text=self._config)

    async def _event(self, request):
        """
        Callback for SSE GET on /event
        """
        loop = request.app.loop
        async with sse_response(request) as resp:
            while True:
                while True:
                    try:
                        event = self._event_queue.get(block=False)
                        await resp.send(event)
                    except:
                        break
                try:
                    new_config = self._config_queue.get(block=False)
                    if new_config:
                        self._config = new_config
                except:
                    pass

                data = json.dumps('NOP')
                await resp.send(data)
                await asyncio.sleep(1 / self.events_per_second, loop=loop)

    def start(self, event_queue, config_queue):
        """
        Starts the backend server.
        :param event_queue: multiprocessing.Manager.Queue object
        :param config_queue: multiprocessing.Manager.Queue object
        """
        self._p = Process(target=self._main, args=(event_queue, config_queue))
        self._p.start()

    def stop(self):
        """
        Kills the backend server.
        """
        print("Shutting down Pencil backend")
        self._p.terminate()

    def get_endpoint(self, name=None):
        """
        Returns full http path for the given endpoint.
        :param name: string (if None, returns path for /)
        """
        return 'http://{}:{}/{}'.format(self.host, self.port, name if name else '')
