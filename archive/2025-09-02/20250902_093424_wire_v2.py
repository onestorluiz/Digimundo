# -*- coding: utf-8 -*-
from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
import json, msgpack

SEP = "\x1F"  # US (unit separator), 1 byte

@dataclass
class Frame:
    op: str
    frm: str
    to: str
    payload: str

def encode_frame(op:str, frm:str, to:str, payload:str) -> bytes:
    return f"{op}{SEP}{frm}{SEP}{to}{SEP}{payload}\n".encode("utf-8")

def decode_frame(b: bytes) -> Frame:
    s = b.decode("utf-8")
    if s.endswith("\n"): s = s[:-1]
    op, frm, to, payload = s.split(SEP, 3)
    return Frame(op, frm, to, payload)

def encode_json(op:str, frm:str, to:str, payload:str) -> bytes:
    return json.dumps({"op":op,"from":frm,"to":to,"payload":payload}, separators=(",",":")).encode("utf-8")

def encode_msgpack(op:str, frm:str, to:str, payload:str) -> bytes:
    # chaves curtas 1 byte
    return msgpack.packb({"o":op,"f":frm,"t":to,"p":payload}, use_bin_type=True)