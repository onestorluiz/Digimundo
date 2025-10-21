# 🎬 Scripturemon - Professional Screenplay Analyzer

## ✅ APP V2.0 - ELEGANTE & ROBUSTO!

Native macOS application for multi-author screenplay analysis.

---

## 🚀 COMO USAR:

### **Opção 1: Drag & Drop (RECOMENDADO)**

```
1. Arraste um PDF de roteiro para o ícone do app
2. Confirmação aparece com informações do arquivo
3. Clique "Analisar"
4. Terminal abre automaticamente com progresso em tempo real
5. Notificações informam quando termina
```

### **Opção 2: Duplo Clique no App**

```
1. Duplo clique em "Analyze Screenplay.app"
2. Janela de seleção de arquivo abre
3. Escolha seu PDF
4. Confirme a análise
5. Análise inicia automaticamente
```

### **Opção 3: Botão Direito no PDF**

```
1. Clique direito no PDF do roteiro
2. Abrir com → Analyze Screenplay
3. Confirme e pronto!
```

---

## 🎯 MELHORIAS DA VERSÃO 2.0:

### **🔒 Validação Robusta**
- ✅ Verifica se Ollama está instalado e rodando
- ✅ Valida se modelo "scripturemon-optimized" existe
- ✅ Checa permissões do arquivo
- ✅ Alerta se arquivo é muito grande (>50MB)
- ✅ Mostra tamanho do arquivo na confirmação

### **📊 Feedback em Tempo Real**
- ✅ Output do Python sem buffer (`-u` flag)
- ✅ Notificações de progresso durante análise
- ✅ Timestamps de início e término
- ✅ Notificação com som quando completa
- ✅ Mensagens de erro elegantes

### **🧹 Gestão de Recursos**
- ✅ Scripts temporários em `/tmp/scripturemon/`
- ✅ Cleanup automático após execução
- ✅ Logs organizados em `scripturemon/logs/`
- ✅ Tratamento correto de erros com exit status

### **💎 Código Profissional**
- ✅ Funções modulares e reutilizáveis
- ✅ Comentários detalhados
- ✅ Error handling robusto
- ✅ Strict mode (`set -euo pipefail`)
- ✅ Variáveis readonly para configuração

---

## 📁 ESTRUTURA DE OUTPUTS:

```
scripturemon/
├── logs/
│   └── app_YYYYMMDD_HHMMSS.log    (Log completo da execução)
└── workspace/outputs/
    └── [ROTEIRO]_dialogue_XXXX/
        ├── 1_individuais/          (13 análises por autor)
        ├── 2_logs/                 (Logs de execução)
        └── 3_consolidados/         (HTML final consolidado)
```

---

## 🔧 INSTALAÇÃO:

### **Mover para Applications (Recomendado):**

O app já está em `/Applications/`, acessível globalmente!

### **Adicionar ao Dock:**

```
1. Abra /Applications/
2. Arraste "Analyze Screenplay.app" para o Dock
3. Agora pode arrastar PDFs direto para o ícone!
```

### **Ícone Customizado (Opcional):**

```
1. Baixe um ícone .icns de filme/roteiro
2. Salve em: /Applications/Analyze Screenplay.app/Contents/Resources/AppIcon.icns
3. Reinicie o Finder
```

---

## 🛡️ RESOLUÇÃO DE PROBLEMAS:

### **"Ollama não está rodando"**
→ Inicie o Ollama primeiro: `ollama serve`

### **"Modelo não encontrado"**
→ Verifique modelos disponíveis: `ollama list`
→ Crie o modelo se necessário

### **"Arquivo não encontrado"**
→ Certifique-se que o PDF existe e é legível

### **"Permissão negada"**
→ Rode: `chmod +x "/Applications/Analyze Screenplay.app/Contents/MacOS/run"`

### **"App não funciona após atualização do macOS"**
→ Rode: `xattr -cr "/Applications/Analyze Screenplay.app"`

### **Terminal não mostra output**
→ O app usa Python unbuffered (`-u`), output deve aparecer instantaneamente

---

## 📊 O QUE O APP FAZ:

```
✅ Valida ambiente (Ollama, Python, modelo)
✅ Valida arquivo (formato, tamanho, permissões)
✅ Mostra confirmação com informações detalhadas
✅ Abre Terminal com output em tempo real
✅ Notifica progresso periodicamente
✅ Gera 13 análises teóricas individuais
✅ Consolida tudo em HTML profissional
✅ Notifica quando completa (com som!)
✅ Salva logs completos automaticamente
✅ Cleanup automático de arquivos temporários
✅ Tratamento elegante de erros
```

---

## 💡 DICAS PRO:

**1. Monitorar Progresso:**
   - Terminal mostra cada passo da análise
   - Notificações aparecem durante execução
   - Log em tempo real (sem buffer!)

**2. Múltiplas Análises:**
   - Pode iniciar múltiplas análises simultaneamente
   - Cada uma abre nova aba do Terminal
   - Rodam em paralelo sem interferência

**3. Logs Detalhados:**
   - Cada análise salva log em `scripturemon/logs/`
   - Formato: `app_YYYYMMDD_HHMMSS.log`
   - Contém output completo + timestamps

**4. Verificar Saúde do Sistema:**
   - O app valida tudo antes de iniciar
   - Mensagens de erro são claras e acionáveis
   - Não deixa processos orfãos

**5. Performance:**
   - Arquivos grandes (>50MB) recebem aviso
   - Deep mode usa ~128k tokens
   - Tempo: ~30-40 minutos para roteiro padrão

---

## 🔍 CARACTERÍSTICAS TÉCNICAS:

**Bash Script Profissional:**
- Strict mode (`set -euo pipefail`)
- Error handling robusto
- Funções modulares
- Cleanup automático
- Exit codes corretos

**Python Integration:**
- Unbuffered output (`python3 -u`)
- Environment variable (`PYTHONUNBUFFERED=1`)
- Output em tempo real via pipe
- Exit status checking

**macOS Native:**
- AppleScript para diálogos
- Notification Center integration
- Terminal automation
- Sound alerts
- File type registration

---

## 🎉 PRONTO PARA USAR!

**Arraste seu roteiro e deixe a IA trabalhar!** 🥷

- ⚡ Rápido e eficiente
- 🎯 Preciso e confiável
- 💎 Elegante e profissional
- 🔒 Robusto e seguro

---

## 📝 CHANGELOG:

**v2.0 (Current):**
- Refatoração completa do código
- Validação robusta de ambiente
- Output em tempo real (unbuffered)
- Notificações de progresso
- Tratamento elegante de erros
- Cleanup automático
- Logs com timestamps
- Mensagens profissionais

**v1.0:**
- Versão inicial
- Drag & drop básico
- File picker dialog

---

**Digimundo Presente**
Scripturemon v2.0 - Professional Multi-Author Screenplay Analyzer
