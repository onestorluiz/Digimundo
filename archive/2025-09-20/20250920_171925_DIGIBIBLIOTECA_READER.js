/**
 * 📚 DIGIBIBLIOTECA READER - Sistema de Aprendizado Contínuo
 * 
 * Os Digimons leem e aprendem automaticamente com o conteúdo da biblioteca
 * Extrai conhecimento de PDFs, textos, documentos e integra à memória
 */

import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)
const __dirname = path.dirname(fileURLToPath(import.meta.url))

class DigibibliotecaReader {
  constructor() {
    this.bibliotecaPath = path.join(__dirname, '../../Digibiblioteca')
    this.logsPath = path.join(__dirname, '../../biblioteca_logs')
    this.scanInterval = 30 * 60 * 1000 // 30 minutos
    this.lastScan = new Map()
    this.knowledgeBase = new Map()
    this.isScanning = false
    
    this.initializeDirectories()
  }

  async initializeDirectories() {
    try {
      await fs.mkdir(this.logsPath, { recursive: true })
      console.log('📚 [Digibiblioteca] Sistema de leitura inicializado')
    } catch (error) {
      console.error('❌ Erro ao inicializar diretórios:', error)
    }
  }

  /**
   * INICIAR MONITORAMENTO CONTÍNUO
   */
  async startContinuousLearning() {
    console.log('🧠 [Digibiblioteca] Iniciando aprendizado contínuo dos Digimons')
    console.log(`   📁 Monitorando: ${this.bibliotecaPath}`)
    console.log(`   ⏱️ Intervalo: ${this.scanInterval / 1000 / 60} minutos`)
    
    // Scan inicial
    await this.scanAndLearn()
    
    // Loop contínuo
    setInterval(async () => {
      if (!this.isScanning) {
        await this.scanAndLearn()
      }
    }, this.scanInterval)
  }

  /**
   * ESCANEAR E APRENDER COM NOVOS CONTEÚDOS
   */
  async scanAndLearn() {
    this.isScanning = true
    const startTime = Date.now()
    
    console.log(`\\n📚 [${new Date().toLocaleTimeString()}] Iniciando scan da Digibiblioteca...`)
    
    try {
      const categories = ['livros', 'roteiros', 'artigos', 'referencias', 'estudos']
      let totalFiles = 0
      let newFiles = 0
      let learnedContent = []

      for (const category of categories) {
        const categoryPath = path.join(this.bibliotecaPath, category)
        
        try {
          const files = await this.scanDirectory(categoryPath)
          totalFiles += files.length
          
          for (const file of files) {
            const filePath = path.join(categoryPath, file)
            const stats = await fs.stat(filePath)
            const lastModified = stats.mtime.getTime()
            
            // Verificar se arquivo é novo ou foi modificado
            if (!this.lastScan.has(filePath) || this.lastScan.get(filePath) < lastModified) {
              console.log(`   📖 Lendo: ${category}/${file}`)
              
              const content = await this.extractContent(filePath, file)
              if (content) {
                const knowledge = await this.processKnowledge(content, category, file)
                if (knowledge) {
                  learnedContent.push(knowledge)
                  newFiles++
                  
                  // Integrar ao sistema de memória dos Digimons
                  await this.integrateToDigimonMemory(knowledge)
                }
              }
              
              this.lastScan.set(filePath, lastModified)
            }
          }
        } catch (error) {
          if (error.code !== 'ENOENT') {
            console.error(`   ❌ Erro em ${category}:`, error.message)
          }
        }
      }

      const duration = Date.now() - startTime
      
      console.log(`\\n📊 [Scan Completo] ${duration}ms`)
      console.log(`   📁 Arquivos totais: ${totalFiles}`)
      console.log(`   🆕 Novos/Modificados: ${newFiles}`)
      console.log(`   🧠 Conhecimentos extraídos: ${learnedContent.length}`)
      
      // Salvar log
      await this.saveLog({
        timestamp: new Date(),
        duration,
        totalFiles,
        newFiles,
        learnedContent: learnedContent.length,
        categories: categories.map(cat => ({ 
          name: cat, 
          processed: learnedContent.filter(k => k.category === cat).length 
        }))
      })

    } catch (error) {
      console.error('❌ Erro durante scan:', error)
    } finally {
      this.isScanning = false
    }
  }

