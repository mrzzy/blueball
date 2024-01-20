#
# blueball
# Server
#

import logging
import asyncio
from argparse import ArgumentParser

from logfmter.formatter import Logfmter
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent
from aioquic.quic.logger import QuicLogger, QuicLoggerTrace
from aioquic.asyncio.server import serve

from network import PROTOCOL_NAME, PROTOCOL_PORT, QuicStdoutLogger


class Player:
    """Tracks a single game player in the multiplayer game setting."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer

async def main():
    # parse command line arguments
    parser = ArgumentParser(description="Blueball game server")
    parser.add_argument(
        "-a",
        "--address",
        type=str,
        default="127.0.0.1",
        help="Listen requests on the specified address",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=PROTOCOL_PORT,
        help="Listen for requests on the specified port",
    )
    parser.add_argument(
        "-c",
        "--certificate",
        type=str,
        required=True,
        help="load the TLS certificate from the specified file",
    )
    parser.add_argument(
        "-k",
        "--private-key",
        type=str,
        required=True,
        help="load the TLS private key from the specified file",
    )
    parser.add_argument(
        "-l",
        "--log",
        type=str,
        default="/dev/stdout",
        help="Path to write log requests",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=bool,
        default=False,
        help="Whether to log verbose debug messages",
    )
    args = parser.parse_args()

    # setup logger
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(Logfmter())
    logging.basicConfig(
        handlers=[log_handler],
        level=logging.INFO if args.verbose == False else logging.DEBUG,
    )

    # bootstrap server
    config = QuicConfiguration(
        is_client=False,
        alpn_protocols=[PROTOCOL_NAME],
        quic_logger=QuicStdoutLogger(),
    )
    config.load_cert_chain(args.certificate, args.private_key)

    players: list[Player] = []

    def new_player(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        players.append(Player(reader, writer))
        logging.info("New player registered.")

    await serve(
        host=args.address,
        port=args.port,
        configuration=config,
        stream_handler=new_player,
    )

    # serve requests from users
    while True:
        if len(players) >= 1 and not players[0]._reader.at_eof():
            x = await players[0]._reader.read()
            logging.info(f"GOT: {x}")
        await asyncio.sleep(0.001)


if __name__ == "__main__":
    # bootstrap quic server
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ctrl-c: exit
        pass
