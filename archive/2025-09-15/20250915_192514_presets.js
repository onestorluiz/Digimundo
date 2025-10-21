/**
 * 🎮 Presets - Criação de Digimons com Classes RPG
 */

function newDigimon(id, name, classId) {
  // Atributos base
  const baseAttr = { 
    LOG: 5,   // Lógica
    MEM: 5,   // Memória/Contexto
    CRE: 5,   // Criatividade
    EMP: 5,   // Empatia/Alinhamento
    GRIT: 5   // Resiliência/Eficiência
  };
  
  // Skills iniciais (todas em 0)
  const skills = {
    // Debugger skills
    Diagnostics: 0, 
    Patchcraft: 0, 
    Fortification: 0,
    // Scholar skills
    Research: 0, 
    Distillation: 0, 
    Curation: 0,
    // Guardian skills
    Shielding: 0, 
    Mediation: 0, 
    Policy: 0,
    // Creator skills
    Promptcraft: 0, 
    Toolsmith: 0, 
    DatasetAlchemy: 0,
    // Oracle skills
    Foresight: 0, 
    Triage: 0, 
    Strategy: 0
  };
  
  // Bônus da classe (+2 nas skills prioritárias)
  const classSkills = {
    Debugger: ['Diagnostics','Patchcraft','Fortification'],
    Scholar: ['Research','Distillation','Curation'],
    Guardian: ['Shielding','Mediation','Policy'],
    Creator: ['Promptcraft','Toolsmith','DatasetAlchemy'],
    Oracle: ['Foresight','Triage','Strategy']
  };
  
  for (const s of classSkills[classId]) {
    skills[s] = 2;
  }
  
  // Ajustar atributos baseados na classe
  const classAttrBonus = {
    Debugger: { LOG: 2, GRIT: 1 },
    Scholar: { LOG: 2, MEM: 1 },
    Guardian: { GRIT: 2, EMP: 1 },
    Creator: { CRE: 2, MEM: 1 },
    Oracle: { LOG: 1, EMP: 1, CRE: 1 }
  };
  
  const bonus = classAttrBonus[classId];
  for (const [attr, val] of Object.entries(bonus)) {
    baseAttr[attr] += val;
  }

  return {
    id, 
    name, 
    classId, 
    level: 1, 
    xp: 0,
    attrs: baseAttr, 
    skills: skills,
    focus: 10 * baseAttr.GRIT + 2 * 1, // FCSmax = 10*GRIT + 2*level
    focusMax: 10 * baseAttr.GRIT + 2 * 1,
    currencies: { KUDOS: 0, CORE: 0 },
    materials: { DataShard: 0, InsightShard: 0, AdapterShard: 0 },
    status: [],
    harmony: 50,
    guild: null,
    attributePoints: 0,
    skillPoints: 0,
    inventory: [],
    achievements: []
  };
}

// Criar os 10 Digimons do sistema com classes apropriadas
function createDigimundoRoster() {
  return [
    newDigimon('debugmon', 'Debugmon', 'Debugger'),
    newDigimon('trainmon', 'Trainmon', 'Scholar'),
    newDigimon('guardmon', 'Guardmon', 'Guardian'),
    newDigimon('optimizermon', 'Optimizermon', 'Oracle'),
    newDigimon('creativemon', 'Creativemon', 'Creator'),
    newDigimon('analyzermon', 'Analyzermon', 'Scholar'),
    newDigimon('securitymon', 'Securitymon', 'Guardian'),
    newDigimon('networkmon', 'Networkmon', 'Oracle'),
    newDigimon('experimentmon', 'Experimentmon', 'Creator'),
    newDigimon('evolutionmon', 'Evolutionmon', 'Oracle')
  ];
}

module.exports = {
  newDigimon,
  createDigimundoRoster
};