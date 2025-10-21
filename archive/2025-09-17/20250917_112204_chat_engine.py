"""
Chat Engine - Motor de chat real com Ollama
Fase 2.A - Implementação completa
"""
import json
import time
from typing import Dict, List, Optional, Any, Generator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from apps.scripturemon.ollama_manager import get_ollama_manager
from apps.scripturemon.persona import PersonaManager
from apps.scripturemon.bootstrap import get_config

class ChatMode(Enum):
    """Modos de operação do chat"""
    NORMAL = 'normal'
    ANALYSIS = 'analysis'
    CREATIVE = 'creative'
    TECHNICAL = 'technical'
    SOCRATIC = 'socratic'

@dataclass
class Message:
    """Representa uma mensagem no chat"""
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ChatSession:
    """Sessão de chat com histórico e contexto"""
    session_id: str
    messages: List[Message] = field(default_factory=list)
    mode: ChatMode = ChatMode.NORMAL
    personality: Optional[str] = None
    model: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    total_tokens: int = 0
    max_context: int = 4096

class ChatEngine:
    """
    Motor principal de chat
    Coordena geração, contexto, personalidades e comandos
    """
    COMMANDS = {'/help': 'Mostra comandos disponíveis', '/clear': 'Limpa contexto da conversa', '/mode': 'Altera modo de operação', '/model': 'Altera modelo em uso', '/personality': 'Define personalidade', '/save': 'Salva conversa', '/load': 'Carrega conversa', '/analyze': 'Analisa roteiro', '/status': 'Mostra status do sistema'}
    MODE_PROMPTS = {ChatMode.NORMAL: 'Você é Scripturemon, um assistente especializado em análise de roteiros.', ChatMode.ANALYSIS: 'Você é um analista crítico de roteiros cinematográficos. Seja detalhado e técnico.', ChatMode.CREATIVE: 'Você é um roteirista criativo. Sugira melhorias e ideias inovadoras.', ChatMode.TECHNICAL: 'Você é um consultor técnico de produção. Foque em viabilidade e orçamento.', ChatMode.SOCRATIC: 'Use o método socrático. Faça perguntas que levem o usuário a descobrir as respostas.'}

    def __init__(self):
        """Inicializa engine"""
        self.config = get_config()
        self.ollama = get_ollama_manager()
        self.persona_manager = PersonaManager()
        self.sessions: Dict[str, ChatSession] = {}
        self.current_session: Optional[ChatSession] = None
        self.default_model = self.config.get('default_model', None)
        self.default_mode = ChatMode.NORMAL
        self.temperature = self.config.get('temperature', 0.7)
        self.max_tokens = self.config.get('max_tokens', 2048)
        self._create_session('default')

    def _create_session(self, session_id: str) -> ChatSession:
        """Cria nova sessão"""
        session = ChatSession(session_id=session_id, mode=self.default_mode, model=self.default_model)
        self.sessions[session_id] = session
        self.current_session = session
        return session

    def _estimate_tokens(self, text: str) -> int:
        """Estima número de tokens (aproximado)"""
        return len(text) // 4

    def _build_context(self, session: ChatSession) -> str:
        """Constrói contexto completo para geração"""
        system_prompt = self.MODE_PROMPTS[session.mode]
        if session.personality:
            persona_prompt = self.persona_manager.get_prompt(session.personality)
            if persona_prompt:
                system_prompt = f'{system_prompt}\n\n{persona_prompt}'
        context_parts = [f'System: {system_prompt}']
        for msg in session.messages[-20:]:
            if msg.role == 'user':
                context_parts.append(f'User: {msg.content}')
            elif msg.role == 'assistant':
                context_parts.append(f'Assistant: {msg.content}')
        return '\n\n'.join(context_parts)

    def process_message(self, user_input: str, session_id: Optional[str]=None, stream: bool=False) -> Any:
        """
        Processa mensagem do usuário
        Retorna resposta ou generator para streaming
        """
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            session = self.current_session or self._create_session('default')
        if user_input.startswith('/'):
            return self._handle_command(user_input, session)
        user_msg = Message(role='user', content=user_input, tokens=self._estimate_tokens(user_input))
        session.messages.append(user_msg)
        session.total_tokens += user_msg.tokens
        context = self._build_context(session)
        model = session.model or self.ollama.get_best_model('chat')
        if not model:
            error_msg = '❌ Nenhum modelo disponível'
            self._add_assistant_message(session, error_msg)
            return error_msg
        if stream:
            return self._stream_response(context, model, session)
        else:
            return self._generate_response(context, model, session)

    def _generate_response(self, context: str, model: str, session: ChatSession) -> str:
        """Gera resposta completa (não streaming)"""
        prompt = f'{context}\n\nAssistant:'
        response = self.ollama.generate(prompt=prompt, model=model, temperature=self.temperature, max_tokens=self.max_tokens)
        if response:
            self._add_assistant_message(session, response)
            return response
        else:
            error_msg = '❌ Erro gerando resposta'
            self._add_assistant_message(session, error_msg)
            return error_msg

    def _stream_response(self, context: str, model: str, session: ChatSession) -> Generator[str, None, None]:
        """Gera resposta em streaming"""
        prompt = f'{context}\n\nAssistant:'
        full_response = []
        for token in self.ollama.stream_generate(prompt=prompt, model=model, temperature=self.temperature, max_tokens=self.max_tokens):
            full_response.append(token)
            yield token
        complete = ''.join(full_response)
        if complete:
            self._add_assistant_message(session, complete)

    def _add_assistant_message(self, session: ChatSession, content: str) -> None:
        """Adiciona mensagem do assistente ao histórico"""
        msg = Message(role='assistant', content=content, tokens=self._estimate_tokens(content))
        session.messages.append(msg)
        session.total_tokens += msg.tokens
        self._manage_context(session)

    def _manage_context(self, session: ChatSession) -> None:
        """Gerencia tamanho do contexto"""
        if session.total_tokens > session.max_context:
            while len(session.messages) > 10 and session.total_tokens > session.max_context:
                removed = session.messages.pop(0)
                session.total_tokens -= removed.tokens

    def _handle_command(self, command: str, session: ChatSession) -> str:
        """Processa comandos especiais"""
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        if cmd == '/help':
            return self._show_help()
        elif cmd == '/clear':
            session.messages.clear()
            session.total_tokens = 0
            return '✅ Contexto limpo'
        elif cmd == '/mode':
            if args:
                mode_name = args[0].upper()
                try:
                    session.mode = ChatMode[mode_name]
                    return f'✅ Modo alterado para {session.mode.value}'
                except KeyError:
                    modes = ', '.join([m.value for m in ChatMode])
                    return f'❌ Modo inválido. Disponíveis: {modes}'
            else:
                return f'Modo atual: {session.mode.value}'
        elif cmd == '/model':
            if args:
                model_name = args[0]
                if self.ollama.load_model(model_name):
                    session.model = model_name
                    return f'✅ Modelo alterado para {model_name}'
                else:
                    return f'❌ Erro carregando modelo {model_name}'
            else:
                models = self.ollama.list_models()
                names = [m.name for m in models[:5]]
                return f"Modelos disponíveis: {', '.join(names)}"
        elif cmd == '/personality':
            if args:
                persona = ' '.join(args)
                if self.persona_manager.set_personality(persona):
                    session.personality = persona
                    return f'✅ Personalidade definida: {persona}'
                else:
                    return '❌ Personalidade não encontrada'
            else:
                personas = self.persona_manager.list_personalities()
                return f"Personalidades: {', '.join(personas[:5])}"
        elif cmd == '/save':
            filename = args[0] if args else f'chat_{session.session_id}.json'
            if self._save_session(session, filename):
                return f'✅ Conversa salva em {filename}'
            else:
                return '❌ Erro salvando conversa'
        elif cmd == '/load':
            if args:
                filename = args[0]
                if self._load_session(filename):
                    return f'✅ Conversa carregada de {filename}'
                else:
                    return f'❌ Erro carregando {filename}'
            else:
                return '❌ Especifique o arquivo'
        elif cmd == '/analyze':
            from apps.scripturemon.doctor import analyze_with_context
            if args:
                script_path = ' '.join(args)
                return analyze_with_context(script_path, session)
            else:
                return '❌ Especifique o roteiro para análise'
        elif cmd == '/status':
            return self._get_status(session)
        else:
            return f'❌ Comando desconhecido: {cmd}'

    def _show_help(self) -> str:
        """Mostra ajuda com comandos"""
        help_text = ['📚 COMANDOS DISPONÍVEIS:']
        for cmd, desc in self.COMMANDS.items():
            help_text.append(f'  {cmd} - {desc}')
        help_text.append('\n📝 MODOS:')
        for mode in ChatMode:
            help_text.append(f'  {mode.value}')
        return '\n'.join(help_text)

    def _get_status(self, session: ChatSession) -> str:
        """Retorna status do sistema"""
        ollama_health = self.ollama.health_check()
        status = ['📊 STATUS DO SISTEMA', '=' * 40, f'Sessão: {session.session_id}', f'Modo: {session.mode.value}', f"Modelo: {session.model or 'auto'}", f"Personalidade: {session.personality or 'nenhuma'}", f'Mensagens: {len(session.messages)}', f'Tokens usados: {session.total_tokens}/{session.max_context}', '', f"Ollama: {('✅ Online' if ollama_health['ollama_running'] else '❌ Offline')}", f"Modelos disponíveis: {ollama_health['models_available']}"]
        return '\n'.join(status)

    def _save_session(self, session: ChatSession, filename: str) -> bool:
        """Salva sessão em arquivo"""
        try:
            import os
            data_dir = 'data/chats'
            os.makedirs(data_dir, exist_ok=True)
            filepath = os.path.join(data_dir, filename)
            session_data = {'session_id': session.session_id, 'mode': session.mode.value, 'personality': session.personality, 'model': session.model, 'created_at': session.created_at.isoformat(), 'messages': [{'role': msg.role, 'content': msg.content, 'timestamp': msg.timestamp.isoformat(), 'tokens': msg.tokens} for msg in session.messages]}
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f'❌ Erro salvando: {e}')
            return False

    def _load_session(self, filename: str) -> bool:
        """Carrega sessão de arquivo"""
        try:
            import os
            data_dir = 'data/chats'
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                return False
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            session = ChatSession(session_id=session_data['session_id'], mode=ChatMode[session_data['mode'].upper()], personality=session_data.get('personality'), model=session_data.get('model'), created_at=datetime.fromisoformat(session_data['created_at']))
            for msg_data in session_data['messages']:
                msg = Message(role=msg_data['role'], content=msg_data['content'], timestamp=datetime.fromisoformat(msg_data['timestamp']), tokens=msg_data['tokens'])
                session.messages.append(msg)
                session.total_tokens += msg.tokens
            self.sessions[session.session_id] = session
            self.current_session = session
            return True
        except Exception as e:
            print(f'❌ Erro carregando: {e}')
            return False

    def apply_personality(self, personality_name: str) -> bool:
        """Aplica personalidade à sessão atual"""
        if self.current_session:
            self.current_session.personality = personality_name
            return True
        return False

    def handle_commands(self, command: str) -> str:
        """Interface pública para comandos"""
        if self.current_session:
            return self._handle_command(command, self.current_session)
        return '❌ Nenhuma sessão ativa'

    def get_session_info(self) -> Dict[str, Any]:
        """Retorna informações da sessão atual"""
        if not self.current_session:
            return {'error': 'Nenhuma sessão ativa'}
        session = self.current_session
        return {'session_id': session.session_id, 'mode': session.mode.value, 'personality': session.personality, 'model': session.model, 'messages_count': len(session.messages), 'tokens_used': session.total_tokens, 'max_context': session.max_context, 'created_at': session.created_at.isoformat()}
_engine_instance: Optional[ChatEngine] = None

def get_chat_engine() -> ChatEngine:
    """Retorna instância singleton do engine"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = ChatEngine()
    return _engine_instance
__all__ = ['ChatEngine', 'ChatMode', 'Message', 'ChatSession', 'get_chat_engine']