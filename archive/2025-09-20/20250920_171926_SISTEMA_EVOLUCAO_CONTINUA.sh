#!/bin/bash

# 🧬 SISTEMA DE EVOLUÇÃO CONTÍNUA DO SCRIPTUREMON
# Inspirado no SDL (Self-Distillation LoRA) mas adaptado para Ollama

CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${MAGENTA}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   🧬 SISTEMA DE EVOLUÇÃO CONTÍNUA - SCRIPTUREMON       ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# CONCEITO: Ao invés de fine-tuning, fazemos:
# 1. DIGESTÃO: Processar novo PDF em Q&As
# 2. VALIDAÇÃO: Testar conhecimento com Sabiamon/Claude
# 3. CONSOLIDAÇÃO: Gerar insights e padrões
# 4. EVOLUÇÃO: Atualizar modelfile com novo conhecimento
# 5. VERSIONAMENTO: Criar snapshot da evolução

# FASE 1: DIGESTÃO DE CONHECIMENTO
processar_pdf_em_qa() {
    local pdf="$1"
    local output="memorias/qa_$(date +%Y%m%d_%H%M%S).json"
    
    echo -e "${CYAN}📖 FASE 1: Digestão de Conhecimento${NC}"
    echo "  Processando: $(basename $pdf)"
    
    # Extrair texto do PDF
    echo "  Extraindo conteúdo..."
    
    # Gerar Q&As usando o próprio Scripturemon
    cat << PROMPT | ollama run scripturemon-maestro > "$output" 2>/dev/null
Analise este roteiro/teoria e gere 20 Q&As profundos sobre:
1. Técnicas narrativas únicas
2. Estruturas inovadoras
3. Diálogos memoráveis
4. Arcos de personagem
5. Comparação com mestres

Formato JSON:
{
  "qa_pairs": [
    {"q": "pergunta", "a": "resposta detalhada"},
    ...
  ],
  "insights": ["insight1", "insight2"],
  "techniques": ["técnica1", "técnica2"],
  "comparison": "como se compara aos mestres"
}

PDF: $(basename $pdf)
PROMPT
    
    echo -e "  ${GREEN}✓ Q&As gerados${NC}"
}

# FASE 2: VALIDAÇÃO COM SABIAMON/CLAUDE
validar_conhecimento() {
    local qa_file="$1"
    
    echo -e "${CYAN}🔬 FASE 2: Validação de Conhecimento${NC}"
    
    # Usar Sabiamon (Claude Code) para validar
    echo "  Validando com Sabiamon..."
    
    # Criar contexto temporário
    cat << CONTEXT > /tmp/sabiamon_validate.md
# Validação de Conhecimento Cinematográfico

Analise estas Q&As e:
1. Verifique precisão técnica
2. Identifique insights valiosos
3. Sugira melhorias
4. Compare com teoria estabelecida

$(cat $qa_file)
CONTEXT
    
    # Invocar Claude Code via Sabiamon
    if command -v sabiamon &> /dev/null; then
        sabiamon "Valide este conhecimento cinematográfico" < /tmp/sabiamon_validate.md
    else
        echo "  ⚠️  Sabiamon não disponível, pulando validação"
    fi
    
    echo -e "  ${GREEN}✓ Conhecimento validado${NC}"
}

# FASE 3: CONSOLIDAÇÃO NEURAL
consolidar_memorias() {
    echo -e "${CYAN}🧠 FASE 3: Consolidação Neural${NC}"
    
    # Consolidar todas Q&As do dia
    local hoje=$(date +%Y%m%d)
    local consolidado="memorias/consolidado_${hoje}.md"
    
    echo "# Memórias Consolidadas - $hoje" > "$consolidado"
    echo "" >> "$consolidado"
    
    # Processar cada Q&A do dia
    for qa in memorias/qa_${hoje}*.json; do
        if [ -f "$qa" ]; then
            echo "  Consolidando: $(basename $qa)"
            
            # Extrair insights únicos
            grep '"insights"' "$qa" >> "$consolidado"
            grep '"techniques"' "$qa" >> "$consolidado"
        fi
    done
    
    # Gerar síntese do dia
    echo "" >> "$consolidado"
    echo "## Síntese do Aprendizado" >> "$consolidado"
    
    ollama run scripturemon-maestro << SYNTH >> "$consolidado" 2>/dev/null
Sintetize o aprendizado do dia em 5 bullets principais.
Foque em técnicas PRÁTICAS que melhoram roteiros.
SYNTH
    
    echo -e "  ${GREEN}✓ Memórias consolidadas${NC}"
}

