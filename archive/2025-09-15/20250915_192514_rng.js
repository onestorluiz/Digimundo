/**
 * 🎲 RNG Determinístico para RPG
 * PRNG via mulberry32 para replay e fairness
 */

function seedToInt(seed) {
  let h = 1779033703 ^ seed.length;
  for (let i = 0; i < seed.length; i++) {
    h = Math.imul(h ^ seed.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  return (h >>> 0);
}

function mulberry32(a) {
  return function() {
    let t = a += 0x6D2B79F5;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function roll2d6(rnd) {
  return (1 + Math.floor(rnd()*6)) + (1 + Math.floor(rnd()*6));
}

function rollWithAdv(rnd, mode) {
  if (!mode) return roll2d6(rnd);
  const a = roll2d6(rnd), b = roll2d6(rnd), c = roll2d6(rnd);
  if (mode === 'adv') {
    // Pega 2 melhores de 3
    return Math.max(a,b,c) - Math.min(a,b,c) + Math.min(a,b,c);
  }
  // Pega 2 piores de 3
  return Math.min(a,b,c) - Math.max(a,b,c) + Math.max(a,b,c);
}

module.exports = {
  seedToInt,
  mulberry32,
  roll2d6,
  rollWithAdv
};