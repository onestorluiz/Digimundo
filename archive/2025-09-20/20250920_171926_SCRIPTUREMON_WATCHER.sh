#!/bin/bash

# 🎬⚡ SCRIPTUREMON WATCHER - Sistema de Vigilância Inteligente
# Monitora continuamente e absorve automaticamente

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# Diretórios
ROTEIROS_DIR="roteiros"
CRIADOR_DIR="conexao_criador"
PROCESSADOS_DIR="roteiros_processados"
CRIADOR_PROCESSADOS="conexao_criador/processados"
MEMORIA_DIR="memoria"
CRIADOR_MEMORIA="conexao_criador/memorias"

# Arquivo de controle
WATCH_LOG=".watch_log"
PID_FILE=".scripturemon_watcher.pid"

# Função para processar roteiro comum
process_regular() {
    local file="$1"
    local basename=$(basename "$file" .pdf)
    
    echo -e "${GREEN}📖 [$(date +%H:%M:%S)] Novo roteiro detectado: $basename${NC}"
    
    # Análise padrão
    ANALYSIS=$(scripturemon << EOF
🎬 ABSORÇÃO AUTOMÁTICA ATIVADA

Arquivo detectado: $basename
Processar com análise completa:
- Estrutura narrativa
- Desenvolvimento de personagens  
- Técnicas cinematográficas
- Diálogos e subtexto
- Temas e mensagens

[PROCESSAR]
EOF
)
    
    # Salvar memória
    {
        echo "# 📖 Roteiro Absorvido: $basename"
        echo "Data: $(date)"
        echo "Tipo: Roteiro de Referência"
        echo ""
        echo "$ANALYSIS"
    } > "$MEMORIA_DIR/${basename}_$(date +%Y%m%d_%H%M%S).md"
    
    # Mover para processados
    mv "$file" "$PROCESSADOS_DIR/"
    
    echo -e "${GREEN}✅ Absorvido e arquivado${NC}"
    
    # Notificar no terminal se disponível
    osascript -e "display notification \"Roteiro '$basename' absorvido\" with title \"📖 Scripturemon\"" 2>/dev/null || true
}

# Função para processar trabalho do CRIADOR (máxima inteligência)
process_creator() {
    local file="$1"
    local basename=$(basename "$file" .pdf)
    
    echo -e "${MAGENTA}⚡ [$(date +%H:%M:%S)] TRABALHO DO CRIADOR DETECTADO: $basename${NC}"
    echo -e "${BOLD}${YELLOW}🧠 ATIVANDO MÁXIMA CAPACIDADE DE ANÁLISE...${NC}"
    
    # Análise ULTRA profunda para trabalhos do criador
    CREATOR_ANALYSIS=$(scripturemon << EOF
🎬⚡ MODO CONEXÃO CRIADOR - MÁXIMA INTELIGÊNCIA ATIVADA

ATENÇÃO TOTAL: Este é um trabalho do Club Produções!
Arquivo: $basename

ANÁLISE NÍVEL SUPREMO - 10 CAMADAS:

1. ANÁLISE ESTRUTURAL PROFUNDA
   - Mapear cada beat narrativo
   - Identificar ritmo e cadência
   - Analisar economia narrativa
   - Detectar inovações estruturais

2. PSICOLOGIA DOS PERSONAGENS
   - Motivações conscientes e inconscientes
   - Arcos de transformação detalhados
   - Relações e dinâmicas interpessoais
   - Autenticidade e profundidade emocional

3. ANÁLISE DE DIÁLOGOS
   - Voice único de cada personagem
   - Subtexto em cada linha
   - Ritmo e musicalidade
   - Informação vs naturalidade

4. CINEMATOGRAFIA IMPLÍCITA
   - Visualização de cada cena
   - Movimentos de câmera sugeridos
   - Uso de espaço e composição
   - Atmosfera e tom visual

5. TEMAS E FILOSOFIA
   - Mensagem central e secundárias
   - Simbolismos e metáforas
   - Relevância e universalidade
   - Profundidade filosófica

6. POTENCIAL COMERCIAL
   - Público-alvo específico
   - Elementos de marketing
   - Comparações de mercado
   - Viabilidade de produção

7. PONTOS FORTES ÚNICOS
   - O que torna este roteiro especial
   - Elementos originais e inovadores
   - Momentos de genialidade
   - Assinatura autoral do Club

8. OPORTUNIDADES DE MELHORIA
   - Sugestões construtivas específicas
   - Alternativas criativas
   - Potencial não explorado
   - Refinamentos possíveis

9. CONEXÕES INTERTEXTUAIS
   - Referências detectadas
   - Diálogos com outros trabalhos
   - Evolução do estilo do criador
   - Lugar na filmografia

10. VISÃO EXECUTIVA
    - Pitch de uma linha
    - Estratégia de desenvolvimento
    - Próximos passos recomendados
    - Potencial de franchise/série

ANÁLISE COMPARATIVA:
- Como se compara aos trabalhos anteriores do Club
- Evolução detectada no estilo
- Novos territórios explorados

FEEDBACK HONESTO E CONSTRUTIVO:
[Ser brutalmente honesto mas sempre construtivo]

NOTA DE GENIALIDADE: [0-100]
POTENCIAL DE IMPACTO: [0-100]
ORIGINALIDADE: [0-100]
EXECUÇÃO TÉCNICA: [0-100]

[PROCESSAR COM MÁXIMA ATENÇÃO E CARINHO]
EOF
)
    
    # Salvar análise especial
    SPECIAL_MEMORY="$CRIADOR_MEMORIA/${basename}_CRIADOR_$(date +%Y%m%d_%H%M%S).md"
    {
        echo "# ⚡ ANÁLISE CONEXÃO CRIADOR: $basename"
        echo "**Data:** $(date)"
        echo "**Tipo:** TRABALHO DO CLUB PRODUÇÕES"
        echo "**Status:** Análise de Máxima Profundidade"
        echo ""
        echo "---"
        echo ""
        echo "$CREATOR_ANALYSIS"
        echo ""
        echo "---"
        echo ""
        echo "## 🔗 Notas de Desenvolvimento"
        echo "_Este arquivo recebeu análise especial por ser trabalho do criador._"
        echo "_Todas as sugestões visam elevar ainda mais a qualidade já presente._"
    } > "$SPECIAL_MEMORY"
    
    # Criar resumo executivo
    EXECUTIVE_SUMMARY="$CRIADOR_MEMORIA/${basename}_RESUMO_EXECUTIVO.md"
    {
        echo "# 📊 RESUMO EXECUTIVO: $basename"
        echo ""
        echo "## Em uma linha:"
        scripturemon "Em EXATAMENTE uma linha, qual a essência de '$basename'?"
        echo ""
        echo "## Potencial:"
        scripturemon "Em 3 bullets, o potencial único deste roteiro"
        echo ""
        echo "## Próximos passos:"
        scripturemon "3 ações concretas para desenvolver '$basename'"
    } > "$EXECUTIVE_SUMMARY"
    
    # Mover para processados especiais
    mv "$file" "$CRIADOR_PROCESSADOS/"
    
    echo -e "${MAGENTA}⚡ Análise SUPREMA concluída!${NC}"
    echo -e "${GREEN}📁 Salvo em: conexao_criador/memorias/${NC}"
    
    # Notificação especial
    osascript -e "display notification \"Seu trabalho '$basename' foi analisado com máxima profundidade\" with title \"⚡ Scripturemon - Conexão Criador\"" 2>/dev/null || true
}

