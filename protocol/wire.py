"""Pack/unpack multi-field messages for UDP."""

import struct

def pack(*fields) -> bytes:
    """Packs multiple bytes fields into a single bytes object.
    Uses 4-byte length prefixes for each field."""
    result = bytearray()
    for field in fields:
        result.extend(struct.pack(">I", len(field)))
        result.extend(field)
    return bytes(result)

def unpack(data: bytes) -> tuple:
    """Unpacks a bytes object created by pack() into a tuple of fields."""
    fields = []
    offset = 0
    while offset < len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        offset += 4
        fields.append(data[offset:offset+length])
        offset += length
    return tuple(fields)
