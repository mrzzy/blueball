#
# blueball
# Server
#

import logging
import asyncio
from argparse import ArgumentParser
from typing import cast

from logfmter.formatter import Logfmter
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent
from aioquic.quic.logger import QuicLogger, QuicLoggerTrace
from aioquic.asyncio.server import serve

from network import PROTOCOL_NAME, PROTOCOL_PORT, QuicStdoutLogger, _write
from network.protocol import Packet, PacketKind, RegisterRequest, RegisterResponse


class Client:
    """Client in served by the Blueball Server"""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer


async def register(clients: list[Client], client: Client):
    """Client registration request flow"""
    # parse expected register packet from client
    p = Packet.from_bytes(await client.reader.read())
    if p.payload.kind != PacketKind.RegisterRequest:
        logging.error("Client failed to register.")

    request = cast(RegisterRequest, p.payload)
    if request.client_id is None:
        # new client registering
        client_id = len(clients)
        clients.append(client)
    else:
        # existing client restablishing stream connection
        client_id = request.client_id
        clients[client_id] = client

    # reply with client_id
    await _write(client.writer, Packet(RegisterResponse(client_id)).to_bytes())


def parse_args():
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
    return parser.parse_args()


async def main():
    args = parse_args()

    # setup logger
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(Logfmter())
    logging.basicConfig(
        handlers=[log_handler],
        level=logging.INFO if args.verbose == False else logging.DEBUG,
    )

    # bootstrap quic server
    config = QuicConfiguration(
        is_client=False,
        alpn_protocols=[PROTOCOL_NAME],
        quic_logger=QuicStdoutLogger(),
    )
    config.load_cert_chain(args.certificate, args.private_key)

    clients = []

    def new_stream(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        asyncio.get_event_loop().create_task(register(clients, Client(reader, writer)))

    await serve(
        host=args.address,
        port=args.port,
        configuration=config,
        stream_handler=new_stream,
    )

    logging.info("Server listening", extra={"address": args.address, "port": args.port})

    # handle requests from users
    await asyncio.Future()
    # while True:
    #     await asyncio.sleep(0.001)


if __name__ == "__main__":
    # bootstrap quic server
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ctrl-c: exit
        pass
