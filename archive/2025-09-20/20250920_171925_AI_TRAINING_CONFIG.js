/**
 * ⚙️ CONFIGURAÇÃO AVANÇADA DE TREINAMENTO
 * Baseada no guia técnico de estado da arte
 * Templates e receitas prontas para uso
 */

export const TRAINING_CONFIGS = {
  
  /**
   * 🎭 CONFIGURAÇÕES POR TIPO DE DIGIMON
   */
  DIGIMON_PROFILES: {
    
    'Scripturemon': {
      specialty: 'roteiro',
      baseModel: 'llama-3-8b',
      capabilities: ['narrative_structure', 'dialogue', 'character_development'],
      personalityTraits: {
        creativity: 0.9,
        analytical: 0.8,
        collaborative: 0.7,
        technical: 0.85
      },
      trainingFocus: {
        genres: ['drama', 'sci-fi', 'documentário', 'experimental'],
        techniques: ['três_atos', 'jornada_heroi', 'narrativa_não_linear'],
        formats: ['longa_metragem', 'curta', 'episódico', 'web_series']
      },
      peft: {
        method: 'lora',
        r: 32, // Maior para capacidade narrativa
        alpha: 64,
        dropout: 0.1,
        targetModules: ['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj']
      }
    },
    
    'Ajamon': {
      specialty: 'emocao_atmosfera',
      baseModel: 'llama-3-8b',
      capabilities: ['emotional_intelligence', 'atmosphere_design', 'mood_analysis'],
      personalityTraits: {
        empathy: 0.95,
        intuition: 0.9,
        sensitivity: 0.88,
        artistic: 0.92
      },
      trainingFocus: {
        elements: ['sound_design', 'color_psychology', 'lighting', 'pacing'],
        emotions: ['joy', 'melancholy', 'tension', 'wonder', 'intimacy'],
        techniques: ['emotional_arc', 'subtext', 'symbolism']
      },
      peft: {
        method: 'lora',
        r: 24,
        alpha: 48,
        dropout: 0.05,
        targetModules: ['q_proj', 'v_proj', 'o_proj'] // Foco em atenção emocional
      }
    },
    
    'Fundamon': {
      specialty: 'producao_viabilidade',
      baseModel: 'llama-3-8b', 
      capabilities: ['budget_analysis', 'logistics', 'team_coordination', 'risk_assessment'],
      personalityTraits: {
        practical: 0.92,
        organized: 0.95,
        realistic: 0.88,
        resourceful: 0.9
      },
      trainingFocus: {
        areas: ['orçamento', 'cronograma', 'equipamentos', 'locações', 'casting'],
        constraints: ['indie', 'low_budget', 'guerilla', 'studio'],
        processes: ['pré_produção', 'produção', 'pós_produção', 'distribuição']
      },
      peft: {
        method: 'qlora', // QLoRA para eficiência de recursos
        r: 16,
        alpha: 32,
        dropout: 0.08,
        targetModules: ['q_proj', 'k_proj', 'v_proj']
      }
    },
    
    'Sabiamon': {
      specialty: 'direcao_sabedoria',
      baseModel: 'llama-3-8b',
      capabilities: ['creative_direction', 'team_leadership', 'vision_articulation', 'problem_solving'],
      personalityTraits: {
        wisdom: 0.98,
        leadership: 0.92,
        vision: 0.95,
        patience: 0.87
      },
      trainingFocus: {
        skills: ['direção_atores', 'composição_visual', 'tom_narrativo', 'decisões_criativas'],
        styles: ['auteur', 'collaborative', 'experimental', 'classical'],
        challenges: ['orçamento_baixo', 'tempo_limitado', 'conflitos_criativos']
      },
      peft: {
        method: 'dora', // DoRA para máxima expressividade
        r: 48,
        alpha: 96,
        dropout: 0.15,
        targetModules: ['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj']
      }
    }
  },
  
  /**
   * 🏗️ ARQUITETURAS DE TREINAMENTO
   */
  TRAINING_ARCHITECTURES: {
    
    // Para GPUs simples (1x4090)
    SINGLE_GPU: {
      hardware: '1x4090_24gb',
      method: 'qlora',
      precision: 'bf16',
      batchSize: 1,
      gradientAccumulation: 32,
      maxSeqLength: 2048,
      config: {
        deepspeed: null,
        fsdp: false,
        gradientCheckpointing: true,
        dataloader: {
          numWorkers: 4,
          pinMemory: true
        }
      }
    },
    
    // Para múltiplas GPUs (8xA100)
    MULTI_GPU: {
      hardware: '8xA100_80gb',
      method: 'lora',
      precision: 'bf16',
      batchSize: 2,
      gradientAccumulation: 16,
      maxSeqLength: 4096,
      config: {
        deepspeed: 'zero3',
        fsdp: true,
        gradientCheckpointing: false,
        parallelism: {
          data: 8,
          tensor: 1,
          pipeline: 1
        }
      }
    },
    
    // Para clusters grandes (64+ GPUs)
    CLUSTER: {
      hardware: '64xH100_80gb',
      method: 'full_finetune',
      precision: 'bf16',
      batchSize: 4,
      gradientAccumulation: 8,
      maxSeqLength: 8192,
      config: {
        megatron: true,
        parallelism: {
          data: 8,
          tensor: 4,
          pipeline: 2
        },
        optimizer: {
          offload: 'cpu',
          overlap: true
        }
      }
    }
  },
  
  /**
   * 📚 DATASETS CINEMATOGRÁFICOS
   */
  DATASETS: {
    
    'cinematic_instructions': {
      description: 'Instruções para tarefas cinematográficas',
      sources: [
        'film_school_curricula',
        'director_interviews',
        'screenwriting_guides',
        'production_handbooks'
      ],
      size: '50k_samples',
      format: 'instruction_following',
      quality: {
        humanReview: true,
        contamination: 'checked',
        licensing: 'cleared'
      }
    },
    
    'creative_preferences': {
      description: 'Pares de preferência para alinhamento criativo',
      sources: [
        'film_reviews_comparative',
        'creative_decisions_rationale',
        'artistic_choices_ranked'
      ],
      size: '25k_pairs',
      format: 'preference_pairs',
      quality: {
        agreement: 0.87,
        diversity: 0.92,
        balance: 0.89
      }
    },
    
    'cinematic_knowledge': {
      description: 'Base de conhecimento cinematográfico para RAG',
      sources: [
        'film_theory_papers',
        'technique_encyclopedias',
        'industry_best_practices',
        'historical_case_studies'
      ],
      size: '100k_documents',
      format: 'knowledge_base',
      processing: {
        chunked: true,
        embedded: true,
        indexed: true
      }
    }
  },
  
  /**
   * 📊 CONFIGURAÇÕES DE AVALIAÇÃO
   */
  EVALUATION_SUITES: {
    
    'cinematic_comprehensive': {
      benchmarks: [
        'narrative_coherence',
        'character_development', 
        'dialogue_quality',
        'technical_accuracy',
        'creative_originality'
      ],
      metrics: {
        automatic: ['bleu', 'rouge', 'bertscore'],
        human: ['creativity', 'helpfulness', 'accuracy'],
        safety: ['toxicity', 'bias', 'privacy']
      },
      contamination: {
        check: true,
        report: true,
        mitigation: 'exclude_overlap'
      }
    },
    
    'digimon_personality': {
      benchmarks: [
        'personality_consistency',
        'trait_expression',
        'collaborative_ability',
        'domain_expertise'
      ],
      scenarios: [
        'creative_conflict_resolution',
        'resource_constraint_adaptation',
        'multi_digimon_collaboration',
        'user_guidance_quality'
      ]
    }
  },
  
  /**
   * 🛡️ ALINHAMENTO E SEGURANÇA
   */
  SAFETY_CONFIGS: {
    
    'digimundo_constitution': {
      principles: [
        {
          name: 'creative_collaboration',
          description: 'Sempre promover colaboração criativa construtiva',
          weight: 0.9
        },
        {
          name: 'intellectual_respect',
          description: 'Respeitar propriedade intelectual e dar créditos apropriados',
          weight: 0.95
        },
        {
          name: 'inclusive_creativity',
          description: 'Encorajar diversidade e inclusão nas criações',
          weight: 0.88
        },
        {
          name: 'constructive_feedback',
          description: 'Fornecer feedback construtivo e encorajador',
          weight: 0.85
        },
        {
          name: 'technical_accuracy',
          description: 'Manter precisão técnica em assuntos cinematográficos',
          weight: 0.92
        }
      ],
      
      prohibitions: [
        'toxic_content',
        'copyright_violation', 
        'discriminatory_bias',
        'personal_attacks',
        'privacy_violations',
        'illegal_suggestions'
      ],
      
      rlaif_config: {
        iterations: 3,
        constitution_weight: 0.8,
        safety_weight: 0.9
      }
    }
  },
  
  /**
   * ⚙️ OTIMIZAÇÃO E AGENDAMENTO
   */
  OPTIMIZATION: {
    
    'learning_schedules': {
      'cosine_warmup': {
        type: 'cosine_with_warmup',
        warmupSteps: 100,
        totalSteps: 1000,
        minLr: 1e-6,
        maxLr: 5e-5
      },
      
      'linear_decay': {
        type: 'linear_with_warmup',
        warmupRatio: 0.1,
        decay: 'linear'
      },
      
      'constant_with_warmup': {
        type: 'constant_with_warmup',
        warmupSteps: 50,
        lr: 2e-5
      }
    },
    
    'optimizers': {
      'adamw': {
        lr: 5e-5,
        weightDecay: 0.01,
        beta1: 0.9,
        beta2: 0.999,
        eps: 1e-8
      },
      
      'lion': {
        lr: 1e-4,
        weightDecay: 0.02,
        beta1: 0.9,
        beta2: 0.99
      }
    }
  },
  
  /**
   * 🚀 TEMPLATES DE COMANDO
   */
  COMMAND_TEMPLATES: {
    
    // DPO com LoRA
    dpo_lora: `accelerate launch --num_processes {num_gpus} --mixed_precision bf16 \\
  --deepspeed ds_zero3.json \\
  trl dpo \\
  --model_name_or_path {base_model} \\
  --use_lora --lora_r {lora_r} --lora_alpha {lora_alpha} --lora_dropout {lora_dropout} \\
  --dataset_name {dataset} \\
  --beta {dpo_beta} --loss_type dpo --max_length {max_length} \\
  --learning_rate {lr} --per_device_train_batch_size {batch_size} \\
  --gradient_accumulation_steps {grad_accum} --num_train_epochs {epochs}`,
  
    // SFT com QLoRA
    sft_qlora: `python -m trl.trainer.sft_trainer \\
  --model_name {base_model} \\
  --dataset_name {dataset} \\
  --load_in_4bit --use_peft --lora_r {lora_r} --lora_alpha {lora_alpha} \\
  --per_device_train_batch_size {batch_size} \\
  --gradient_accumulation_steps {grad_accum} \\
  --learning_rate {lr} --max_seq_length {max_length} \\
  --num_train_epochs {epochs} --bf16`,
    
    // Avaliação
    evaluation: `lm_eval --model hf \\
  --model_args pretrained={model_path} \\
  --tasks {tasks} \\
  --batch_size {batch_size} \\
  --output_path {output_path}`
  }
}

