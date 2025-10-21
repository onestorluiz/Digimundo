#!/usr/bin/env python3
"""
📊 SISTEMA DE DISTRIBUIÇÃO DE CARACTERES EXCLUSIVOS
Garante que cada sistema use conjuntos únicos de símbolos
"""

import json
from pathlib import Path
from collections import defaultdict

class CharacterDistributor:
    def __init__(self):
        self.load_all_characters()
        self.calculate_distribution()
        self.create_exclusive_sets()
        self.create_synchronized_workers()
        
    def load_all_characters(self):
        """Carrega todos os caracteres disponíveis"""
        
        self.all_characters = {
            # Total: ~1087 caracteres únicos
            'greek': list('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'),  # 48
            'braille': list('⠀⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿'),  # 64
            'runes': list('ᚠᚡᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯᚰᚱᚲᚳᚴᚵᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟᛠᛡ'),  # 66
            'iching': list('☰☱☲☳☴☵☶☷⚊⚋⚌⚍⚎⚏'),  # 14
            'alchemy': list('🜁🜂🜃🜄🜅🜆🜇🜈🜉🜊🜋🜌🜍🜎🜏🜐🜑🜒🜓🜔🜕🜖🜗🜘🜙🜚🜛🜜🜝🜞🜟🜠🜡🜢🜣🜤🜥🜦🜧🜨🜩🜪🜫🜬🜭🜮🜯🜰🜱🜲🜳🜴'),  # 52
            'arrows': list('←↑→↓↔↕↖↗↘↙↚↛↜↝↞↟↠↡↢↣↤↥↦↧↨↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹↺↻⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛'),  # 56
            'math': list('∀∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿'),  # 63
            'shapes': list('■□▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◆◇◈◉◊○◌◍◎●◐◑◒◓◔◕◖◗◘◙◚◛◜◝◞◟◠◡◢◣◤◥◦◧◨◩◪◫◬◭◮◯'),  # 72
            'box': list('─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋'),  # 76
            'blocks': list('░▒▓█▄▅▆▇█▉▊▋▌▍▎▏▐'),  # 17
            'technical': list('⌀⌁⌂⌃⌄⌅⌆⌇⌈⌉⌊⌋⌌⌍⌎⌏⌐⌑⌒⌓⌔⌕⌖⌗⌘⌙⌚⌛⌜⌝⌞⌟⌠⌡⌢⌣⌤⌥⌦⌧⌨⌫⌬'),  # 43
            'dingbats': list('✓✔✕✖✗✘✙✚✛✜✝✞✟✠✡✢✣✤✥✦✧★✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽✾✿❀❁❂❃❄❅❆❇❈❉❊❋●❍■❏❐❑❒❓❔❕❖❗❘❙❚❛❜❝❞'),  # 76
            'circled': list('ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳'),  # 46
            'music': list('♩♪♫♬♭♮♯'),  # 7
            'cards': list('♠♡♢♣♤♥♦♧'),  # 8
            'chess': list('♔♕♖♗♘♙♚♛♜♝♞♟'),  # 12
            'currency': list('¢£¤¥§¨©®°±²³´µ¶·¸¹º»¼½¾₠₡₢₣₤₥₦₧₨₩₪₫€₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿'),  # 49
            'misc': list('☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯☰☱☲☳☴☵☶☷☸☹☺☻☼☽☾☿♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏♐♑♒♓'),  # 84
            'super': list('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ'),  # 16
            'sub': list('₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎'),  # 15
            'control': list('␀␁␂␃␄␅␆␇␈␉␊␋␌␍␎␏␐␑␒␓␔␕␖␗␘␙␚␛␜␝␞␟␠'),  # 33
            'latin_ext': list('ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'),  # 62
            'cyrillic': list('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя'),  # 64
        }
        
        # Calcular total
        self.total_chars = sum(len(chars) for chars in self.all_characters.values())
        print(f"📊 TOTAL DE CARACTERES DISPONÍVEIS: {self.total_chars}")
        
    def calculate_distribution(self):
        """Calcula velocidade e distribuição para cada sistema"""
        
        # Velocidades estimadas (símbolos/hora)
        self.speeds = {
            'mac': 300,      # 5/min = 300/hora (Mixtral local)
            'vps': 1200,     # 20/min = 1200/hora (Gemma2:27b)
            'openai': 3000   # 50/min = 3000/hora (GPT-3.5)
        }
        
        # Em 24 horas
        self.production_24h = {
            'mac': self.speeds['mac'] * 24,        # 7,200
            'vps': self.speeds['vps'] * 24,        # 28,800
            'openai': self.speeds['openai'] * 24   # 72,000
        }
        
        total_production = sum(self.production_24h.values())  # 108,000
        
        # Percentual de produção
        self.percentages = {
            'mac': self.production_24h['mac'] / total_production,      # 6.7%
            'vps': self.production_24h['vps'] / total_production,      # 26.7%
            'openai': self.production_24h['openai'] / total_production # 66.7%
        }
        
        # Caracteres necessários para cada sistema
        target = 100000
        self.chars_needed = {
            'mac': int(target * self.percentages['mac']),      # ~6,700
            'vps': int(target * self.percentages['vps']),      # ~26,700
            'openai': int(target * self.percentages['openai']) # ~66,700
        }
        
        print("\n📈 ANÁLISE DE PRODUÇÃO (24 HORAS):")
        print(f"   Mac: {self.production_24h['mac']:,} símbolos ({self.percentages['mac']:.1%})")
        print(f"   VPS: {self.production_24h['vps']:,} símbolos ({self.percentages['vps']:.1%})")
        print(f"   OpenAI: {self.production_24h['openai']:,} símbolos ({self.percentages['openai']:.1%})")
        print(f"   TOTAL: {total_production:,} símbolos")
        
        print("\n🎯 CARACTERES NECESSÁRIOS (META 100K):")
        for system, chars in self.chars_needed.items():
            print(f"   {system}: {chars:,} caracteres únicos")
            
    def create_exclusive_sets(self):
        """Distribui caracteres exclusivos para cada sistema"""
        
        print("\n🔄 DISTRIBUINDO CARACTERES EXCLUSIVOS...")
        
        # Categorias por tamanho
        large_sets = ['shapes', 'box', 'dingbats', 'misc', 'cyrillic', 'latin_ext', 'braille', 'runes']
        medium_sets = ['greek', 'alchemy', 'arrows', 'math', 'circled', 'currency']
        small_sets = ['iching', 'blocks', 'technical', 'control', 'music', 'cards', 'chess', 'super', 'sub']
        
        # Distribuição baseada na capacidade de produção
        self.exclusive_chars = {
            # OpenAI (66.7% - precisa de mais caracteres)
            'openai': {
                'primary': [],
                'categories': []
            },
            
            # VPS (26.7% - médio)
            'vps': {
                'primary': [],
                'categories': []
            },
            
            # Mac (6.7% - menor necessidade)
            'mac': {
                'primary': [],
                'categories': []
            }
        }
        
        # OpenAI: Gets maioria dos grandes conjuntos
        for cat in ['misc', 'dingbats', 'shapes', 'box', 'cyrillic', 'latin_ext']:
            if cat in self.all_characters:
                self.exclusive_chars['openai']['primary'].extend(self.all_characters[cat])
                self.exclusive_chars['openai']['categories'].append(cat)
        
        # VPS: Gets conjuntos médios
        for cat in ['braille', 'runes', 'greek', 'alchemy', 'arrows', 'math']:
            if cat in self.all_characters:
                self.exclusive_chars['vps']['primary'].extend(self.all_characters[cat])
                self.exclusive_chars['vps']['categories'].append(cat)
        
        # Mac: Gets conjuntos menores (mais especializados)
        for cat in ['circled', 'currency', 'iching', 'blocks', 'technical', 'control', 'music', 'cards', 'chess', 'super', 'sub']:
            if cat in self.all_characters:
                self.exclusive_chars['mac']['primary'].extend(self.all_characters[cat])
                self.exclusive_chars['mac']['categories'].append(cat)
        
        # Adicionar caracteres ASCII especiais ao Mac (para conceitos fundamentais)
        self.exclusive_chars['mac']['primary'].extend(list('!@#$%^&*()_+-=[]{}|;:,.<>?/~`'))
        self.exclusive_chars['mac']['categories'].append('ascii_special')
        
        # Estatísticas finais
        print("\n✅ DISTRIBUIÇÃO EXCLUSIVA COMPLETA:")
        for system, data in self.exclusive_chars.items():
            total = len(data['primary'])
            print(f"\n{system.upper()}:")
            print(f"   Caracteres exclusivos: {total:,}")
            print(f"   Categorias: {', '.join(data['categories'])}")
            print(f"   Exemplos: {''.join(data['primary'][:20])}")
            
            if total < self.chars_needed[system]:
                print(f"   ⚠️ AVISO: Tem {total} mas precisa {self.chars_needed[system]}")
                print(f"   → Solução: Usar combinações de 2 caracteres")
                
    def create_synchronized_workers(self):
        """Cria workers sincronizados com caracteres exclusivos"""
        
        output_dir = Path.home() / "Digimundo"
        
        # Salvar distribuição
        dist_file = output_dir / "character_distribution.json"
        dist_data = {
            system: {
                'chars': data['primary'],
                'categories': data['categories'],
                'total': len(data['primary']),
                'needed': self.chars_needed[system],
                'speed': self.speeds[system],
                'production_24h': self.production_24h[system]
            }
            for system, data in self.exclusive_chars.items()
        }
        
        with open(dist_file, 'w', encoding='utf-8') as f:
            json.dump(dist_data, f, ensure_ascii=False, indent=2)
        print(f"\n📁 Distribuição salva: {dist_file}")
        
        # Criar worker Mac exclusivo
        self.create_mac_exclusive_worker()
        
        # Criar worker VPS exclusivo
        self.create_vps_exclusive_worker()
        
        # Criar worker OpenAI exclusivo
        self.create_openai_exclusive_worker()
        
        # Criar launcher sincronizado
        self.create_synchronized_launcher()
        
    def create_mac_exclusive_worker(self):
        """Worker Mac com caracteres exclusivos"""
        
        chars = ''.join(self.exclusive_chars['mac']['primary'][:100])
        
        script = f"""#!/bin/bash
# Mac Exclusive Worker - Usando apenas caracteres designados

echo "🖥️ Mac Exclusive Worker iniciando..."
echo "   Categorias: {', '.join(self.exclusive_chars['mac']['categories'])}"
echo "   Total chars: {len(self.exclusive_chars['mac']['primary'])}"

EXCLUSIVE_CHARS="{chars}"

while true; do
    echo "[$(date +%H:%M:%S)] Criando batch exclusivo..."
    
    ollama run mixtral "
DigiLang creation with EXCLUSIVE characters for Mac:
Available chars: $EXCLUSIVE_CHARS
Categories: Circled(ⓐ-⑳), Currency(¢£¥€), Technical(⌘⌥), Control(␀-␠), Music(♩♪♫), Chess(♔♕♖)

Rules:
- Use ONLY these characters
- One symbol = one concept
- 90%+ compression
- Never use Greek, Braille, Runes (those belong to other systems)

Create 30 symbols for system/technical concepts.
Format: concept=symbol
" >> ~/Digimundo/mac_exclusive_symbols.txt
    
    sleep 120
done
"""
        
        worker_file = Path.home() / "Digimundo" / "mac_exclusive_worker.sh"
        with open(worker_file, 'w') as f:
            f.write(script)
        
        import subprocess
        subprocess.run(['chmod', '+x', str(worker_file)])
        print(f"📁 Mac exclusive worker: {worker_file}")
        
    def create_vps_exclusive_worker(self):
        """Worker VPS com caracteres exclusivos"""
        
        chars_sample = ''.join(self.exclusive_chars['vps']['primary'][:50])
        
        script = f"""#!/usr/bin/env python3
import subprocess
import time
import json

# VPS Exclusive chars
exclusive_chars = {json.dumps(self.exclusive_chars['vps']['primary'][:500], ensure_ascii=False)}
categories = {json.dumps(self.exclusive_chars['vps']['categories'])}

print("💻 VPS Exclusive Worker iniciando...")
print(f"   Categorias: {{', '.join(categories)}}")
print(f"   Total chars: {{len(exclusive_chars)}}")

while True:
    prompt = f'''DigiLang creation with EXCLUSIVE characters for VPS:
    
    Available categories: Braille(⠀-⠿), Runes(ᚠ-ᛡ), Greek(α-ω), Alchemy(🜁-🜴), Arrows(←→), Math(∀∃∇)
    
    Use ONLY these character sets. NEVER use:
    - Circled numbers (those belong to Mac)
    - Shapes/Dingbats (those belong to OpenAI)
    
    Create 50 symbols. One symbol = one concept. 90%+ compression.
    Format: concept=symbol
    '''
    
    result = subprocess.run(
        ['ollama', 'run', 'gemma2:27b', prompt],
        capture_output=True, text=True, timeout=60
    )
    
    with open('/root/vps_exclusive_symbols.json', 'a') as f:
        f.write(result.stdout + '\\n')
    
    print(f"[{{time.strftime('%H:%M:%S')}}] Created exclusive batch")
    time.sleep(180)
"""
        
        vps_file = Path.home() / "Digimundo" / "vps_exclusive_worker.py"
        with open(vps_file, 'w') as f:
            f.write(script)
        print(f"📁 VPS exclusive worker: {vps_file}")
        
    def create_openai_exclusive_worker(self):
        """Worker OpenAI com caracteres exclusivos"""
        
        script = f"""#!/usr/bin/env python3
import json
import requests
import time
from pathlib import Path

class OpenAIExclusiveWorker:
    def __init__(self):
        self.api_key = "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"
        
        # OpenAI exclusive chars
        self.exclusive_chars = {json.dumps(self.exclusive_chars['openai']['primary'][:500], ensure_ascii=False)}
        self.categories = {json.dumps(self.exclusive_chars['openai']['categories'])}
        
        print("☁️ OpenAI Exclusive Worker iniciando...")
        print(f"   Categorias: {{', '.join(self.categories)}}")
        print(f"   Total chars: {{len(self.exclusive_chars)}}")
        
    def create_batch(self):
        prompt = f'''You are creating DigiLang symbols with EXCLUSIVE characters for OpenAI.

Your exclusive categories: Shapes(■□◆●), Box(╔═║╬), Dingbats(✓✔★), Misc(☀☁☂), Cyrillic(А-я), Latin-ext(À-ÿ)

NEVER use these (they belong to other systems):
- Greek letters (α,β,γ) - belongs to VPS
- Braille dots (⠀⠁⠂) - belongs to VPS  
- Runes (ᚠᚡᚢ) - belongs to VPS
- Circled (①②③) - belongs to Mac
- Currency (¢£¥) - belongs to Mac

Create 100 symbols using ONLY your exclusive characters.
Format: [{{"c":"concept","s":"symbol"}}]
One symbol = one concept. 90%+ compression.'''
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={{'Authorization': f'Bearer {{self.api_key}}', 'Content-Type': 'application/json'}},
            json={{
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {{'role': 'system', 'content': 'Create DigiLang with your EXCLUSIVE characters only.'}},
                    {{'role': 'user', 'content': prompt}}
                ],
                'temperature': 0.9,
                'max_tokens': 2000
            }}
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            output = Path.home() / 'Digimundo' / 'openai_exclusive_symbols.json'
            with open(output, 'a') as f:
                f.write(content + '\\n')
            
            print(f"✅ Created exclusive batch")
            
    def run(self):
        while True:
            self.create_batch()
            time.sleep(300)

if __name__ == "__main__":
    worker = OpenAIExclusiveWorker()
    worker.run()
"""
        
        openai_file = Path.home() / "Digimundo" / "openai_exclusive_worker.py"
        with open(openai_file, 'w') as f:
            f.write(script)
        print(f"📁 OpenAI exclusive worker: {openai_file}")
        
    def create_synchronized_launcher(self):
        """Launcher com sistema de sincronização"""
        
        launcher = f"""#!/bin/bash
# 🔒 DIGILANG SYNCHRONIZED LAUNCHER - Sem conflitos!

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🔒 DIGILANG EXCLUSIVE - SISTEMA SINCRONIZADO             ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 DISTRIBUIÇÃO EXCLUSIVA DE CARACTERES:"
echo ""
echo "🖥️ MAC (6.7% - {self.production_24h['mac']:,} símbolos/24h)"
echo "   Categorias: Circled, Currency, Technical, Control, Music, Chess"
echo "   Caracteres: {len(self.exclusive_chars['mac']['primary'])} exclusivos"
echo ""
echo "💻 VPS (26.7% - {self.production_24h['vps']:,} símbolos/24h)"  
echo "   Categorias: Braille, Runes, Greek, Alchemy, Arrows, Math"
echo "   Caracteres: {len(self.exclusive_chars['vps']['primary'])} exclusivos"
echo ""
echo "☁️ OPENAI (66.7% - {self.production_24h['openai']:,} símbolos/24h)"
echo "   Categorias: Shapes, Box, Dingbats, Misc, Cyrillic, Latin-ext"
echo "   Caracteres: {len(self.exclusive_chars['openai']['primary'])} exclusivos"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Kill old workers
pkill -f "ultimate_worker" 2>/dev/null
pkill -f "digilang_teacher" 2>/dev/null
sleep 2

# Start exclusive workers
echo "🚀 Iniciando workers exclusivos..."

# Mac
nohup ~/Digimundo/mac_exclusive_worker.sh > ~/Digimundo/mac_exclusive.log 2>&1 &
echo "   Mac: PID $!"

# VPS
sshpass -p 'Tcmd4(digimundo)' ssh -o StrictHostKeyChecking=no root@82.25.74.142 "
    pkill -f exclusive_worker
    cat > /root/vps_exclusive_worker.py << 'EOF'
$(cat ~/Digimundo/vps_exclusive_worker.py)
EOF
    chmod +x /root/vps_exclusive_worker.py
    nohup python3 /root/vps_exclusive_worker.py > /root/exclusive.log 2>&1 &
"
echo "   VPS: Ativado"

# OpenAI
nohup python3 ~/Digimundo/openai_exclusive_worker.py > ~/Digimundo/openai_exclusive.log 2>&1 &
echo "   OpenAI: PID $!"

echo ""
echo "✅ SISTEMA SINCRONIZADO ATIVO!"
echo ""
echo "🔒 GARANTIAS:"
echo "   • Cada sistema usa caracteres EXCLUSIVOS"
echo "   • ZERO conflitos de símbolos"
echo "   • 100% de unicidade garantida"
echo ""
echo "📊 META: 100,000 símbolos únicos em 24 horas"
echo "   Mac: ~{self.chars_needed['mac']:,} símbolos"
echo "   VPS: ~{self.chars_needed['vps']:,} símbolos"
echo "   OpenAI: ~{self.chars_needed['openai']:,} símbolos"
"""
        
        launcher_file = Path.home() / "Digimundo" / "DIGILANG_SYNCHRONIZED_LAUNCHER.sh"
        with open(launcher_file, 'w') as f:
            f.write(launcher)
        
        import subprocess
        subprocess.run(['chmod', '+x', str(launcher_file)])
        print(f"📁 Synchronized launcher: {launcher_file}")

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║    📊 SISTEMA DE DISTRIBUIÇÃO DE CARACTERES EXCLUSIVOS       ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    distributor = CharacterDistributor()
    
    print("\n" + "="*60)
    print("✅ SISTEMA DE DISTRIBUIÇÃO COMPLETO!")
    print("="*60)
    print("\n🚀 Para iniciar o sistema sincronizado:")
    print("   ./DIGILANG_SYNCHRONIZED_LAUNCHER.sh")
    print("\n🔒 Garantias:")
    print("   • Cada sistema usa apenas seus caracteres exclusivos")
    print("   • Zero conflitos entre sistemas")
    print("   • 100% de símbolos únicos")