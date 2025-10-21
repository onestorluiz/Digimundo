from src.telepathy.wire_v2 import encode_frame, decode_frame, encode_json, encode_msgpack

def test_frame_roundtrip():
    b = encode_frame("MSG","A","B","hello")
    f = decode_frame(b)
    assert (f.op,f.frm,f.to,f.payload)==("MSG","A","B","hello")

def test_json_msgpack_not_crash():
    assert encode_json("MSG","A","B","x")
    assert encode_msgpack("MSG","A","B","x")