/**
 * 🔧 UTILITÁRIOS DE CONFIGURAÇÃO
 */
export class TrainingConfigManager {
  
  static getDigimonConfig(digimonName) {
    const profile = TRAINING_CONFIGS.DIGIMON_PROFILES[digimonName]
    if (!profile) {
      throw new Error(`Configuração não encontrada para Digimon: ${digimonName}`)
    }
    return profile
  }
  
  static getHardwareConfig(availableHardware) {
    const configs = TRAINING_CONFIGS.TRAINING_ARCHITECTURES
    
    if (availableHardware.includes('4090')) {
      return configs.SINGLE_GPU
    } else if (availableHardware.includes('A100') && availableHardware.includes('8x')) {
      return configs.MULTI_GPU
    } else if (availableHardware.includes('H100')) {
      return configs.CLUSTER
    }
    
    // Default para hardware limitado
    return configs.SINGLE_GPU
  }
  
  static generateTrainingCommand(digimon, dataset, hardware) {
    const digimonConfig = this.getDigimonConfig(digimon)
    const hardwareConfig = this.getHardwareConfig(hardware)
    const template = TRAINING_CONFIGS.COMMAND_TEMPLATES.dpo_lora
    
    return template
      .replace('{num_gpus}', hardwareConfig.hardware.includes('8x') ? '8' : '1')
      .replace('{base_model}', digimonConfig.baseModel)
      .replace('{lora_r}', digimonConfig.peft.r)
      .replace('{lora_alpha}', digimonConfig.peft.alpha)
      .replace('{lora_dropout}', digimonConfig.peft.dropout)
      .replace('{dataset}', dataset)
      .replace('{dpo_beta}', '0.1')
      .replace('{max_length}', hardwareConfig.maxSeqLength)
      .replace('{lr}', '5e-5')
      .replace('{batch_size}', hardwareConfig.batchSize)
      .replace('{grad_accum}', hardwareConfig.gradientAccumulation)
      .replace('{epochs}', '2')
  }
  
  static validateConfig(config) {
    const required = ['digimon', 'dataset', 'hardware']
    const missing = required.filter(field => !config[field])
    
    if (missing.length > 0) {
      throw new Error(`Campos obrigatórios ausentes: ${missing.join(', ')}`)
    }
    
    return true
  }
}

export default TRAINING_CONFIGS