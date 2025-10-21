export const ONLINE = process.env.DIGI_OFFLINE === '1' ? false : true

export async function offlineFetchGuard(url, opts){
  if (!ONLINE) throw new Error('Air-gapped: rede desativada (DIGI_OFFLINE=1)')
  const r = await fetch(url, opts)
  if (!r.ok) throw new Error(`HTTP ${r.status} ${url}`)
  return r
}
