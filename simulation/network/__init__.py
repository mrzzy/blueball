#
# blueball
# Simulation Package
# Networking
#

import asyncio
from contextlib import AbstractContextManager
from dataclasses import dataclass
import logging
import ssl
from threading import Thread
from typing import cast
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent
from aioquic.quic.logger import QuicLogger, QuicLoggerTrace

from network.protocol import (
    PROTOCOL_NAME,
    PROTOCOL_PORT,
    Packet,
    Payload,
    RegisterRequest,
    RegisterResponse,
)


class QuicStdoutLogger(QuicLogger):
    """Implementation of QuicLogger that logs to stdout"""

    def end_trace(self, trace: QuicLoggerTrace) -> None:
        logging.debug(trace.to_dict(), extra={"kind": "request"})


async def _write(writer: asyncio.StreamWriter, b: bytes):
    writer.write(b)
    writer.write_eof()
    await writer.drain()


class BlueballClient(AbstractContextManager):
    """Client to communicate blueball server for multiplayer functionality."""

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.client_id = None

    def __enter__(self) -> "BlueballClient":
        # run asyncio loop in separate thread
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        def loop_async(loop: asyncio.AbstractEventLoop):
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()

        # mark thread as daemonic to allow program to exit when this thread is running
        self._thread = Thread(target=loop_async, args=(self._loop,), daemon=True)
        self._thread.start()

        # connect to server & establish a stream
        self._context = connect(
            self.address,
            self.port,
            configuration=QuicConfiguration(
                is_client=True,
                alpn_protocols=[PROTOCOL_NAME],
                verify_mode=ssl.CERT_NONE,
                quic_logger=QuicStdoutLogger(),
            ),
            create_protocol=QuicConnectionProtocol,
        )
        self._conn = cast(
            QuicConnectionProtocol,
            asyncio.run_coroutine_threadsafe(
                self._context.__aenter__(),
                self._loop,
            ).result(),
        )
        self._reader, self._writer = asyncio.run_coroutine_threadsafe(
            self._conn.create_stream(), self._loop
        ).result()

        # register with the serve
        self.register()

        return self

    def _send(self, payload: Payload):
        """Send a packet with the given payload to server"""
        asyncio.run_coroutine_threadsafe(
            _write(self._writer, Packet(payload).to_bytes()), self._loop
        )

    def _recieve(self) -> Payload:
        """Receive a packet with a payload from the server"""
        p = Packet.from_bytes(
            asyncio.run_coroutine_threadsafe(self._reader.read(), self._loop).result()
        )
        return p.payload

    def register(self):
        """Register client with the server"""
        self._send(RegisterRequest(client_id=self.client_id))
        self.client_id = cast(RegisterResponse, self._recieve()).client_id
        logging.info(f"Registered as client id: {self.client_id}")

    def __exit__(self, _e, _v, _t):
        asyncio.run_coroutine_threadsafe(
            self._context.__aexit__(None, None, None), self._loop
        ).result()


if __name__ == "__main__":
    with BlueballClient("127.0.0.1", PROTOCOL_PORT) as client:
        print(client.client_id)
