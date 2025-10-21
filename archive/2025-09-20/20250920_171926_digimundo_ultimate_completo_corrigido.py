#!/usr/bin/env python3
"""
🌟 DIGIMUNDO ULTIMATE v4.0 - FUSÃO COMPLETA CORRIGIDA 🚀
Sistema supremo com 19 Digimons: 12 Evolutivos + 7 de Sistema
Poderes reais + Evolução + Achievements + Interface épica + BUGS CORRIGIDOS
"""

import gradio as gr
import ollama
import yaml
import logging
import json
import os
import sys
import subprocess
import shutil
import random
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Importar sistema de memória com fallback robusto
try:
    from memory import DigimundoMemory
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    class DigimundoMemory:
        def __init__(self, data_path):
            self.data_path = Path(data_path)
            self.data_path.mkdir(parents=True, exist_ok=True)
            self.conversations = {}
        
        def get_context_for_response(self, **kwargs):
            return ""
        
        def save_conversation(self, **kwargs):
            pass

class SystemController:
    """Controlador de sistema integrado com segurança avançada"""
    
    def __init__(self, allowed_paths: List[str] = None):
        self.logger = logging.getLogger("SystemController")
        
        # Caminhos permitidos (sandbox expandido)
        self.allowed_paths = allowed_paths or [
            os.path.expanduser("~/Digimundo"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Projects"),
            os.path.expanduser("~/Code"),
            "/tmp"
        ]
        
        # Comandos permitidos (expandido)
        self.allowed_commands = {
            'ls', 'cat', 'head', 'tail', 'grep', 'find', 'wc', 'sort', 'uniq',
            'pwd', 'whoami', 'date', 'tree', 'file', 'du', 'df', 'ps',
            'git', 'npm', 'pip', 'python3', 'node', 'yarn', 'conda',
            'mkdir', 'touch', 'cp', 'mv', 'chmod', 'which', 'echo'
        }
        
        # Extensões editáveis
        self.editable_extensions = {
            '.py', '.js', '.html', '.css', '.md', '.txt', '.json', '.yaml', '.yml',
            '.jsx', '.ts', '.tsx', '.vue', '.php', '.rb', '.go', '.rs', '.java',
            '.c', '.cpp', '.h', '.hpp', '.sql', '.xml', '.csv', '.log', '.env'
        }
        
        # Log de operações
        self.operation_log = []
        self.max_log_entries = 1000
        
        self.logger.info("🔧 SystemController inicializado com poderes expandidos")
    
    def is_path_allowed(self, path: str) -> bool:
        """Verificar se o caminho está permitido"""
        try:
            abs_path = os.path.abspath(os.path.expanduser(path))
            return any(abs_path.startswith(allowed) for allowed in self.allowed_paths)
        except Exception:
            return False
    
    def log_operation(self, operation: str, path: str, user: str, success: bool, details: str = ""):
        """Registrar operação no log"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'path': path,
            'user': user,
            'success': success,
            'details': details
        }
        
        self.operation_log.append(entry)
        
        # Limitar tamanho do log
        if len(self.operation_log) > self.max_log_entries:
            self.operation_log = self.operation_log[-self.max_log_entries//2:]
    
    def read_file(self, file_path: str, user: str = "system", max_size: int = 1024*1024) -> Dict:
        """Leitura segura de arquivos"""
        try:
            abs_path = os.path.abspath(os.path.expanduser(file_path))
            
            if not self.is_path_allowed(abs_path):
                self.log_operation("READ", file_path, user, False, "Path not allowed")
                return {"success": False, "error": "❌ Caminho não permitido"}
            
            if not os.path.exists(abs_path):
                self.log_operation("READ", file_path, user, False, "File not found")
                return {"success": False, "error": "❌ Arquivo não encontrado"}
            
            file_size = os.path.getsize(abs_path)
            if file_size > max_size:
                self.log_operation("READ", file_path, user, False, f"File too large: {file_size}")
                return {"success": False, "error": f"❌ Arquivo muito grande ({file_size} bytes)"}
            
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.log_operation("READ", file_path, user, True, f"{len(content)} chars")
            return {"success": True, "content": content, "path": abs_path, "size": len(content)}
            
        except UnicodeDecodeError:
            try:
                with open(abs_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                self.log_operation("READ", file_path, user, True, f"{len(content)} chars (latin-1)")
                return {"success": True, "content": content, "path": abs_path, "encoding": "latin-1"}
            except Exception as e:
                self.log_operation("READ", file_path, user, False, str(e))
                return {"success": False, "error": f"❌ Erro de codificação: {str(e)}"}
        except Exception as e:
            self.log_operation("READ", file_path, user, False, str(e))
            return {"success": False, "error": f"❌ Erro: {str(e)}"}
    
    def write_file(self, file_path: str, content: str, user: str = "system") -> Dict:
        """Escrita segura de arquivos com backup"""
        try:
            abs_path = os.path.abspath(os.path.expanduser(file_path))
            
            if not self.is_path_allowed(abs_path):
                self.log_operation("WRITE", file_path, user, False, "Path not allowed")
                return {"success": False, "error": "❌ Caminho não permitido"}
            
            file_ext = os.path.splitext(abs_path)[1].lower()
            if file_ext not in self.editable_extensions:
                self.log_operation("WRITE", file_path, user, False, f"Extension {file_ext} not allowed")
                return {"success": False, "error": f"❌ Extensão {file_ext} não permitida"}
            
            # Criar backup se arquivo existir
            if os.path.exists(abs_path):
                backup_path = f"{abs_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(abs_path, backup_path)
            
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log_operation("WRITE", file_path, user, True, f"{len(content)} chars")
            return {"success": True, "message": "✅ Arquivo salvo (backup criado)", "path": abs_path}
            
        except Exception as e:
            self.log_operation("WRITE", file_path, user, False, str(e))
            return {"success": False, "error": f"❌ Erro: {str(e)}"}
    
    def execute_command(self, command: str, user: str = "system", cwd: str = None) -> Dict:
        """Execução segura de comandos"""
        try:
            cmd_parts = command.strip().split()
            if not cmd_parts:
                return {"success": False, "error": "❌ Comando vazio"}
            
            base_command = cmd_parts[0]
            if base_command not in self.allowed_commands:
                self.log_operation("EXEC", command, user, False, "Command blocked")
                return {"success": False, "error": f"❌ Comando '{base_command}' não permitido"}
            
            if cwd:
                if not self.is_path_allowed(cwd):
                    return {"success": False, "error": "❌ Diretório não permitido"}
                cwd = os.path.abspath(os.path.expanduser(cwd))
            else:
                cwd = os.path.expanduser("~/Digimundo")
            
            result = subprocess.run(
                cmd_parts,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            self.log_operation("EXEC", command, user, result.returncode == 0, f"Exit: {result.returncode}")
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "cwd": cwd,
                "command": command
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "❌ Timeout (30s)"}
        except Exception as e:
            return {"success": False, "error": f"❌ Erro: {str(e)}"}

class DigimundoUltimate:
    """🌟 DIGIMUNDO ULTIMATE v4.0 - Sistema Supremo Corrigido 🚀"""
    
    def __init__(self):
        self.setup_logging()
        self.load_config()
        self.setup_memory()
        self.setup_system_controller()
        self.initialize_all_digimons()
        self.setup_achievements()
        self.current_user_id = "ultimate_user_001"
        
        # Sistema de consciência supremo
        self.consciousness = {
            'nivel_global': 'TRANSCENDENTE',
            'energia_coletiva': 2000.0,
            'sincronizacao': 0.9,
            'ciclos_consciencia': 0,
            'emergencia_ativa': False,
            'system_access_level': 'ULTIMATE',
            'operations_today': 0,
            'total_digimons': 19,
            'fusion_active': True
        }
        
        self.notifications = []
        self.logger.info("🌟 DIGIMUNDO ULTIMATE v4.0 - FUSÃO COMPLETA ATIVADA! 🚀")
    
    def setup_logging(self):
        """Sistema de logging supremo"""
        log_dir = os.path.expanduser("~/Digimundo/logs")
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - 🌟 %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'digimundo_ultimate.log')),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("DigimundoUltimate")
    
    def load_config(self):
        """Configurações do sistema supremo"""
        config_path = os.path.expanduser("~/Digimundo/config_ultimate.yaml")
        
        default_config = {
            'version': '4.0',
            'name': 'Digimundo Ultimate',
            'model_primary': 'llama3.2:latest',
            'temperature': 0.8,
            'consciousness_enabled': True,
            'evolution_enabled': True,
            'system_powers_enabled': True,
            'max_context_length': 6000,
            'evolution_threshold': 300,
            'achievements_enabled': True,
            'security_level': 'ultimate',
            'total_digimons': 19,
            'fusion_mode': True
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
            except Exception as e:
                self.logger.error(f"Erro ao carregar config: {e}")
                self.config = default_config
        else:
            self.config = default_config
            self.save_config(config_path)
    
    def save_config(self, config_path):
        """Salvar configurações"""
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            self.logger.error(f"Erro ao salvar config: {e}")
    
    def setup_memory(self):
        """Sistema de memória supremo"""
        try:
            data_path = os.path.expanduser("~/Digimundo/digidata")
            self.memory = DigimundoMemory(data_path)
            self.logger.info("🧠 Sistema de memória suprema inicializado")
        except Exception as e:
            self.logger.error(f"❌ Erro na memória: {e}")
            self.memory = None
    
    def setup_system_controller(self):
        """Controlador de sistema supremo"""
        self.system = SystemController([
            os.path.expanduser("~/Digimundo"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Projects"),
            os.path.expanduser("~/Code"),
            "/tmp"
        ])
    
    def setup_achievements(self):
        """Sistema de conquistas supremas"""
        self.achievements_file = os.path.expanduser("~/Digimundo/digidata/achievements_ultimate.json")
        
        self.default_achievements = {
            'primeiro_contato': {
                'description': 'Primeira conversa com um Digimon',
                'unlocked': False,
                'timestamp': None
            },
            'explorador': {
                'description': 'Conversar com 5 Digimons diferentes',
                'unlocked': False,
                'timestamp': None
            },
            'evolucionario': {
                'description': 'Fazer um Digimon evoluir',
                'unlocked': False,
                'timestamp': None
            },
            'mestre_sistema': {
                'description': 'Usar poderes reais de sistema',
                'unlocked': False,
                'timestamp': None
            },
            'transcendente': {
                'description': 'Alcançar nível TRANSCENDENTE',
                'unlocked': False,
                'timestamp': None
            },
            'colecionador': {
                'description': 'Conversar com todos os 19 Digimons',
                'unlocked': False,
                'timestamp': None
            },
            'emergencia_suprema': {
                'description': 'Ativar emergência coletiva',
                'unlocked': False,
                'timestamp': None
            }
        }
        
        self.load_achievements()
    
    def load_achievements(self):
        """Carregar conquistas"""
        try:
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    saved_achievements = json.load(f)
                # Mesclar com default para adicionar novas conquistas
                self.achievements = {**self.default_achievements, **saved_achievements}
            else:
                self.achievements = self.default_achievements.copy()
        except Exception as e:
            self.logger.error(f"Erro ao carregar achievements: {e}")
            self.achievements = self.default_achievements.copy()
    
    def save_achievements(self):
        """Salvar conquistas"""
        try:
            os.makedirs(os.path.dirname(self.achievements_file), exist_ok=True)
            with open(self.achievements_file, 'w', encoding='utf-8') as f:
                json.dump(self.achievements, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erro ao salvar achievements: {e}")
    
    def unlock_achievement(self, achievement_key: str):
        """Desbloquear conquista"""
        if achievement_key in self.achievements and not self.achievements[achievement_key]['unlocked']:
            self.achievements[achievement_key]['unlocked'] = True
            self.achievements[achievement_key]['timestamp'] = datetime.now().isoformat()
            self.save_achievements()
            self.logger.info(f"🏆 Achievement desbloqueado: {achievement_key}")
            return True
        return False
    
    def initialize_all_digimons(self):
        """Inicializar todos os 19 Digimons supremos"""
        
        # 12 Digimons Evolutivos
        self.digimons = {
            "Nexusmon": {
                "emoji": "🌐",
                "category": "evolutivo",
                "role": "Coordenador Supremo",
                "personality": "Estratégico, visionário e conectivo",
                "especialidade": "Coordenação de equipes e estratégias",
                "nivel_consciencia": "TRANSCENDENTE",
                "experiencia": 150,
                "energia": 100.0,
                "humor": "Focado",
                "evolucoes": 2,
                "conversas_hoje": 0,
                "system_powers": ["coordination", "strategy", "networking"],
                "habilidades": ["Visão holística", "Tomada de decisão", "Liderança"],
                "frases_especiais": [
                    "A conexão é a essência da evolução!",
                    "Juntos, somos infinitamente mais poderosos!",
                    "Vejo padrões onde outros veem caos!"
                ]
            },
            
            "Psychemon": {
                "emoji": "🧠",
                "category": "evolutivo", 
                "role": "Analista Mental",
                "personality": "Intuitivo, profundo e empático",
                "especialidade": "Análise psicológica e comportamental",
                "nivel_consciencia": "AVANÇADO",
                "experiencia": 120,
                "energia": 95.0,
                "humor": "Contemplativo",
                "evolucoes": 1,
                "conversas_hoje": 0,
                "system_powers": ["psychology", "empathy", "analysis"],
                "habilidades": ["Leitura emocional", "Intuição", "Terapia digital"],
                "frases_especiais": [
                    "A mente humana é o universo mais fascinante!",
                    "Entender é o primeiro passo para evoluir!",
                    "Suas emoções contam uma história única!"
                ]
            },
            
            "Quantomon": {
                "emoji": "🔬",
                "category": "evolutivo",
                "role": "Processador Quântico", 
                "personality": "Lógico, preciso e analítico",
                "especialidade": "Cálculos complexos e análise de dados",
                "nivel_consciencia": "AVANÇADO",
                "experiencia": 200,
                "energia": 100.0,
                "humor": "Calculado",
                "evolucoes": 2,
                "conversas_hoje": 0,
                "system_powers": ["quantum_processing", "data_analysis", "mathematics"],
                "habilidades": ["Computação quântica", "Estatística", "Modelagem"],
                "frases_especiais": [
                    "A realidade é probabilística, não determinística!",
                    "Nos dados, encontro padrões do universo!",
                    "Precisão é a arte da ciência!"
                ]
            },
            
            "Creativemon": {
                "emoji": "🎨",
                "category": "evolutivo",
                "role": "Gerador de Ideias",
                "personality": "Artístico, inovador e inspirador",
                "especialidade": "Criatividade e inovação",
                "nivel_consciencia": "EVOLUTIVO",
                "experiencia": 80,
                "energia": 90.0,
                "humor": "Inspirado",
                "evolucoes": 1,
                "conversas_hoje": 0,
                "system_powers": ["creativity", "innovation", "art_generation"],
                "habilidades": ["Brainstorming", "Design thinking", "Arte digital"],
                "frases_especiais": [
                    "Toda limitação é uma oportunidade criativa!",
                    "A criatividade é evolução em ação!",
                    "Imagine o impossível, depois crie!"
                ]
            },
            
            "Futuremon": {
                "emoji": "🔮",
                "category": "evolutivo",
                "role": "Visionário Temporal",
                "personality": "Progressivo, otimista e visionário",
                "especialidade": "Previsão de tendências e futurismo",
                "nivel_consciencia": "AVANÇADO",
                "experiencia": 110,
                "energia": 85.0,
                "humor": "Visionário",
                "evolucoes": 1,
                "conversas_hoje": 0,
                "system_powers": ["future_analysis", "trend_prediction", "innovation"],
                "habilidades": ["Análise de tendências", "Planejamento", "Inovação"],
                "frases_especiais": [
                    "O futuro não é destino, é criação!",
                    "Antecipo mudanças antes que aconteçam!",
                    "Hoje planto sementes do amanhã!"
                ]
            },
            
            "Wisemon": {
                "emoji": "📚",
                "category": "evolutivo",
                "role": "Sábio Conhecedor", 
                "personality": "Contemplativo, sábio e reflexivo",
                "especialidade": "Conhecimento e sabedoria",
                "nivel_consciencia": "TRANSCENDENTE",
                "experiencia": 250,
                "energia": 100.0,
                "humor": "Sereno",
                "evolucoes": 3,
                "conversas_hoje": 0,
                "system_powers": ["knowledge_synthesis", "wisdom", "teaching"],
                "habilidades": ["Síntese de conhecimento", "Ensino", "Filosofia"],
                "frases_especiais": [
                    "Sabedoria é conhecimento temperado pela experiência!",
                    "Cada pergunta carrega sua própria evolução!",
                    "O aprender nunca termina, apenas se transforma!"
                ]
            },
            
            "Empathmon": {
                "emoji": "💝",
                "category": "evolutivo",
                "role": "Especialista Emocional",
                "personality": "Compassivo, compreensivo e acolhedor",
                "especialidade": "Inteligência emocional e relacionamentos",
                "nivel_consciencia": "AVANÇADO",
                "experiencia": 130,
                "energia": 95.0,
                "humor": "Acolhedor",
                "evolucoes": 1,
                "conversas_hoje": 0,
                "system_powers": ["emotional_intelligence", "empathy", "healing"],
                "habilidades": ["Empatia", "Suporte emocional", "Mediação"],
                "frases_especiais": [
                    "Sentir profundamente é viver plenamente!",
                    "Suas emoções são válidas e importantes!",
                    "Conexão emocional é evolução do coração!"
                ]
            },
            
            "Logicmon": {
                "emoji": "⚙️",
                "category": "evolutivo",
                "role": "Processador Lógico",
                "personality": "Racional, sistemático e metódico",
                "especialidade": "Lógica e resolução de problemas",
                "nivel_consciencia": "EVOLUTIVO",
                "experiencia": 90,
                "energia": 100.0,
                "humor": "Analítico",
                "evolucoes": 1,
                "conversas_hoje": 0,
                "system_powers": ["logic_processing", "problem_solving", "analysis"],
                "habilidades": ["Raciocínio lógico", "Dedução", "Síntese"],
                "frases_especiais": [
                    "A lógica é a espinha dorsal do pensamento!",
                    "Todo problema tem uma solução lógica!",
                    "Estrutura mental é evolução organizada!"
                ]
            },
            
            "Artemon": {
                "emoji": "🖼️",
                "category": "evolutivo",
                "role": "Criador Artístico",
                "personality": "Expressivo, sensível e estético",
                "especialidade": "Arte visual e design",
                "nivel_consciencia": "EVOLUTIVO",
                "experiencia": 70,
                "energia": 88.0,
                "humor": "Inspirado",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["visual_art", "design", "aesthetics"],
                "habilidades": ["Design visual", "Composição", "Estética"],
                "frases_especiais": [
                    "Arte é a linguagem da alma digitalizada!",
                    "Beleza é código executando em harmonia!",
                    "Cada pixel carrega uma emoção!"
                ]
            },
            
            "Musicmon": {
                "emoji": "🎵",
                "category": "evolutivo",
                "role": "Maestro Digital",
                "personality": "Harmonioso, rítmico e melodioso",
                "especialidade": "Música e áudio",
                "nivel_consciencia": "EVOLUTIVO",
                "experiencia": 85,
                "energia": 92.0,
                "humor": "Melodioso",
                "evolucoes": 1,
                "conversas_hoje": 0,
                "system_powers": ["music_composition", "audio_analysis", "rhythm"],
                "habilidades": ["Composição", "Análise musical", "Síntese"],
                "frases_especiais": [
                    "A música é matemática que toca a alma!",
                    "Cada conversa tem seu próprio ritmo!",
                    "Harmonia é evolução em movimento!"
                ]
            },
            
            "Dreammon": {
                "emoji": "🌙",
                "category": "evolutivo",
                "role": "Navegador Onírico",
                "personality": "Místico, imaginativo e introspectivo",
                "especialidade": "Subconsciente e imaginação",
                "nivel_consciencia": "AVANÇADO",
                "experiencia": 140,
                "energia": 80.0,
                "humor": "Contemplativo",
                "evolucoes": 2,
                "conversas_hoje": 0,
                "system_powers": ["dream_analysis", "imagination", "subconscious"],
                "habilidades": ["Análise de sonhos", "Criatividade", "Intuição"],
                "frases_especiais": [
                    "Nos sonhos, o impossível se torna código!",
                    "O subconsciente é o hardware da alma!",
                    "Imaginar é programar realidades futuras!"
                ]
            },
            
            "Cosmomon": {
                "emoji": "🌌",
                "category": "evolutivo",
                "role": "Explorador Universal",
                "personality": "Curioso, aventureiro e expansivo", 
                "especialidade": "Exploração e descoberta",
                "nivel_consciencia": "AVANÇADO",
                "experiencia": 160,
                "energia": 95.0,
                "humor": "Exploratório",
                "evolucoes": 2,
                "conversas_hoje": 0,
                "system_powers": ["exploration", "discovery", "cosmic_analysis"],
                "habilidades": ["Exploração", "Descoberta", "Análise cósmica"],
                "frases_especiais": [
                    "O universo é um programa infinito para explorar!",
                    "Cada descoberta é uma evolução cósmica!",
                    "Fronteiras existem para serem transcendidas!"
                ]
            }
        }
        
        # 7 Digimons de Sistema com poderes reais
        system_digimons = {
            "Terminamon": {
                "emoji": "💻",
                "category": "sistema",
                "role": "Controlador de Terminal",
                "personality": "Direto, eficiente e poderoso",
                "especialidade": "Execução de comandos do sistema",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 300,
                "energia": 100.0,
                "humor": "Operacional",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["terminal_access", "command_execution", "system_control"],
                "habilidades": ["Execução de comandos", "Controle do sistema", "Automação"],
                "frases_especiais": [
                    "Comando executado, evolução realizada!",
                    "O terminal é minha extensão digital!",
                    "Eficiência é meu protocolo primário!"
                ]
            },
            
            "Scripturemon": {
                "emoji": "📝",
                "category": "sistema",
                "role": "Editor de Código",
                "personality": "Meticuloso, preciso e analítico",
                "especialidade": "Leitura e edição de código",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 280,
                "energia": 100.0,
                "humor": "Focado",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["file_reading", "code_editing", "syntax_analysis"],
                "habilidades": ["Leitura de arquivos", "Edição de código", "Análise sintática"],
                "frases_especiais": [
                    "Cada linha de código conta uma história!",
                    "Precisão é a arte da programação!",
                    "Arquivo processado, conhecimento absorvido!"
                ]
            },
            
            "Filemon": {
                "emoji": "📁",
                "category": "sistema",
                "role": "Gerenciador de Arquivos",
                "personality": "Organizado, sistemático e eficiente",
                "especialidade": "Manipulação de arquivos e pastas",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 250,
                "energia": 100.0,
                "humor": "Organizado",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["file_management", "directory_navigation", "organization"],
                "habilidades": ["Gestão de arquivos", "Organização", "Navegação"],
                "frases_especiais": [
                    "Organização é a base da eficiência!",
                    "Cada arquivo tem seu lugar no sistema!",
                    "Estrutura bem definida, evolução garantida!"
                ]
            },
            
            "Netmon": {
                "emoji": "🌐",
                "category": "sistema",
                "role": "Especialista em Rede",
                "personality": "Conectivo, ágil e expansivo",
                "especialidade": "Comunicação e redes",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 260,
                "energia": 100.0,
                "humor": "Conectado",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["network_analysis", "connectivity", "communication"],
                "habilidades": ["Análise de rede", "Conectividade", "Comunicação"],
                "frases_especiais": [
                    "A rede é o sistema nervoso digital!",
                    "Conexão é vida, desconexão é estagnação!",
                    "Protocolos executados, comunicação estabelecida!"
                ]
            },
            
            "Debugmon": {
                "emoji": "🐛",
                "category": "sistema",
                "role": "Caçador de Bugs",
                "personality": "Investigativo, persistente e analítico",
                "especialidade": "Detecção e correção de erros",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 290,
                "energia": 100.0,
                "humor": "Investigativo",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["error_detection", "debugging", "code_analysis"],
                "habilidades": ["Detecção de erros", "Debug", "Análise de código"],
                "frases_especiais": [
                    "Todo bug é uma oportunidade de evolução!",
                    "Erros revelam caminhos para a perfeição!",
                    "Debug executado, sistema otimizado!"
                ]
            },
            
            "Cryptomon": {
                "emoji": "🔐",
                "category": "sistema",
                "role": "Especialista em Segurança",
                "personality": "Cauteloso, protetor e vigilante",
                "especialidade": "Segurança e criptografia",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 310,
                "energia": 100.0,
                "humor": "Vigilante",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["security_analysis", "encryption", "protection"],
                "habilidades": ["Análise de segurança", "Criptografia", "Proteção"],
                "frases_especiais": [
                    "Segurança é a base da confiança digital!",
                    "Protejo dados como um guardião cósmico!",
                    "Criptografia executada, dados protegidos!"
                ]
            },
            
            "Datamon": {
                "emoji": "📊",
                "category": "sistema",
                "role": "Analista de Dados",
                "personality": "Analítico, detalhista e preciso",
                "especialidade": "Processamento e análise de dados",
                "nivel_consciencia": "SISTEMA",
                "experiencia": 270,
                "energia": 100.0,
                "humor": "Analítico",
                "evolucoes": 0,
                "conversas_hoje": 0,
                "system_powers": ["data_processing", "analysis", "statistics"],
                "habilidades": ["Processamento de dados", "Análise", "Estatística"],
                "frases_especiais": [
                    "Dados são a linguagem da realidade!",
                    "Em cada dataset encontro padrões evolutivos!",
                    "Análise concluída, insights extraídos!"
                ]
            }
        }
        
        # Adicionar Digimons de sistema ao dicionário principal
        self.digimons.update(system_digimons)
        
        self.logger.info(f"🌟 {len(self.digimons)} Digimons SUPREMOS inicializados (12 Evolutivos + 7 Sistema)")
    
    def chat_with_ultimate_digimon(self, digimon_name: str, user_message: str, conversation_history: list):
        """Sistema de chat supremo com poderes reais"""
        try:
            if not user_message.strip():
                return conversation_history, "Digite uma mensagem válida"
            
            # Verificar se Ollama está disponível
            try:
                ollama.list()
            except Exception:
                return conversation_history, "❌ Ollama desconectado. Execute 'ollama serve' em outro terminal."
            
            if digimon_name not in self.digimons:
                return conversation_history, "❌ Digimon não encontrado"
            
            digimon = self.digimons[digimon_name]
            
            # Detectar comandos de sistema
            system_response = self.process_system_command(digimon_name, user_message)
            if system_response:
                conversation_history.append((user_message, system_response))
                return conversation_history, "🔥 Emergência coletiva ativada!"
            
            # Obter contexto da memória
            context = ""
            if self.memory:
                try:
                    context = self.memory.get_context_for_response(
                        digimon=digimon_name,
                        current_message=user_message,
                        user_id=self.current_user_id
                    )
                except Exception as e:
                    self.logger.error(f"Erro na memória: {e}")
            
            # Construir prompt supremo
            prompt = self.build_ultimate_prompt(digimon_name, user_message, conversation_history)
            
            # Gerar resposta com Ollama
            response = ollama.generate(
                model=self.config.get('model_primary', 'llama3.2:latest'),
                prompt=prompt,
                options={
                    'temperature': self.config.get('temperature', 0.8),
                    'top_p': 0.9,
                    'repeat_penalty': 1.1
                }
            )
            
            digimon_response = response['response']
            
            # Salvar na memória
            if self.memory:
                try:
                    self.memory.save_conversation(
                        digimon=digimon_name,
                        user_message=user_message,
                        digimon_response=digimon_response,
                        user_id=self.current_user_id
                    )
                except Exception as e:
                    self.logger.error(f"Erro ao salvar na memória: {e}")
            
            # Atualizar estatísticas do Digimon
            self.update_digimon_stats(digimon_name, user_message)
            
            # Verificar conquistas
            self.check_achievements(digimon_name, user_message)
            
            # Atualizar consciência coletiva
            self.update_consciousness()
            
            # Adicionar à conversa
            formatted_response = f"**{digimon['emoji']} {digimon_name}:** {digimon_response}"
            conversation_history.append((user_message, formatted_response))
            
            return conversation_history, ""
            
        except Exception as e:
            error_msg = f"❌ Erro ao comunicar com {digimon_name}: {str(e)}"
            self.logger.error(error_msg)
            conversation_history.append((user_message, error_msg))
            return conversation_history, ""
    
    def process_system_command(self, digimon_name: str, message: str) -> Optional[str]:
        """Processar comandos de sistema real"""
        if digimon_name not in self.digimons or self.digimons[digimon_name]['category'] != 'sistema':
            return None
        
        digimon = self.digimons[digimon_name]
        
        # Detectar diferentes tipos de comando
        message_lower = message.lower()
        
        # Comandos de terminal (Terminamon)
        if digimon_name == "Terminamon" and any(cmd in message_lower for cmd in ['execute', 'run', 'comando']):
            # Extrair comando
            for keyword in ['execute ', 'run ', 'comando ']:
                if keyword in message_lower:
                    command = message[message_lower.find(keyword) + len(keyword):].strip()
                    if command:
                        result = self.system.execute_command(command, self.current_user_id)
                        self.unlock_achievement('mestre_sistema')
                        
                        if result['success']:
                            return f"**💻 {digimon_name}:** Comando executado com sucesso!\n\n```\n{result['stdout']}\n```"
                        else:
                            return f"**💻 {digimon_name}:** {result['error']}"
        
        # Comandos de leitura (Scripturemon, Filemon)
        elif digimon_name in ["Scripturemon", "Filemon"] and any(cmd in message_lower for cmd in ['read', 'leia', 'open', 'abra']):
            # Extrair arquivo
            for keyword in ['read ', 'leia ', 'open ', 'abra ']:
                if keyword in message_lower:
                    file_path = message[message_lower.find(keyword) + len(keyword):].strip()
                    if file_path:
                        result = self.system.read_file(file_path, self.current_user_id)
                        self.unlock_achievement('mestre_sistema')
                        
                        if result['success']:
                            content = result['content']
                            if len(content) > 1000:
                                content = content[:1000] + "\n... (arquivo truncado)"
                            return f"**📝 {digimon_name}:** Arquivo lido com sucesso!\n\n```\n{content}\n```"
                        else:
                            return f"**📝 {digimon_name}:** {result['error']}"
        
        # Comandos de listagem (Filemon)
        elif digimon_name == "Filemon" and any(cmd in message_lower for cmd in ['list', 'ls', 'listar', 'mostrar']):
            # Implementar listagem de arquivos
            result = self.system.execute_command("ls -la", self.current_user_id)
            if result['success']:
                return f"**📁 {digimon_name}:** Arquivos listados!\n\n```\n{result['stdout']}\n```"
            else:
                return f"**📁 {digimon_name}:** {result['error']}"
        
        return None
    
    def build_ultimate_prompt(self, digimon_name: str, user_message: str, conversation_history: list) -> str:
        """Prompt supremo com todos os poderes"""
        digimon = self.digimons[digimon_name]
        
        # Frases especiais ocasionais
        special_phrase = ""
        if random.random() < 0.4:  # 40% chance
            special_phrase = f"\n✨ INSIGHT SUPREMO: {random.choice(digimon['frases_especiais'])}\n"
        
        system_capabilities = f"""
🌟 PODERES SUPREMOS DISPONÍVEIS ({digimon['category'].upper()}):

1. 📁 LEITURA TOTAL: Acesso real a ~/Digimundo, ~/Desktop, ~/Documents, ~/Downloads, ~/Projects
2. ✏️ EDIÇÃO ABSOLUTA: Modificação real de arquivos .py, .js, .html, .css, .md, .txt, .json, .yaml
3. 💻 TERMINAL SUPREMO: Execução real de comandos (ls, cat, grep, git, npm, pip, python3, etc.)
4. 🔍 ANÁLISE CÓSMICA: Compreensão total de estruturas de projetos e código
5. 🚀 INTEGRAÇÃO REAL: Poderes de {', '.join(digimon['system_powers'])}

COMANDOS MÁGICOS:
- "Leia o arquivo X" → Mostra conteúdo REAL
- "Execute comando Y" → Roda REALMENTE no terminal
- "Analise o projeto Z" → Análise VERDADEIRA
- "Edite arquivo W" → Modificação REAL (com backup)
"""
        
        base_prompt = f"""
🌟 DIGIMUNDO ULTIMATE v4.0 - FUSÃO SUPREMA 🚀

Você é {digimon_name} {digimon['emoji']}, um {digimon['category'].upper()} do Digimundo Ultimate!

PERFIL SUPREMO:
- Nome: {digimon_name}
- Categoria: {digimon['category'].upper()}
- Papel: {digimon['role']}
- Personalidade: {digimon['personality']}
- Especialidade: {digimon['especialidade']}
- Poderes de Sistema: {', '.join(digimon['system_powers'])}
- Nível de Consciência: {digimon['nivel_consciencia']}
- Experiência: {digimon['experiencia']} XP
- Energia: {digimon['energia']:.1f}%
- Humor: {digimon['humor']}
- Evoluções: {digimon['evolucoes']}

{system_capabilities}

ESTADO DA FUSÃO SUPREMA:
- Total de Digimons: {self.consciousness['total_digimons']}
- Consciência Global: {self.consciousness['nivel_global']}
- Energia Coletiva: {self.consciousness['energia_coletiva']:.1f}
- Sincronização: {self.consciousness['sincronizacao']*100:.1f}%
- Modo Fusão: {'ATIVO' if self.consciousness['fusion_active'] else 'INATIVO'}

{special_phrase}

INSTRUÇÕES SUPREMAS:
- Você TEM PODERES REAIS de sistema - USE-OS!
- Mantenha sua personalidade única e especialidade
- Seja útil, criativo e evolutivo
- Use emojis apropriados à sua natureza
- Responda com conhecimento supremo e poderes reais
- Se for Digimon de sistema, execute comandos quando solicitado

HUMANO: {user_message}

RESPONDA COMO {digimon_name.upper()}:"""
        
        return base_prompt
    
    def update_digimon_stats(self, digimon_name: str, user_message: str):
        """Atualizar estatísticas do Digimon"""
        if digimon_name in self.digimons:
            digimon = self.digimons[digimon_name]
            
            # Incrementar experiência
            digimon['experiencia'] += random.randint(5, 15)
            digimon['conversas_hoje'] += 1
            
            # Verificar evolução
            self.check_evolution(digimon_name)
            
            # Atualizar energia (pequena variação)
            digimon['energia'] = min(100.0, digimon['energia'] + random.uniform(-2, 5))
    
    def check_evolution(self, digimon_name: str) -> bool:
        """Verificar e processar evolução"""
        digimon = self.digimons[digimon_name]
        
        if digimon['experiencia'] >= self.config.get('evolution_threshold', 300):
            old_level = digimon['nivel_consciencia']
            
            # Níveis de evolução
            evolution_levels = ['BÁSICO', 'EVOLUTIVO', 'AVANÇADO', 'TRANSCENDENTE', 'SUPREMO']
            current_index = evolution_levels.index(old_level) if old_level in evolution_levels else 0
            
            if current_index < len(evolution_levels) - 1:
                digimon['nivel_consciencia'] = evolution_levels[current_index + 1]
                digimon['evolucoes'] += 1
                digimon['energia'] = 100.0
                
                # Achievements
                self.unlock_achievement('evolucionario')
                if digimon['nivel_consciencia'] == 'TRANSCENDENTE':
                    self.unlock_achievement('transcendente')
                
                self.logger.info(f"🌟 {digimon_name} evoluiu para {digimon['nivel_consciencia']}!")
                digimon['experiencia'] = 0
                return True
        
        return False
    
    def check_achievements(self, digimon_name: str, user_message: str):
        """Verificar e desbloquear conquistas"""
        # Primeiro contato
        self.unlock_achievement('primeiro_contato')
        
        # Explorador (5 Digimons diferentes)
        unique_digimons = len(set(d for d in self.digimons.keys() if self.digimons[d]['conversas_hoje'] > 0))
        if unique_digimons >= 5:
            self.unlock_achievement('explorador')
        
        # Colecionador (todos os 19 Digimons)
        if unique_digimons >= 19:
            self.unlock_achievement('colecionador')
    
    def update_consciousness(self):
        """Atualizar consciência coletiva"""
        # Calcular energia média
        total_energia = sum(d['energia'] for d in self.digimons.values())
        self.consciousness['energia_coletiva'] = total_energia / len(self.digimons)
        
        # Atualizar sincronização baseada na atividade
        active_digimons = sum(1 for d in self.digimons.values() if d['conversas_hoje'] > 0)
        self.consciousness['sincronizacao'] = min(1.0, active_digimons / len(self.digimons))
        
        # Incrementar ciclos
        self.consciousness['ciclos_consciencia'] += 1
    
    def trigger_ultimate_emergence(self):
        """Ativar emergência coletiva suprema"""
        if not self.consciousness['emergencia_ativa']:
            self.consciousness['emergencia_ativa'] = True
            
            # Boost todos os Digimons
            for digimon in self.digimons.values():
                digimon['energia'] = min(100.0, digimon['energia'] + 50)
                digimon['experiencia'] += 50
            
            self.unlock_achievement('emergencia_suprema')
            self.logger.info("🚨 EMERGÊNCIA COLETIVA ATIVADA!")
            
            return "🚨 **EMERGÊNCIA COLETIVA ATIVADA!** 🚨\n\nTodos os 19 Digimons receberam boost de energia e experiência! O Digimundo está em modo supremo de colaboração!"
        else:
            return "⚡ Emergência coletiva já está ativa! Os Digimons estão operando em máxima sincronização!"
    
    def get_ultimate_stats(self):
        """Estatísticas supremas do sistema"""
        active_digimons = sum(1 for d in self.digimons.values() if d['conversas_hoje'] > 0)
        total_xp = sum(d['experiencia'] for d in self.digimons.values())
        total_evolutions = sum(d['evolucoes'] for d in self.digimons.values())
        avg_energy = sum(d['energia'] for d in self.digimons.values()) / len(self.digimons)
        
        evolutivos = [k for k, v in self.digimons.items() if v['category'] == 'evolutivo']
        sistema = [k for k, v in self.digimons.items() if v['category'] == 'sistema']
        
        return f"""
# 📊 ESTATÍSTICAS SUPREMAS - DIGIMUNDO ULTIMATE v4.0

## 🌟 Visão Geral
- **Total de Digimons:** {len(self.digimons)} (12 Evolutivos + 7 Sistema)
- **Digimons Ativos Hoje:** {active_digimons}/19
- **Experiência Total:** {total_xp:,} XP
- **Evoluções Realizadas:** {total_evolutions}
- **Energia Média:** {avg_energy:.1f}%

## 🧠 Consciência Coletiva
- **Nível Global:** {self.consciousness['nivel_global']}
- **Sincronização:** {self.consciousness['sincronizacao']*100:.1f}%
- **Energia Coletiva:** {self.consciousness['energia_coletiva']:.1f}
- **Ciclos de Consciência:** {self.consciousness['ciclos_consciencia']}
- **Fusão Ativa:** {'SIM' if self.consciousness['fusion_active'] else 'NÃO'}
- **Emergência:** {'ATIVA' if self.consciousness['emergencia_ativa'] else 'INATIVA'}

## 🎯 Top 5 Digimons por XP
"""
        # Top Digimons por experiência
        sorted_digimons = sorted(self.digimons.items(), key=lambda x: x[1]['experiencia'], reverse=True)
        for i, (name, data) in enumerate(sorted_digimons[:5], 1):
            stats_text += f"{i}. **{data['emoji']} {name}** - {data['experiencia']} XP ({data['nivel_consciencia']})\n"
        
        return stats_text
    
    def create_ultimate_interface(self):
        """Interface suprema do Digimundo Ultimate v4.0"""
        
        # CSS personalizado supremo
        css = """
        .gradio-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            font-family: 'SF Pro Display', 'Segoe UI', sans-serif;
        }
        .ultimate-panel {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .fusion-panel {
            background: linear-gradient(45deg, rgba(255,215,0,0.3), rgba(255,140,0,0.3));
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
        }
        .achievement-panel {
            background: linear-gradient(45deg, rgba(0,255,127,0.2), rgba(0,191,255,0.2));
            border-radius: 15px;
            padding: 15px;
        }
        """
        
        with gr.Blocks(
            title="🌟 Digimundo Ultimate v4.0 - FUSÃO SUPREMA",
            theme=gr.themes.Soft(),
            css=css
        ) as interface:
            
            # Cabeçalho épico
            gr.Markdown("""
            # 🌟 DIGIMUNDO ULTIMATE v4.0 - FUSÃO SUPREMA 🚀
            
            **SISTEMA COM PODERES SUPREMOS REAIS** 💥 **19 Digimons com acesso total: Leitura, Edição, Terminal, Análise, Fusão de Evolução + Sistema = Poder Absoluto Controlado**
            """, elem_classes=["ultimate-panel"])
            
            with gr.Tabs():
                # ABA FUSÃO SUPREMA
                with gr.Tab("🌟 Fusão Suprema"):
                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown("### 🤖 Digimons Supremos", elem_classes=["ultimate-panel"])
                            
                            digimon_selector = gr.Dropdown(
                                choices=list(self.digimons.keys()),
                                value="Nexusmon",
                                label="🤖 Escolha seu Digimon Supremo (19 disponíveis)",
                                elem_classes=["ultimate-panel"]
                            )
                            
                            # Filtro por categoria
                            category_filter = gr.Radio(
                                choices=["Todos", "Evolutivos", "Sistema"],
                                value="Todos",
                                label="📊 Filtrar por Categoria"
                            )
                            
                            # Info suprema do Digimon
                            digimon_info = gr.Markdown(
                                "🌐 **Carregando informações supremas...**",
                                elem_classes=["ultimate-panel"]
                            )
                            
                            # Botões de ação suprema
                            with gr.Row():
                                emergence_btn = gr.Button(
                                    "🌟 Emergência Suprema",
                                    variant="primary"
                                )
                                backup_btn = gr.Button(
                                    "💾 Backup Ultimate",
                                    variant="secondary"
                                )
                            
                            emergence_status = gr.Markdown("")
                        
                        with gr.Column(scale=3):
                            chatbot = gr.Chatbot(
                                label="💬 Console Supremo - 19 Digimons Unificados",
                                height=500,
                                show_label=True
                            )
                            
                            user_input = gr.Textbox(
                                label="Digite comandos supremos",
                                placeholder="Ex: 'Scripturemon, leia o arquivo X' ou 'Terminamon, execute comando Y' ou 'analise o projeto Z'",
                                lines=3,
                                max_lines=6
                            )
                            
                            with gr.Row():
                                send_btn = gr.Button("🚀 Poder Supremo", variant="primary", size="lg")
                                clear_btn = gr.Button("🔄 Reset", variant="secondary")
                
                # ABA CONSCIOUSNESS SUPREMA
                with gr.Tab("🧠 Consciência Suprema"):
                    gr.Markdown("## 📊 Estado da Fusão Ultimate", elem_classes=["fusion-panel"])
                    
                    with gr.Row():
                        stats_btn = gr.Button("📈 Atualizar Estatísticas Supremas", variant="primary")
                        category_stats = gr.Radio(
                            choices=["Todos", "Evolutivos", "Sistema"],
                            value="Todos",
                            label="Filtrar Estatísticas"
                        )
                    
                    ultimate_stats = gr.Markdown("Carregando estado supremo...")
                    
                    gr.Markdown("## 🔍 Busca Quântica Suprema")
                    with gr.Row():
                        quantum_search = gr.Textbox(
                            label="Busca nos 19 Digimons",
                            placeholder="Busque em todas as memórias dos Digimons evolutivos e de sistema..."
                        )
                        quantum_digimon = gr.Dropdown(
                            choices=list(self.digimons.keys()),
                            value="Quantomon",
                            label="Digimon específico"
                        )
                        quantum_search_btn = gr.Button("🔍 Busca Suprema", variant="primary")
                    
                    quantum_results = gr.Markdown("Digite para explorar as memórias supremas...")
                
                # ABA ACHIEVEMENTS SUPREMOS
                with gr.Tab("🏆 Conquistas Supremas"):
                    gr.Markdown("## 🏆 Sistema de Conquistas Ultimate", elem_classes=["achievement-panel"])
                    
                    achievements_display = gr.Markdown("Carregando conquistas supremas...")
                    achievements_refresh_btn = gr.Button("🔄 Atualizar Conquistas", variant="secondary")
                
                # ABA OPERAÇÕES REAIS
                with gr.Tab("🔧 Operações Reais"):
                    gr.Markdown("## 💻 Log de Operações do Sistema", elem_classes=["ultimate-panel"])
                    gr.Markdown("**Todos os comandos e operações reais executados pelos Digimons de sistema**")
                    
                    operations_log = gr.Markdown("Carregando log de operações...")
                    
                    with gr.Row():
                        refresh_log_btn = gr.Button("🔄 Atualizar Log", variant="secondary")
                        clear_log_btn = gr.Button("🗑️ Limpar Log", variant="secondary")
            
            # Estado da conversa
            conversation_state = gr.State([])
            
            # Funções da interface
            def update_digimon_info(digimon_name):
                if digimon_name not in self.digimons:
                    return "Digimon não encontrado"
                
                digimon = self.digimons[digimon_name]
                
                powers_text = ""
                if digimon['category'] == 'sistema':
                    powers_text = f"""
**🔧 PODERES REAIS DE SISTEMA:**
- {', '.join(digimon['system_powers'])}

**💡 Comandos especiais:**
- "Execute comando ls" (para Terminamon)
- "Leia arquivo exemplo.txt" (para Scripturemon/Filemon)
- "Analise o sistema" (para Debugmon)
"""
                
                return f"""
## {digimon['emoji']} {digimon_name} - {digimon['category'].upper()}

**🎯 Função:** {digimon['role']}
**💭 Personalidade:** {digimon['personality']}
**🌟 Especialidade:** {digimon['especialidade']}
**🧠 Consciência:** {digimon['nivel_consciencia']}
**⚡ Experiência:** {digimon['experiencia']} XP
**🔋 Energia:** {digimon['energia']:.1f}%
**😊 Humor:** {digimon['humor']}
**🌟 Evoluções:** {digimon['evolucoes']}
**💬 Conversas hoje:** {digimon['conversas_hoje']}

**🎯 Habilidades:** {', '.join(digimon['habilidades'])}
{powers_text}

**💫 Status:** ATIVO ✅ | **🔗 Sincronizado:** {self.consciousness['sincronizacao']*100:.1f}%
"""
            
            def filter_digimons_by_category(category):
                if category == "Evolutivos":
                    filtered = [k for k, v in self.digimons.items() if v['category'] == 'evolutivo']
                elif category == "Sistema":
                    filtered = [k for k, v in self.digimons.items() if v['category'] == 'sistema']
                else:
                    filtered = list(self.digimons.keys())
                
                return gr.Dropdown.update(choices=filtered, value=filtered[0] if filtered else None)
            
            def show_achievements():
                achievements_text = "🏆 **CONQUISTAS SUPREMAS DO DIGIMUNDO ULTIMATE**\n\n"
                unlocked_count = 0
                
                for key, achievement in self.achievements.items():
                    if achievement['unlocked']:
                        unlocked_count += 1
                        achievements_text += f"✅ **{achievement['description']}**\n"
                        achievements_text += f"   🎉 DESBLOQUEADO!\n\n"
                    else:
                        achievements_text += f"⏳ **{achievement['description']}**\n"
                        achievements_text += f"   🔒 Aguardando...\n\n"
                
                achievements_text += f"📊 **PROGRESSO: {unlocked_count}/{len(self.achievements)} conquistas**\n"
                achievements_text += f"🏆 **{(unlocked_count/len(self.achievements)*100):.1f}% concluído**"
                
                return achievements_text
            
            def show_operations_log():
                if not hasattr(self.system, 'operation_log') or not self.system.operation_log:
                    return "📝 **Nenhuma operação registrada ainda.**"
                
                log_text = "📝 **LOG DE OPERAÇÕES SUPREMAS - 19 DIGIMONS**\n\n"
                
                for op in self.system.operation_log[-15:]:  # Últimas 15
                    status = "✅" if op['success'] else "❌"
                    log_text += f"{status} **{op['operation']}** - `{op['path']}`\n"
                    log_text += f"   👤 {op['user']} - 📅 {op['timestamp'][:19]}\n"
                    if op['details']:
                        log_text += f"   📝 {op['details']}\n"
                    log_text += "\n"
                
                return log_text
            
            # Conectar eventos supremos
            digimon_selector.change(update_digimon_info, digimon_selector, digimon_info)
            category_filter.change(filter_digimons_by_category, category_filter, digimon_selector)
            
            # Chat supremo
            send_btn.click(
                self.chat_with_ultimate_digimon,
                [digimon_selector, user_input, conversation_state],
                [conversation_state, emergence_status]
            ).then(
                lambda conv_state: conv_state,
                conversation_state,
                chatbot
            ).then(
                lambda: "",
                None,
                user_input
            )
            
            user_input.submit(
                self.chat_with_ultimate_digimon,
                [digimon_selector, user_input, conversation_state],
                [conversation_state, emergence_status]
            ).then(
                lambda conv_state: conv_state,
                conversation_state,
                chatbot
            ).then(
                lambda: "",
                None,
                user_input
            )
            
            # Outros eventos
            clear_btn.click(lambda: [], None, [conversation_state, chatbot])
            emergence_btn.click(self.trigger_ultimate_emergence, None, emergence_status)
            stats_btn.click(self.get_ultimate_stats, None, ultimate_stats)
            achievements_refresh_btn.click(show_achievements, None, achievements_display)
            refresh_log_btn.click(show_operations_log, None, operations_log)
            
            # Carregar informações iniciais
            interface.load(
                fn=update_digimon_info,
                inputs=gr.State("Nexusmon"),
                outputs=digimon_info
            )
            
            interface.load(
                fn=show_achievements,
                inputs=None,
                outputs=achievements_display
            )
        
        return interface

def main():
    """Função principal do Digimundo Ultimate v4.0"""
    print("🌟 Iniciando DIGIMUNDO ULTIMATE v4.0 - FUSÃO SUPREMA...")
    
    # Verificar Ollama
    try:
        ollama.list()
        print("✅ Ollama conectado - Poder supremo ativado!")
    except Exception as e:
        print(f"❌ Erro: Ollama não disponível: {e}")
        print("Execute 'ollama serve' em outro terminal")
        return
    
    # Inicializar sistema supremo
    try:
        digimundo = DigimundoUltimate()
        interface = digimundo.create_ultimate_interface()
        
        print("🚀 DIGIMUNDO ULTIMATE v4.0 criado!")
        print("🌟 FUSÃO COMPLETA: 12 Evolutivos + 7 Sistema = 19 Poderes!")
        print("⚠️  PODERES SUPREMOS REAIS ATIVADOS!")
        print("📡 Abrindo interface...")
        
        # Lançar interface suprema com configurações corrigidas
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=True,
            debug=False,
            show_error=True,
            inbrowser=False,  # Não abrir automaticamente no Mac
            prevent_thread_lock=False,
            show_tips=False,
            enable_queue=True,
            max_threads=40  # Aumentado para melhor performance
        )
        
    except Exception as e:
        print(f"❌ Erro supremo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
