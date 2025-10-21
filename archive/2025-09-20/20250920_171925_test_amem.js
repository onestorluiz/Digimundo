import { getSabiamonAMem } from './app/consciousness/A_MEM_SYSTEM.js'

async function test() {
  const aMem = getSabiamonAMem()
  await aMem.initialize()
  const stats = await aMem.getStats()
  console.log('Stats:', stats)
}

test().catch(console.error)