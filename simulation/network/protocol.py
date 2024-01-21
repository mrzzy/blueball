#
# blueball
# Simulation Package
# Network Protocol
#

from enum import Enum
import struct

# name of the protocol
from dataclasses import dataclass
from typing import ClassVar, Optional
from abc import (
    ABC,
    abstractclassmethod,
    abstractmethod,
    abstractproperty,
    abstractstaticmethod,
)


PROTOCOL_NAME = "blueball"
PROTOCOL_PORT = 8234


class PacketKind(Enum):
    Unknown = 0
    RegisterRequest = 1
    RegisterResponse = 2


class Serializable(ABC):
    """Abstract type for objects Serializable to / from bytes"""

    @abstractmethod
    def to_bytes(self) -> bytes:
        pass

    @staticmethod
    @abstractmethod
    def from_bytes(b: bytes):
        pass


class Payload(Serializable):
    """Abstract Blueball Packet payload"""

    @abstractproperty
    def kind(self) -> PacketKind:
        """Returns string identifying kind of packet payload"""
        return PacketKind.Unknown


@dataclass
class Packet(Serializable):
    """Blueball protocol packet"""

    ENCODING: ClassVar[str] = "!B"

    payload: Payload

    def to_bytes(self) -> bytes:
        return struct.pack(Packet.ENCODING, self.payload.kind.value) + self.payload.to_bytes()

    @staticmethod
    def from_bytes(b: bytes):
        # decode payload kind
        header_len = struct.calcsize(Packet.ENCODING)
        (kind_int,) = struct.unpack(Packet.ENCODING, b[:header_len])
        kind = PacketKind(kind_int)

        if kind == PacketKind.RegisterRequest:
            payload = RegisterRequest.from_bytes(b[header_len:])
        elif kind == PacketKind.RegisterResponse:
            payload = RegisterResponse.from_bytes(b[header_len:])
        else:
            raise ValueError(f"Decode unupported payload type: {kind.name}")

        return Packet(payload)


# Register Flow
@dataclass
class RegisterRequest(Payload):
    """Request to register with the server and obtain a client ID.

    This request is sent on all new stream connections established.


    Attributes:
        client_id:
            Optional. Clients seeking to restablish a dropped connection should pass
            the client ID previousily assigned to it by the server. Otherwise
            the server will assume that the client is new.
    """

    ENCODING: ClassVar[str] = "!I"

    client_id: Optional[int] = None

    @property
    def kind(self) -> PacketKind:
        return PacketKind.RegisterRequest

    def to_bytes(self) -> bytes:
        return (
            b""
            if self.client_id is None
            else struct.pack(RegisterRequest.ENCODING, self.client_id)
        )

    @staticmethod
    def from_bytes(b: bytes) -> "RegisterRequest":
        if len(b) == 0:
            client_id = None
        else:
            (client_id,) = struct.unpack(RegisterRequest.ENCODING, b)
        return RegisterRequest(client_id=client_id)


@dataclass
class RegisterResponse(Payload):
    """Response to a register request from the server.

    Attributes:
        client_id:
            client ID assigned to the client ID by the server. Client should attach
            client ID in any future correspondence with the server identify themselves.
    """

    ENCODING: ClassVar[str] = "!I"
    client_id: int

    @property
    def kind(self) -> PacketKind:
        return PacketKind.RegisterResponse

    def to_bytes(self) -> bytes:
        return struct.pack(RegisterResponse.ENCODING, self.client_id)

    @staticmethod
    def from_bytes(b: bytes) -> "RegisterResponse":
        (client_id,) = struct.unpack(RegisterResponse.ENCODING, b)
        return RegisterResponse(client_id=client_id)