  /**
   * ESCANEAR DIRETÓRIO
   */
  async scanDirectory(dirPath) {
    try {
      const files = await fs.readdir(dirPath)
      return files.filter(file => {
        const ext = path.extname(file).toLowerCase()
        return ['.pdf', '.txt', '.md', '.docx', '.doc'].includes(ext)
      })
    } catch (error) {
      return []
    }
  }

  /**
   * EXTRAIR CONTEÚDO DE ARQUIVOS
   */
  async extractContent(filePath, fileName) {
    const ext = path.extname(fileName).toLowerCase()
    
    try {
      switch (ext) {
        case '.txt':
        case '.md':
          return await fs.readFile(filePath, 'utf8')
          
        case '.pdf':
          return await this.extractFromPDF(filePath)
          
        case '.docx':
        case '.doc':
          return await this.extractFromWord(filePath)
          
        default:
          console.log(`   ⚠️ Formato não suportado: ${ext}`)
          return null
      }
    } catch (error) {
      console.error(`   ❌ Erro ao extrair ${fileName}:`, error.message)
      return null
    }
  }

  /**
   * EXTRAIR TEXTO DE PDF
   */
  async extractFromPDF(filePath) {
    try {
      // Usar pdftotext se disponível
      const { stdout } = await execAsync(`pdftotext "${filePath}" - 2>/dev/null`)
      return stdout
    } catch {
      try {
        // Fallback: tentar pdf-parse via node
        const pdfData = await fs.readFile(filePath)
        // Implementação básica - poderia usar pdf-parse se instalado
        return `[PDF] ${path.basename(filePath)} - Conteúdo requer processamento específico`
      } catch {
        return `[PDF] ${path.basename(filePath)} - Não foi possível extrair texto`
      }
    }
  }

  /**
   * EXTRAIR TEXTO DE WORD
   */
  async extractFromWord(filePath) {
    try {
      // Tentar pandoc se disponível
      const { stdout } = await execAsync(`pandoc "${filePath}" -t plain 2>/dev/null`)
      return stdout
    } catch {
      return `[DOC] ${path.basename(filePath)} - Conteúdo requer conversão`
    }
  }

  /**
   * PROCESSAR CONHECIMENTO EXTRAÍDO
   */
  async processKnowledge(content, category, fileName) {
    if (!content || content.length < 100) return null

    // Extrair insights principais
    const insights = this.extractInsights(content, category)
    
    // Extrair conceitos cinematográficos
    const cinematicConcepts = this.extractCinematicConcepts(content)
    
    // Extrair técnicas narrativas
    const narrativeTechniques = this.extractNarrativeTechniques(content)

    const knowledge = {
      id: `${category}_${fileName}_${Date.now()}`,
      source: fileName,
      category: category,
      extractedAt: new Date(),
      content: content.substring(0, 5000), // Primeiros 5k chars
      wordCount: content.split(' ').length,
      insights: insights,
      cinematicConcepts: cinematicConcepts,
      narrativeTechniques: narrativeTechniques,
      tags: this.extractTags(content, category),
      relevanceScore: this.calculateRelevance(content, category)
    }

    this.knowledgeBase.set(knowledge.id, knowledge)
    return knowledge
  }

  /**
   * EXTRAIR INSIGHTS PRINCIPAIS
   */
  extractInsights(content, category) {
    const insights = []
    
    // Buscar padrões específicos por categoria
    if (category === 'roteiros') {
      const scenePattern = /(FADE IN|INT\.|EXT\.)/gi
      const dialoguePattern = /^[A-Z\\s]+$/gm
      
      if (scenePattern.test(content)) {
        insights.push('Estrutura de roteiro cinematográfico detectada')
      }
    }
    
    if (category === 'livros') {
      if (content.includes('personagem') || content.includes('protagonista')) {
        insights.push('Técnicas de desenvolvimento de personagem')
      }
      if (content.includes('narrativa') || content.includes('estrutura')) {
        insights.push('Elementos de estrutura narrativa')
      }
    }

    return insights
  }

