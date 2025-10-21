#!/usr/bin/env python
"""Enhanced wire protocol for telepathy messaging with DigiLang integration"""

import struct
import msgpack
import json
from typing import Dict, Any, Tuple

# Frame separator
SEP = chr(31)  # Unit separator

def encode_frame(op: str, frm: str, to: str, payload: str) -> bytes:
    """Encode a frame: OP␟FROM␟TO␟PAYLOAD\n"""
    frame = f"{op}{SEP}{frm}{SEP}{to}{SEP}{payload}\n"
    return frame.encode('utf-8')

def decode_frame(data: bytes) -> Tuple[str, str, str, str]:
    """Decode a frame"""
    text = data.decode('utf-8').strip()
    parts = text.split(SEP)
    if len(parts) != 4:
        raise ValueError(f"Invalid frame: {text}")
    return parts[0], parts[1], parts[2], parts[3]

def encode_msgpack(obj: Dict[str, Any]) -> bytes:
    """Encode object with MessagePack using 1-byte keys"""
    # Map to short keys
    short_keys = {
        'type': 't',
        'act': 'a',
        'scene': 's',
        'characters': 'c',
        'action': 'x',
        'emotion': 'e',
        'timestamp': 'ts'
    }
    
    compact = {}
    for k, v in obj.items():
        compact[short_keys.get(k, k[:1])] = v
    
    return msgpack.packb(compact)

def decode_msgpack(data: bytes) -> Dict[str, Any]:
    """Decode MessagePack with short keys"""
    compact = msgpack.unpackb(data)
    
    # Map back to full keys
    full_keys = {
        't': 'type',
        'a': 'act',
        's': 'scene',
        'c': 'characters',
        'x': 'action',
        'e': 'emotion',
        'ts': 'timestamp'
    }
    
    result = {}
    for k, v in compact.items():
        result[full_keys.get(k, k)] = v
    
    return result

def encode_digilang_message(message: Dict[str, Any]) -> str:
    """Encode message payload using DigiLang compression."""
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        
        from digilang.encoder import DigiLangEncoder
        encoder = DigiLangEncoder()
        
        # Create narrative-aware compressed representation
        components = []
        
        # Add structural markers
        if 'act' in message:
            act_num = message['act']
            if act_num == 1: components.append("\"H")  # FADE_IN symbol
            elif act_num == 2: components.append("\"#")  # BEAT_MIDPOINT symbol  
            elif act_num == 3: components.append("\"(")  # BEAT_FINALE symbol
        
        if 'scene' in message:
            scene_ref = encoder.encode_entity('SCENE', message['scene'])
            components.append(scene_ref)
        
        # Add character references
        if 'characters' in message and isinstance(message['characters'], list):
            for i, char in enumerate(message['characters']):
                char_ref = encoder.encode_entity('PERSONA', hash(char) % 1000)  # Simple hash for demo
                components.append(char_ref)
        
        # Add emotional/action context
        if 'emotion' in message:
            emotion = message['emotion'].upper()
            if 'ANGER' in emotion: components.append("#@")  # TENSION symbol
            elif 'LOVE' in emotion: components.append("%@")  # ROMANCE symbol
            elif 'FEAR' in emotion: components.append("%=")  # THRILLER symbol
        
        # Compress main action/text
        action_text = message.get('action', '')
        if action_text:
            compressed_action, _ = encoder.encode(action_text)
            components.append(compressed_action)
        
        return ' '.join(components) if components else json.dumps(message, separators=(',', ':'))
        
    except ImportError:
        # Fallback to compact JSON if DigiLang not available
        return json.dumps(message, separators=(',', ':'))

def create_wire_message_digilang(op: str, from_entity: str, to_entity: str, message_data: Dict[str, Any]) -> bytes:
    """Create wire protocol message with DigiLang-compressed payload."""
    compressed_payload = encode_digilang_message(message_data)
    return encode_frame(op, from_entity, to_entity, compressed_payload)

def estimate_wire_savings(message: Dict[str, Any]) -> float:
    """Estimate compression savings using wire+DigiLang vs JSON."""
    import json
    
    # JSON baseline
    json_bytes = len(json.dumps(message).encode('utf-8'))
    
    # Wire + DigiLang
    wire_payload = encode_digilang_message(message)
    wire_frame = encode_frame("MSG", "agent1", "agent2", wire_payload)
    wire_bytes = len(wire_frame)
    
    return 1 - (wire_bytes / json_bytes) if json_bytes > 0 else 0
