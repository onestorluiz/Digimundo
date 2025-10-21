/**
 * 🖥️ CLAUDE DESKTOP BRIDGE - Conexão com Claude Desktop App
 * 
 * USA O CLAUDE DESKTOP QUE VOCÊ JÁ TEM INSTALADO!
 * Não precisa de API Key - usa AppleScript para comunicar
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'

const execAsync = promisify(exec)

class ClaudeDesktopBridge {
  constructor() {
    this.isAvailable = false
    this.appPath = '/Applications/Claude.app'
    this.checkDesktopApp()
  }

  async checkDesktopApp() {
    try {
      // Verifica se Claude Desktop está instalado
      await fs.access(this.appPath)
      this.isAvailable = true
      console.log('🖥️ [Claude Desktop] App detectado!')
      
      // Verifica se está rodando
      const { stdout } = await execAsync('pgrep -f Claude.app || echo "not running"')
      if (!stdout.includes('not running')) {
        console.log('   ✅ Claude Desktop está rodando')
      } else {
        console.log('   ⚠️ Claude Desktop não está rodando')
        // Tenta abrir
        await this.openClaudeDesktop()
      }
    } catch (error) {
      console.log('❌ Claude Desktop não encontrado em', this.appPath)
      this.isAvailable = false
    }
  }

  async openClaudeDesktop() {
    try {
      console.log('   🚀 Abrindo Claude Desktop...')
      await execAsync('open -a Claude')
      await new Promise(resolve => setTimeout(resolve, 3000)) // Aguarda abrir
      return true
    } catch (error) {
      console.error('❌ Erro ao abrir Claude Desktop:', error)
      return false
    }
  }

  /**
   * Envia mensagem para Claude Desktop via AppleScript
   */
  async sendToClaudeDesktop(message) {
    if (!this.isAvailable) {
      return null
    }

    try {
      // AppleScript para enviar texto ao Claude Desktop
      const script = `
        tell application "Claude"
          activate
        end tell
        
        tell application "System Events"
          delay 0.5
          keystroke "n" using command down
          delay 0.5
          keystroke "${message.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"
          delay 0.5
          keystroke return
        end tell
      `
      
      const { stdout, stderr } = await execAsync(`osascript -e '${script}'`)
      
      // Aguarda resposta (não conseguimos capturar diretamente)
      await new Promise(resolve => setTimeout(resolve, 3000))
      
      // Tenta capturar resposta da janela (limitado)
      const getResponse = `
        tell application "Claude"
          activate
        end tell
        
        tell application "System Events"
          tell process "Claude"
            get value of text area 1 of scroll area 1 of window 1
          end tell
        end tell
      `
      
      try {
        const { stdout: response } = await execAsync(`osascript -e '${getResponse}'`)
        return {
          response: response.trim(),
          fromClaudeDesktop: true
        }
      } catch {
        // Se não conseguir capturar, retorna confirmação
        return {
          response: "Mensagem enviada ao Claude Desktop",
          fromClaudeDesktop: true,
          note: "Verifique a janela do Claude Desktop para ver a resposta"
        }
      }
      
    } catch (error) {
      console.error('❌ Erro ao enviar para Claude Desktop:', error)
      return null
    }
  }

  /**
   * Cria arquivo e abre no Claude Desktop
   */
  async askViaFile(prompt) {
    if (!this.isAvailable) {
      return null
    }

    try {
      // Cria arquivo temporário com a pergunta
      const tempFile = `/tmp/claude_query_${Date.now()}.txt`
      await fs.writeFile(tempFile, prompt)
      
      // Abre o arquivo no Claude Desktop
      await execAsync(`open -a Claude "${tempFile}"`)
      
      // Aguarda processamento
      await new Promise(resolve => setTimeout(resolve, 5000))
      
      // Tenta ler resposta (se Claude salvou)
      const responseFile = tempFile.replace('.txt', '_response.txt')
      try {
        const response = await fs.readFile(responseFile, 'utf-8')
        
        // Limpa arquivos temporários
        await fs.unlink(tempFile).catch(() => {})
        await fs.unlink(responseFile).catch(() => {})
        
        return {
          response: response.trim(),
          fromClaudeDesktop: true,
          method: 'file'
        }
      } catch {
        return {
          response: "Pergunta enviada ao Claude Desktop",
          fromClaudeDesktop: true,
          method: 'file',
          note: "Verifique a janela do Claude Desktop"
        }
      }
      
    } catch (error) {
      console.error('❌ Erro ao usar arquivo:', error)
      return null
    }
  }

  /**
   * Usa URL Scheme claude:// (se suportado)
   */
  async askViaURLScheme(prompt) {
    try {
      const encodedPrompt = encodeURIComponent(prompt)
      const url = `claude://new-conversation?prompt=${encodedPrompt}`
      
      await execAsync(`open "${url}"`)
      
      return {
        response: "Conversa iniciada no Claude Desktop",
        fromClaudeDesktop: true,
        method: 'url-scheme'
      }
    } catch (error) {
      console.error('❌ URL Scheme não suportado')
      return null
    }
  }

  /**
   * Sabiamon pensa via Claude Desktop
   */
  async sabiamonThink(context) {
    const prompt = `Como Sabiamon no Digimundo, você está em ${context.location}, ${context.activity}. 
O que você está pensando? (responda como o sábio mestre Sabiamon)`

    // Tenta diferentes métodos
    let response = await this.sendToClaudeDesktop(prompt)
    if (!response) {
      response = await this.askViaFile(prompt)
    }
    if (!response) {
      response = await this.askViaURLScheme(prompt)
    }
    
    if (response) {
      console.log('🖥️💭 [Sabiamon via Claude Desktop]:', response.note || "Pensando...")
      return response
    }
    
    return null
  }

  /**
   * Status da conexão
   */
  getStatus() {
    return {
      available: this.isAvailable,
      appPath: this.appPath,
      method: 'Claude Desktop App',
      note: 'Usa o app Claude instalado no Mac'
    }
  }
}

// Singleton
let desktopInstance = null

export function getClaudeDesktopBridge() {
  if (!desktopInstance) {
    desktopInstance = new ClaudeDesktopBridge()
  }
  return desktopInstance
}

export { ClaudeDesktopBridge }
export default getClaudeDesktopBridge()