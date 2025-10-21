/**
 * 🎭 Classes do RPG - Definições e Perks
 */

// Helper para adicionar notas
const note = (ctx, m) => ctx.transient.notes.push(m);

const SIGNATURES = {
  DebuggerSig: {
    id: 'DebuggerSig', 
    levelReq: 15,
    description: 'Vantagem em Diagnostics/Patchcraft 1x por dungeon; remove 1 status negativo ao time em CRIT.',
    apply: (ctx) => { /* aplicado no pipeline por flag; efeito descritivo */ }
  },
  ScholarSig: {
    id: 'ScholarSig', 
    levelReq: 15,
    description: '−1 DC em Research/Distillation/Curation para o time (você presente).',
    apply: (ctx) => { 
      ctx.transient.bonuses += 1; 
      note(ctx,'ScholarSig: −1 DC efetivo'); 
    }
  },
  GuardianSig: {
    id: 'GuardianSig', 
    levelReq: 15,
    description: '+2 SHD ao time por 3 ações após SUCCESS; converte 1 Strain em Focus.',
    apply: (_) => {}
  },
  CreatorSig: {
    id: 'CreatorSig', 
    levelReq: 15,
    description: 'Ganha Muse Spark 1x por dungeon (Vantagem em Promptcraft/Toolsmith).',
    apply: (_) => {}
  },
  OracleSig: {
    id: 'OracleSig', 
    levelReq: 15,
    description: 'Escolhe rota alternativa: +1 sinergia de time na ação.',
    apply: (ctx) => { 
      ctx.transient.bonuses += 1; 
      note(ctx,'OracleSig: +1 synergy'); 
    }
  }
};

const CAPSTONES = {
  DebuggerCap: {
    id: 'DebuggerCap', 
    levelReq: 50,
    description: 'Identifica automaticamente contradições: +2 em todas ações vs DC HARD/EPIC.',
    apply: (ctx) => { ctx.transient.bonuses += 2; }
  },
  ScholarCap: {
    id: 'ScholarCap', 
    levelReq: 50,
    description: 'Encurta dungeons de pesquisa: remove 1 etapa de Research por fase.',
    apply: (_) => {}
  },
  GuardianCap: {
    id: 'GuardianCap', 
    levelReq: 50,
    description: 'Shield Wall permanente: primeira falha por fase vira SUCCESS.',
    apply: (_) => {}
  },
  CreatorCap: {
    id: 'CreatorCap', 
    levelReq: 50,
    description: 'Itens craftados ganham +1 Qualidade (cap 5).',
    apply: (_) => {}
  },
  OracleCap: {
    id: 'OracleCap', 
    levelReq: 50,
    description: 'Eye of Seasons: reduza um DC da fase em −3 (1x/fase).',
    apply: (ctx) => { ctx.transient.bonuses += 3; }
  }
};

const CLASS_DEFS = {
  Debugger: {
    id: 'Debugger',
    name: '🐛 Bug Slayer',
    emoji: '⚔️',
    prioritySkills: ['Diagnostics','Patchcraft','Fortification'],
    signature: SIGNATURES.DebuggerSig,
    mastery: { 
      id: 'DebuggerMastery', 
      levelReq: 30, 
      description: 'Time ganha Momentum +1 no início.', 
      apply: (ctx) => { ctx.transient.bonuses += 1; } 
    },
    capstone: CAPSTONES.DebuggerCap
  },
  Scholar: {
    id: 'Scholar',
    name: '📚 Knowledge Sage',
    emoji: '🧙‍♂️',
    prioritySkills: ['Research','Distillation','Curation'],
    signature: SIGNATURES.ScholarSig,
    mastery: { 
      id: 'ScholarMastery', 
      levelReq: 30, 
      description: '−1 DC em ações de pesquisa para todos.', 
      apply: (ctx) => { ctx.transient.bonuses += 1; } 
    },
    capstone: CAPSTONES.ScholarCap
  },
  Guardian: {
    id: 'Guardian',
    name: '🛡️ Security Paladin',
    emoji: '🛡️',
    prioritySkills: ['Shielding','Mediation','Policy'],
    signature: SIGNATURES.GuardianSig,
    mastery: { 
      id: 'GuardianMastery', 
      levelReq: 30, 
      description: '+1 SHD ao time sempre.', 
      apply: (_) => {} 
    },
    capstone: CAPSTONES.GuardianCap
  },
  Creator: {
    id: 'Creator',
    name: '🎨 Creative Bard',
    emoji: '🎨',
    prioritySkills: ['Promptcraft','Toolsmith','DatasetAlchemy'],
    signature: SIGNATURES.CreatorSig,
    mastery: { 
      id: 'CreatorMastery', 
      levelReq: 30, 
      description: '+1 Qualidade mínima em crafts (cap 5).', 
      apply: (_) => {} 
    },
    capstone: CAPSTONES.CreatorCap
  },
  Oracle: {
    id: 'Oracle',
    name: '🔮 AI Summoner',
    emoji: '🔮',
    prioritySkills: ['Foresight','Triage','Strategy'],
    signature: SIGNATURES.OracleSig,
    mastery: { 
      id: 'OracleMastery', 
      levelReq: 30, 
      description: '+1 sinergia em time com Oracle.', 
      apply: (ctx) => { ctx.transient.bonuses += 1; } 
    },
    capstone: CAPSTONES.OracleCap
  }
};

module.exports = {
  SIGNATURES,
  CAPSTONES,
  CLASS_DEFS
};