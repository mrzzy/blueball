#
# blueball
# Simulation Package
# Network Protocol
#

import asyncio
import logging
import ssl
from threading import Thread
from typing import cast
from aioquic.asyncio.client import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent
from aioquic.quic.logger import QuicLogger, QuicLoggerTrace


# name of the protocol
PROTOCOL_NAME = "blueball"
PROTOCOL_PORT = 8234


class QuicStdoutLogger(QuicLogger):
    """Implementation of QuicLogger that logs to stdout"""

    def end_trace(self, trace: QuicLoggerTrace) -> None:
        logging.debug(trace.to_dict(), extra={"kind": "request"})


class BlueballClient:
    """Client to communicate blueball server for multiplayer functionality."""

    def __init__(self, host: str, port: int):
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
            host,
            port,
            configuration=QuicConfiguration(
                is_client=True,
                alpn_protocols=[PROTOCOL_NAME],
                verify_mode=ssl.CERT_NONE,
                quic_logger=QuicStdoutLogger(),
            ),
            create_protocol=QuicConnectionProtocol,
        )
        self._conn = cast(QuicConnectionProtocol, asyncio.run_coroutine_threadsafe(
            self._context.__aenter__(),
            self._loop,
        ).result())
        self._reader, self._writer = asyncio.run_coroutine_threadsafe(
            self._conn.create_stream(), self._loop
        ).result()

    def test(self):
        self._writer.write(b"blah blah blah")
        asyncio.run_coroutine_threadsafe(self._writer.drain(), self._loop)

    def close(self):
        asyncio.run_coroutine_threadsafe(self._context.__aexit__(None, None, None), self._loop).result()


if __name__ == "__main__":
    c = BlueballClient("127.0.0.1", PROTOCOL_PORT)
    c.test()
    c.close()