  /**
   * EXTRAIR CONCEITOS CINEMATOGRÁFICOS
   */
  extractCinematicConcepts(content) {
    const concepts = []
    const cinematicTerms = [
      'plano', 'enquadramento', 'montagem', 'edição', 'trilha sonora',
      'iluminação', 'cinematografia', 'direção', 'roteiro', 'diálogo',
      'personagem', 'protagonista', 'antagonista', 'conflito', 'clímax',
      'plot twist', 'flashback', 'mise en scène', 'close-up', 'travelling'
    ]

    for (const term of cinematicTerms) {
      const regex = new RegExp(`\\\\b${term}\\\\b`, 'gi')
      if (regex.test(content)) {
        concepts.push(term)
      }
    }

    return [...new Set(concepts)] // Remove duplicatas
  }

  /**
   * EXTRAIR TÉCNICAS NARRATIVAS
   */
  extractNarrativeTechniques(content) {
    const techniques = []
    
    if (content.includes('três atos') || content.includes('3 atos')) {
      techniques.push('Estrutura de três atos')
    }
    if (content.includes('jornada do herói')) {
      techniques.push('Jornada do herói')
    }
    if (content.includes("show, don't tell")) {
      techniques.push("Show, don't tell")
    }

    return techniques
  }

  /**
   * EXTRAIR TAGS
   */
  extractTags(content, category) {
    const tags = [category]
    
    // Tags baseadas em palavras-chave
    const keywordMap = {
      'cinema': ['filme', 'diretor', 'ator', 'produção'],
      'narrativa': ['história', 'enredo', 'personagem', 'narrativa'],
      'técnica': ['técnica', 'método', 'abordagem', 'processo'],
      'teoria': ['teoria', 'conceito', 'princípio', 'fundamento']
    }

    for (const [tag, keywords] of Object.entries(keywordMap)) {
      if (keywords.some(keyword => content.toLowerCase().includes(keyword))) {
        tags.push(tag)
      }
    }

    return tags
  }

  /**
   * CALCULAR RELEVÂNCIA
   */
  calculateRelevance(content, category) {
    let score = 50 // Base score
    
    // Pontuação por categoria
    const categoryScores = {
      'roteiros': 80,
      'livros': 70,
      'artigos': 60,
      'estudos': 75,
      'referencias': 40
    }
    
    score = categoryScores[category] || 50
    
    // Ajustar por tamanho do conteúdo
    const wordCount = content.split(' ').length
    if (wordCount > 5000) score += 20
    else if (wordCount > 1000) score += 10
    
    // Ajustar por termos cinematográficos
    const cinematicTerms = this.extractCinematicConcepts(content)
    score += cinematicTerms.length * 2
    
    return Math.min(score, 100)
  }

  /**
   * INTEGRAR AO SISTEMA DE MEMÓRIA DOS DIGIMONS
   */
  async integrateToDigimonMemory(knowledge) {
    try {
      // Preparar para cada Digimon específico
      const digimonLearning = {
        'Scripturemon': this.prepareForScripturemon(knowledge),
        'Ajamon': this.prepareForAjamon(knowledge),
        'Fundamon': this.prepareForFundamon(knowledge),
        'Sabiamon': this.prepareForSabiamon(knowledge)
      }

      // Salvar na memória compartilhada
      const memoryPath = path.join(__dirname, '../consciousness/biblioteca_knowledge.json')
      let existingKnowledge = []
      
      try {
        const data = await fs.readFile(memoryPath, 'utf8')
        existingKnowledge = JSON.parse(data)
      } catch {
        // Arquivo não existe ainda
      }

      existingKnowledge.push({
        ...knowledge,
        digimonSpecific: digimonLearning,
        integratedAt: new Date()
      })

      // Manter apenas últimos 1000 conhecimentos
      if (existingKnowledge.length > 1000) {
        existingKnowledge = existingKnowledge.slice(-1000)
      }

      await fs.writeFile(memoryPath, JSON.stringify(existingKnowledge, null, 2))
      
      console.log(`   🧠 Conhecimento integrado: ${knowledge.source}`)
      
    } catch (error) {
      console.error('   ❌ Erro ao integrar conhecimento:', error.message)
    }
  }