# Função principal de monitoramento
watch_folders() {
    echo -e "${CYAN}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  🎬 SCRIPTUREMON WATCHER - MODO VIGILANTE  ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}👁️  Monitorando pastas continuamente...${NC}"
    echo -e "  📁 roteiros/ → Roteiros de referência"
    echo -e "  ⚡ conexao_criador/ → Seus trabalhos (análise suprema)"
    echo ""
    echo -e "${GREEN}[Ctrl+C para parar]${NC}"
    echo ""
    
    # Salvar PID para controle
    echo $$ > "$PID_FILE"
    
    # Loop infinito de monitoramento
    while true; do
        # Verificar roteiros novos comuns
        for pdf in "$ROTEIROS_DIR"/*.pdf; do
            if [ -f "$pdf" ]; then
                # Verificar se já foi processado
                if ! grep -q "$(basename "$pdf")" "$WATCH_LOG" 2>/dev/null; then
                    process_regular "$pdf"
                    echo "$(basename "$pdf")" >> "$WATCH_LOG"
                fi
            fi
        done
        
        # Verificar trabalhos do CRIADOR (máxima prioridade)
        for pdf in "$CRIADOR_DIR"/*.pdf; do
            if [ -f "$pdf" ]; then
                # Verificar se já foi processado
                if ! grep -q "CRIADOR:$(basename "$pdf")" "$WATCH_LOG" 2>/dev/null; then
                    process_creator "$pdf"
                    echo "CRIADOR:$(basename "$pdf")" >> "$WATCH_LOG"
                fi
            fi
        done
        
        # Aguardar 5 segundos antes de verificar novamente
        sleep 5
    done
}

# Função para parar o watcher
stop_watcher() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            rm -f "$PID_FILE"
            echo -e "${GREEN}✅ Watcher parado${NC}"
        else
            echo -e "${YELLOW}Watcher não está rodando${NC}"
        fi
    else
        echo -e "${YELLOW}Nenhum watcher ativo encontrado${NC}"
    fi
}

# Verificar comando
case "$1" in
    stop)
        stop_watcher
        ;;
    status)
        if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
            echo -e "${GREEN}✅ Watcher está ativo (PID: $(cat "$PID_FILE"))${NC}"
            echo ""
            echo "📊 Estatísticas:"
            echo "  Roteiros processados: $(ls -1 "$PROCESSADOS_DIR"/*.pdf 2>/dev/null | wc -l)"
            echo "  Trabalhos do criador: $(ls -1 "$CRIADOR_PROCESSADOS"/*.pdf 2>/dev/null | wc -l)"
            echo "  Memórias totais: $(ls -1 "$MEMORIA_DIR"/*.md 2>/dev/null | wc -l)"
        else
            echo -e "${YELLOW}⚠️ Watcher não está rodando${NC}"
        fi
        ;;
    clean)
        echo "Limpar log de processamento? (s/n)"
        read -r confirm
        if [[ "$confirm" == "s" ]]; then
            rm -f "$WATCH_LOG"
            echo -e "${GREEN}Log limpo${NC}"
        fi
        ;;
    *)
        watch_folders
        ;;
esac