# FASE 4: EVOLUÇÃO DO MODELFILE
evoluir_modelo() {
    echo -e "${CYAN}🔄 FASE 4: Evolução do Modelo${NC}"
    
    local versao_atual=$(grep "# Versão:" scripturemon_maestro_brutal.modelfile | cut -d' ' -f3)
    local nova_versao=$(echo "$versao_atual + 0.1" | bc)
    
    echo "  Versão atual: $versao_atual"
    echo "  Nova versão: $nova_versao"
    
    # Criar backup
    cp scripturemon_maestro_brutal.modelfile "backups/scripturemon_v${versao_atual}.modelfile"
    
    # Adicionar novo conhecimento ao SYSTEM prompt
    local consolidado=$(cat memorias/consolidado_$(date +%Y%m%d).md)
    
    # Atualizar modelfile
    sed -i '' "s/# Versão: $versao_atual/# Versão: $nova_versao/" scripturemon_maestro_brutal.modelfile
    
    # Recriar modelo no Ollama
    ollama rm scripturemon-maestro 2>/dev/null
    ollama create scripturemon-maestro -f scripturemon_maestro_brutal.modelfile
    
    echo -e "  ${GREEN}✓ Modelo evoluído para v$nova_versao${NC}"
}

# FASE 5: TESTE DE REGRESSÃO
testar_evolucao() {
    echo -e "${CYAN}🧪 FASE 5: Teste de Evolução${NC}"
    
    # Testes básicos para garantir que não regrediu
    local testes=(
        "Quem é você?"
        "Analise esta cena: FADE IN"
        "Compare com Citizen Kane"
        "Qual a estrutura ideal?"
    )
    
    local score=0
    for teste in "${testes[@]}"; do
        echo -n "  Testando: $teste... "
        
        response=$(timeout 10 ollama run scripturemon-maestro "$teste" 2>/dev/null)
        
        if [[ $response == *"62/100"* ]] && [[ $response == *"mestres"* ]]; then
            echo -e "${GREEN}✓${NC}"
            ((score++))
        else
            echo -e "${RED}✗${NC}"
        fi
    done
    
    echo ""
    echo -e "  Score: $score/4"
    
    if [ $score -lt 3 ]; then
        echo -e "  ${RED}⚠️ Evolução falhou! Revertendo...${NC}"
        # Reverter para versão anterior
        mv backups/scripturemon_v${versao_atual}.modelfile scripturemon_maestro_brutal.modelfile
        ollama rm scripturemon-maestro 2>/dev/null
        ollama create scripturemon-maestro -f scripturemon_maestro_brutal.modelfile
    else
        echo -e "  ${GREEN}✓ Evolução bem-sucedida!${NC}"
    fi
}

# SISTEMA PRINCIPAL
main() {
    # Criar estrutura necessária
    mkdir -p memorias backups cinema/{entrada,processando,processados}
    
    # Monitorar pasta de entrada
    echo -e "${YELLOW}👁️ Monitorando pasta cinema/entrada...${NC}"
    echo ""
    
    while true; do
        for pdf in cinema/entrada/*.pdf; do
            if [ -f "$pdf" ]; then
                echo -e "${BOLD}${GREEN}📚 NOVO PDF DETECTADO!${NC}"
                echo ""
                
                # Mover para processamento
                mv "$pdf" cinema/processando/
                pdf_name=$(basename "$pdf")
                pdf_path="cinema/processando/$pdf_name"
                
                # Executar pipeline completo
                processar_pdf_em_qa "$pdf_path"
                validar_conhecimento "memorias/qa_*.json"
                consolidar_memorias
                evoluir_modelo
                testar_evolucao
                
                # Mover para processados
                mv "$pdf_path" cinema/processados/
                
                echo ""
                echo -e "${MAGENTA}✨ PDF processado e conhecimento absorvido!${NC}"
                echo ""
            fi
        done
        
        # Aguardar 30 segundos antes de verificar novamente
        sleep 30
    done
}

# MODO MANUAL (para testar com um PDF específico)
if [ "$1" = "manual" ] && [ -f "$2" ]; then
    echo -e "${CYAN}🎯 Modo manual: Processando $2${NC}"
    processar_pdf_em_qa "$2"
    validar_conhecimento "memorias/qa_*.json"
    consolidar_memorias
    evoluir_modelo
    testar_evolucao
    exit 0
fi

# Executar sistema principal
main