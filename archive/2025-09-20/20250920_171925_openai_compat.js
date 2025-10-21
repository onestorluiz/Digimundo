import fs from 'node:fs'
let llama = null
try {
  llama = await import('node-llama-cpp') // opcional; se falhar, usamos mock
} catch (e) {
  console.warn('[llm] node-llama-cpp não disponível; usando mock para testes.')
}
import { getModelPath } from './tools/config.js'

let cached = { ctx: null, modelPath: null }

async function ensureModel(){
  const modelPath = getModelPath()
  if (!modelPath) throw new Error('Sem modelo configurado. Use /digimundo/models/set ou a UI.')
  if (!fs.existsSync(modelPath)) throw new Error('Modelo não encontrado: ' + modelPath)
  if (!llama) return { mock: true }
  if (cached.ctx && cached.modelPath === modelPath) return cached.ctx

  const { LlamaModel, LlamaContext } = llama
  const model = new LlamaModel({ modelPath })
  const context = new LlamaContext({ model, contextSize: 4096 })
  cached = { ctx: { model, context }, modelPath }
  return cached.ctx
}

export async function chatCompletionsHandler(req, res){
  try {
    const { messages, max_tokens = 256, temperature = 0.7 } = req.body || {}
    if (!Array.isArray(messages)) return res.status(400).json({ error: 'messages required' })
    const sys = messages.filter(m=>m.role==='system').map(m=>m.content).join('\n')
    const user = messages.filter(m=>m.role!=='system').map(m=>`${m.role}: ${m.content}`).join('\n')

    const ctx = await ensureModel()
    res.setHeader('x-model', getModelPath())

    if (ctx.mock) {
      const text = `[MOCK] Digimundo pronto. Você disse: ${user.slice(-200)}`
      return res.json({
        id:'mock', object:'chat.completion',
        choices:[{ index:0, message:{ role:'assistant', content:text }, finish_reason:'stop' }],
        usage:{ prompt_tokens:user.length/4|0, completion_tokens:text.length/4|0, total_tokens:0 }
      })
    }

    const { LlamaChatSession } = llama
    const session = new LlamaChatSession({ context: ctx.context, systemPrompt: sys || 'Você é o Digimundo (Scripturemon), útil e offline.' })
    const out = await session.prompt(user, { temperature, maxTokens: max_tokens })
    return res.json({
      id: 'local-1',
      object: 'chat.completion',
      choices: [{ index:0, message: { role:'assistant', content: out }, finish_reason: 'stop' }],
      usage: { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 }
    })
  } catch (e) {
    console.error(e)
    res.status(500).json({ error: String(e) })
  }
}
