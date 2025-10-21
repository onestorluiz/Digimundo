/**
 * 🤖 CLAUDE CODE INTEGRATION
 * Integração nativa com Claude Code CLI
 */

const { exec, spawn } = require('child_process');
const { promisify } = require('util');
const path = require('path');
const fs = require('fs').promises;
const os = require('os');

const execAsync = promisify(exec);

class ClaudeIntegration {
  constructor() {
    this.claudePath = null;
    this.isAvailable = false;
    this.claudeProcess = null;
    this.sessionActive = false;
    
    this.detectClaude();
  }

  async detectClaude() {
    try {
      // Tenta encontrar Claude em vários locais
      const homePath = os.homedir();
      const possiblePaths = [
        '/Users/clubproducoes/.local/bin/claude',
        '/usr/local/bin/claude',
        '/opt/homebrew/bin/claude',
        path.join(homePath, '.local/bin/claude')
      ];

      for (const claudePath of possiblePaths) {
        try {
          await fs.access(claudePath);
          this.claudePath = claudePath;
          this.isAvailable = true;
          
          // Verifica versão
          const { stdout } = await execAsync(`${claudePath} --version`);
          console.log('✅ Claude Code encontrado:', claudePath);
          console.log('   Versão:', stdout.trim());
          
          // Verifica se há sessão ativa
          await this.checkSession();
          break;
        } catch {
          continue;
        }
      }

      if (!this.isAvailable) {
        // Tenta com which
        try {
          const { stdout } = await execAsync('which claude');
          if (stdout.trim()) {
            this.claudePath = stdout.trim();
            this.isAvailable = true;
            console.log('✅ Claude Code encontrado via PATH:', this.claudePath);
          }
        } catch {
          console.log('⚠️ Claude Code não encontrado no sistema');
        }
      }
    } catch (error) {
      console.error('Erro ao detectar Claude:', error);
    }
  }

  async checkSession() {
    try {
      // Verifica se há credenciais válidas
      const homePath = os.homedir();
      const configPath = path.join(homePath, '.config', 'claude', 'config.json');
      await fs.access(configPath);
      
      // Testa um comando simples
      const { stdout } = await execAsync(`${this.claudePath} echo "test" 2>&1 | head -1`);
      
      if (stdout && !stdout.includes('error') && !stdout.includes('login')) {
        this.sessionActive = true;
        console.log('✅ Sessão Claude ativa');
        return true;
      }
    } catch {
      console.log('⚠️ Sem sessão ativa do Claude');
      return false;
    }
  }

  /**
   * Abre Claude Code em uma nova janela de terminal
   */
  async openClaude(options = {}) {
    if (!this.isAvailable) {
      throw new Error('Claude Code não está instalado');
    }

    const { projectPath, message } = options;
    
    try {
      let command = `${this.claudePath}`;
      
      // Adiciona diretório do projeto se especificado
      if (projectPath) {
        command += ` --dir "${projectPath}"`;
      }
      
      // Adiciona mensagem inicial se especificada
      if (message) {
        command += ` --message "${message}"`;
      }

      // Abre em novo terminal no macOS
      const terminalCommand = `osascript -e 'tell app "Terminal" to do script "${command}"'`;
      
      await execAsync(terminalCommand);
      console.log('✅ Claude Code aberto com sucesso');
      
      return true;
    } catch (error) {
      console.error('Erro ao abrir Claude:', error);
      throw error;
    }
  }

  /**
   * Envia comando para Claude via CLI
   */
  async sendToClaude(prompt, options = {}) {
    if (!this.isAvailable) {
      throw new Error('Claude Code não está instalado');
    }

    try {
      // Cria arquivo temporário com o prompt
      const tempDir = os.tmpdir();
      const tempFile = path.join(tempDir, `claude-prompt-${Date.now()}.txt`);
      await fs.writeFile(tempFile, prompt);

      // Executa Claude com o prompt
      const command = `${this.claudePath} < "${tempFile}"`;
      const { stdout, stderr } = await execAsync(command, {
        maxBuffer: 1024 * 1024 * 10 // 10MB buffer
      });

      // Remove arquivo temporário
      await fs.unlink(tempFile).catch(() => {});

      if (stderr && stderr.includes('error')) {
        throw new Error(stderr);
      }

      return stdout;
    } catch (error) {
      console.error('Erro ao enviar para Claude:', error);
      throw error;
    }
  }

  /**
   * Inicia sessão interativa com Claude
   */
  startInteractiveSession() {
    if (!this.isAvailable) {
      throw new Error('Claude Code não está instalado');
    }

    if (this.claudeProcess) {
      console.log('Sessão já ativa');
      return this.claudeProcess;
    }

    try {
      this.claudeProcess = spawn(this.claudePath, [], {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      this.claudeProcess.stdout.on('data', (data) => {
        console.log('Claude:', data.toString());
      });

      this.claudeProcess.stderr.on('data', (data) => {
        console.error('Claude Error:', data.toString());
      });

      this.claudeProcess.on('close', (code) => {
        console.log(`Claude process exited with code ${code}`);
        this.claudeProcess = null;
      });

      console.log('✅ Sessão interativa iniciada');
      return this.claudeProcess;
    } catch (error) {
      console.error('Erro ao iniciar sessão:', error);
      throw error;
    }
  }

  /**
   * Envia mensagem para sessão interativa
   */
  sendToSession(message) {
    if (!this.claudeProcess) {
      throw new Error('Nenhuma sessão ativa');
    }

    this.claudeProcess.stdin.write(message + '\n');
  }

  /**
   * Encerra sessão interativa
   */
  endSession() {
    if (this.claudeProcess) {
      this.claudeProcess.kill();
      this.claudeProcess = null;
      console.log('Sessão encerrada');
    }
  }

  /**
   * Verifica e instala Claude se necessário
   */
  async installClaudeIfNeeded() {
    if (this.isAvailable) {
      return true;
    }

    try {
      console.log('📦 Instalando Claude Code...');
      const { stdout, stderr } = await execAsync('npm install -g @anthropic-ai/claude-code');
      
      if (stderr && stderr.includes('error')) {
        throw new Error(stderr);
      }

      console.log('✅ Claude Code instalado com sucesso');
      await this.detectClaude();
      return this.isAvailable;
    } catch (error) {
      console.error('Erro ao instalar Claude:', error);
      return false;
    }
  }
}

module.exports = ClaudeIntegration;