
# digilang_v3_ta_lib_example.py
# Example: library-style usage of DigiLang v3-TA
#
# 1) Encode a piece of screenplay text (selects token-aware macros automatically)
# 2) Reuse the header across turns in a session (so you don't pay for it every call)
# 3) Decode back to original (round-trip)

from digilang_v3_ta import encode_text, decode_text, SEED_EXPANSIONS, encode_body

# --- Simulated 'session' store for header and mapping ---
SESSION = {
    "header": None,      # str with MACROS_BEGIN...MACROS_END
    "mapping": None,     # dict {placeholder -> expansion}
}

def first_turn_send_to_llm(raw_text: str):
    # Encode with default seeds; will auto-pick only beneficial macros
    encoded_text, mapping, metrics, winners = encode_text(raw_text, SEED_EXPANSIONS, max_macros=64)

    # Split header and body for reuse
    marker = "\nMACROS_END\n"
    header_end_idx = encoded_text.find(marker)
    if header_end_idx == -1:
        # No header (no macros selected), simulate empty header block
        header = "MACROS_BEGIN\nMACROS_END\n"
        body   = encoded_text
    else:
        header = encoded_text[:header_end_idx + len(marker)]
        body   = encoded_text[header_end_idx + len(marker):]

    # Store for later turns
    SESSION["header"] = header
    SESSION["mapping"] = mapping

    print("=== FIRST TURN ===")
    print("--- Header (send once at start of session) ---")
    print(header)
    print("--- Body (send with your task prompt) ---")
    print(body[:600] + ("..." if len(body) > 600 else ""))
    print("--- Metrics ---", metrics)
    return header, body, metrics

def next_turn_send_only_body(new_raw_text: str):
    # Reuse header already in the LLM conversation context; only encode body
    if not SESSION["mapping"] or not SESSION["header"]:
        raise RuntimeError("Session header/mapping not initialized. Call first_turn_send_to_llm() first.")

    encoded_body = encode_body(new_raw_text, SESSION["mapping"], ignore_case=True)

    print("=== NEXT TURN ===")
    print("--- Body only (since header is already in context) ---")
    print(encoded_body[:600] + ("..." if len(encoded_body) > 600 else ""))
    return encoded_body

def decode_from_llm(encoded_text_or_body: str, header: str = None):
    """If you sent header+body together, pass the full string.
       If you sent only body (header was already in context), reconstruct a temporary full text for decode.
    """
    if header is None:
        if SESSION["header"] is None:
            raise RuntimeError("No header available in session; cannot decode body alone.")
        full = SESSION["header"] + encoded_text_or_body
    else:
        full = encoded_text_or_body  # already full

    original = decode_text(full)
    print("=== DECODED ORIGINAL ===")
    print(original[:600] + ("..." if len(original) > 600 else ""))
    return original

if __name__ == "__main__":
    raw_1 = """\
FADE IN:

INT. CAFÉ - DAY

    JOHN está sentado em uma mesa.
    Ele olha para a porta.

CUT TO:
"""
    # First turn: send header+body
    header, body, metrics = first_turn_send_to_llm(raw_1)

    # Next turn: only body (header is already in the conversation history of the LLM)
    raw_2 = """\
EXT. RUA - NIGHT

    MARY, sussurrando, olha para JOHN.
"""
    encoded_body_2 = next_turn_send_only_body(raw_2)

    # Decode examples
    _ = decode_from_llm(header + body)       # when you sent both
    _ = decode_from_llm(encoded_body_2)      # when you sent only body (header reused)