  /**
   * PREPARAR CONHECIMENTO PARA SCRIPTUREMON
   */
  prepareForScripturemon(knowledge) {
    return {
      focus: 'Estrutura narrativa e roteiro',
      relevantFor: knowledge.category === 'roteiros' ? 'Alta' : 'Média',
      applicationHints: [
        'Usar para melhorar estrutura de roteiros',
        'Aplicar técnicas narrativas descobertas',
        'Incorporar diálogos e formatos aprendidos'
      ],
      keyTakeaways: knowledge.narrativeTechniques
    }
  }

  /**
   * PREPARAR CONHECIMENTO PARA AJAMON
   */
  prepareForAjamon(knowledge) {
    return {
      focus: 'Aspectos emocionais e desenvolvimento de personagem',
      relevantFor: knowledge.cinematicConcepts.length > 0 ? 'Alta' : 'Baixa',
      applicationHints: [
        'Usar para enriquecer personagens',
        'Aplicar em desenvolvimento emocional',
        'Incorporar em aspectos de produção'
      ],
      keyTakeaways: knowledge.insights
    }
  }

  /**
   * PREPARAR CONHECIMENTO PARA FUNDAMON
   */
  prepareForFundamon(knowledge) {
    return {
      focus: 'Fundamentos técnicos e práticos',
      relevantFor: knowledge.category === 'estudos' ? 'Alta' : 'Média',
      applicationHints: [
        'Aplicar em aspectos técnicos de produção',
        'Usar para fundamentar decisões criativas',
        'Incorporar em metodologias de trabalho'
      ],
      keyTakeaways: knowledge.cinematicConcepts
    }
  }

  /**
   * PREPARAR CONHECIMENTO PARA SABIAMON
   */
  prepareForSabiamon(knowledge) {
    return {
      focus: 'Síntese e sabedoria cinematográfica',
      relevantFor: 'Sempre Alta',
      applicationHints: [
        'Integrar todos os aspectos aprendidos',
        'Usar para orientar outros Digimons',
        'Aplicar em visão holística de projetos'
      ],
      keyTakeaways: [...knowledge.insights, ...knowledge.cinematicConcepts, ...knowledge.narrativeTechniques]
    }
  }

  /**
   * SALVAR LOG
   */
  async saveLog(logData) {
    try {
      const logFile = path.join(this.logsPath, `scan_${new Date().toISOString().split('T')[0]}.json`)
      
      let logs = []
      try {
        const data = await fs.readFile(logFile, 'utf8')
        logs = JSON.parse(data)
      } catch {
        // Novo arquivo
      }

      logs.push(logData)
      await fs.writeFile(logFile, JSON.stringify(logs, null, 2))
      
    } catch (error) {
      console.error('❌ Erro ao salvar log:', error)
    }
  }

  /**
   * OBTER ESTATÍSTICAS
   */
  getStats() {
    return {
      totalKnowledge: this.knowledgeBase.size,
      lastScanFiles: this.lastScan.size,
      isCurrentlyScanning: this.isScanning,
      scanInterval: this.scanInterval,
      categories: ['livros', 'roteiros', 'artigos', 'referencias', 'estudos']
    }
  }

  /**
   * BUSCAR CONHECIMENTO
   */
  searchKnowledge(query, category = null) {
    const results = []
    
    for (const [id, knowledge] of this.knowledgeBase) {
      if (category && knowledge.category !== category) continue
      
      const content = knowledge.content.toLowerCase()
      if (content.includes(query.toLowerCase()) || 
          knowledge.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))) {
        results.push(knowledge)
      }
    }

    return results.sort((a, b) => b.relevanceScore - a.relevanceScore)
  }
}

// Singleton
let readerInstance = null

export function getDigibibliotecaReader() {
  if (!readerInstance) {
    readerInstance = new DigibibliotecaReader()
  }
  return readerInstance
}

export { DigibibliotecaReader }
export default getDigibibliotecaReader()