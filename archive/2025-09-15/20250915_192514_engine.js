/**
 * ⚙️ RPG Engine - Motor Principal do Sistema de Combate
 */

const { DC_TABLE, CATEGORY_XP_BASE, xpNext, mod } = require('./config');
const { mulberry32, seedToInt, rollWithAdv } = require('./rng');
const { CLASS_DEFS } = require('./classes');

function initContext(actor, input, team) {
  return { 
    actor, 
    team, 
    input, 
    transient: { 
      advantage: input.advantage ?? null, 
      bonuses: 0, 
      penalties: 0, 
      notes: [] 
    } 
  };
}

function synergyBonus(ctx) {
  if (!ctx.team) return 0;
  const classes = new Set(ctx.team.members.map(m => m.classId));
  let bonus = Math.min(4, classes.size - 1); // +1 por classe distinta (além do próprio)
  
  // Masteries e Signatures podem somar
  for (const m of ctx.team.members) {
    const def = CLASS_DEFS[m.classId];
    if (m.level >= def.mastery.levelReq) bonus += 1;
  }
  
  // Composição ideal em raids
  if (ctx.input.category === 'RAID' && classes.size >= 4) bonus += 1;
  
  return bonus;
}

function performAction(actor, input, team) {
  const ctx = initContext(actor, input, team);
  
  // Aplicar perks de classe
  const def = CLASS_DEFS[actor.classId];
  if (actor.level >= def.signature.levelReq) {
    def.signature.apply(ctx);
  }
  if (actor.level >= def.mastery.levelReq) {
    def.mastery.apply(ctx);
  }
  if (actor.level >= def.capstone.levelReq) {
    def.capstone.apply(ctx);
  }

  // RNG determinístico
  const rnd = mulberry32(seedToInt(input.seed || `${actor.id}:${Date.now()}`));

  // Rolagem base
  const baseRoll = rollWithAdv(rnd, ctx.transient.advantage ?? null);
  const attrVal = actor.attrs[input.relatedAttr];
  const skillVal = actor.skills[input.skill] || 0;
  const levelBonus = Math.floor(actor.level / 3);
  const teamBonus = synergyBonus(ctx);

  const score = baseRoll
    + mod(attrVal)
    + 2 * skillVal
    + levelBonus
    + teamBonus
    + ctx.transient.bonuses
    - ctx.transient.penalties;

  const dc = DC_TABLE[input.difficulty];
  const margin = score - dc;
  
  let outcome = 'FAIL';
  if (margin >= 10) outcome = 'CRIT';
  else if (margin >= 5) outcome = 'GREAT';
  else if (margin >= 0) outcome = 'SUCCESS';

  // Cálculo de XP
  const baseXP = CATEGORY_XP_BASE[input.category];
  const diffMult = input.difficulty === 'CHALLENGING' ? 1.25
                 : input.difficulty === 'HARD' ? 1.5
                 : input.difficulty === 'EPIC' ? 2.0 : 1.0;
  const marginBonus = Math.min(100, Math.max(0, 5 * margin));
  const coopBonus = team && team.members.length >= 3 ? 0.10 : 0;
  const xpGained = Math.round((baseXP * diffMult) * (1 + coopBonus) + marginBonus);

  const focusCost = outcome === 'FAIL' ? 3 : 2;
  
  return { 
    score, 
    dc, 
    margin, 
    outcome, 
    xpGained, 
    focusCost, 
    notes: ctx.transient.notes 
  };
}

function awardXpAndLevelUp(digimon, gained) {
  digimon.xp += gained;
  let ups = 0;
  
  while (digimon.level < 50 && digimon.xp >= xpNext(digimon.level)) {
    digimon.xp -= xpNext(digimon.level);
    digimon.level += 1;
    digimon.focus += 2; // Pequeno refresh de Focus ao subir de nível
    ups += 1;
    
    // Atribuir pontos de atributo (níveis ímpares)
    if (digimon.level % 2 === 1) {
      digimon.attributePoints = (digimon.attributePoints || 0) + 1;
    }
    
    // Atribuir pontos de skill (todo nível)
    digimon.skillPoints = (digimon.skillPoints || 0) + 3;
  }
  
  return { 
    levelUps: ups, 
    remainingXpToNext: Math.max(0, xpNext(digimon.level) - digimon.xp) 
  };
}

module.exports = {
  initContext,
  synergyBonus,
  performAction,
  awardXpAndLevelUp
};