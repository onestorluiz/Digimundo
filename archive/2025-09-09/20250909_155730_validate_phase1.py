#!/usr/bin/env python3
import re

# Check help output
with open("reports/harmony_vFinal/system_audit/phase1_help.txt") as f:
    help_text = f.read()
    has_status = "status" in help_text.lower()
    has_analyze = "analyze" in help_text.lower()
    has_backup = "backup" in help_text.lower()
    has_chat = "chat" in help_text.lower() or "entering" in help_text.lower()
    
    print(f"Help validation:")
    print(f"  status: {'✅' if has_status else '❌'}")
    print(f"  analyze: {'✅' if has_analyze else '❌'}")
    print(f"  backup: {'✅' if has_backup else '❌'}")
    print(f"  chat: {'✅' if has_chat else '❌'}")

# Check status output
with open("reports/harmony_vFinal/system_audit/phase1_status.txt") as f:
    status_text = f.read()
    has_persona = "Persona:" in status_text
    has_mode = "Mode:" in status_text
    has_telepathy = bool(re.search(r"Telepathy:\s*(REDIS|FAKEREDIS|MOCK)", status_text, re.I))
    has_soulos = "SoulOS:" in status_text
    has_monitor = "Monitor:" in status_text
    has_memory = "Memory Manager:" in status_text or "canonical" in status_text.lower()
    
    print(f"\nStatus validation:")
    print(f"  Persona: {'✅' if has_persona else '❌'}")
    print(f"  Mode: {'✅' if has_mode else '❌'}")
    print(f"  Telepathy: {'✅' if has_telepathy else '❌'}")
    print(f"  SoulOS: {'✅' if has_soulos else '❌'}")
    print(f"  Monitor: {'✅' if has_monitor else '❌'}")
    print(f"  Memory: {'✅' if has_memory else '❌'}")
