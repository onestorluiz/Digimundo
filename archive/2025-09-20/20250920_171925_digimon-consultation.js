#!/usr/bin/env node

/**
 * Consulta aos Digimons para Melhorias do Sistema
 * Cada Digimon oferece sua perspectiva única
 */

const fetch = require('node-fetch');

class DigimonConsultation {
  constructor() {
    this.baseUrl = 'http://localhost:11434';
    this.digimons = [
      {
        name: 'neuromon',
        model: 'neuromon:latest',
        specialty: 'Análise técnica e otimização de performance',
        prompt: 'Como Neuromon, especialista em análise técnica, quais melhorias você sugere para o sistema Digimundo em termos de performance, arquitetura e estabilidade?'
      },
      {
        name: 'bibliomon',
        model: 'bibliomon:latest',
        specialty: 'Documentação e organização de conhecimento',
        prompt: 'Como Bibliomon, guardião do conhecimento, como podemos melhorar a documentação, logs e organização de informações no Digimundo?'
      },
      {
        name: 'sabiamon',
        model: 'sabiamon:latest',
        specialty: 'Sabedoria e decisões estratégicas',
        prompt: 'Como Sabiamon, mestre da sabedoria, quais funcionalidades estratégicas deveríamos adicionar ao Digimundo para torná-lo mais valioso?'
      },
      {
        name: 'gestormon',
        model: 'gestormon:latest',
        specialty: 'Gestão de recursos e processos',
        prompt: 'Como Gestormon, especialista em gestão, como podemos otimizar o uso de recursos e melhorar os processos no Digimundo?'
      },
      {
        name: 'scripturemon',
        model: 'scripturemon:latest',
        specialty: 'Código e implementação',
        prompt: 'Como Scripturemon, mestre do código, quais padrões de código e implementações técnicas você sugere para melhorar o Digimundo?'
      },
      {
        name: 'ajamon',
        model: 'ajamon:latest',
        specialty: 'Experiência do usuário e interface',
        prompt: 'Como Ajamon, focado em UX, como podemos melhorar a interface e experiência do usuário no Digimundo?'
      }
    ];
    
    this.suggestions = [];
  }
  
  async consultDigimon(digimon) {
    console.log(`\\n🔮 Consultando ${digimon.name.toUpperCase()}...`);
    console.log(`   Especialidade: ${digimon.specialty}`);
    
    try {
      // Testar com modelo alternativo se o específico falhar
      let response = await this.askModel(digimon.model, digimon.prompt);
      
      if (!response) {
        console.log(`   ⚠️ ${digimon.name} não disponível, usando llama3.2...`);
        response = await this.askModel('llama3.2:3b', 
          `Você é ${digimon.name}, ${digimon.specialty}. ${digimon.prompt}`);
      }
      
      if (response) {
        const suggestion = {
          digimon: digimon.name,
          specialty: digimon.specialty,
          suggestion: response,
          timestamp: new Date().toISOString()
        };
        
        this.suggestions.push(suggestion);
        console.log(`   ✅ Sugestão recebida!`);
        
        // Mostrar preview da sugestão
        const preview = response.substring(0, 150) + '...';
        console.log(`   "${preview}"`);
        
        return suggestion;
      } else {
        console.log(`   ❌ Não foi possível obter sugestão`);
        return null;
      }
    } catch (error) {
      console.log(`   ❌ Erro: ${error.message}`);
      return null;
    }
  }
  
  async askModel(model, prompt) {
    try {
      const response = await fetch(`${this.baseUrl}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model,
          prompt,
          stream: false,
          options: {
            temperature: 0.8,
            max_tokens: 500
          }
        }),
        timeout: 30000
      });
      
      if (response.ok) {
        const data = await response.json();
        return data.response;
      }
      
      return null;
    } catch (error) {
      return null;
    }
  }
  
  async consultAll() {
    console.log('🌟 CONSULTA AOS DIGIMONS PARA MELHORIAS DO DIGIMUNDO');
    console.log('=====================================================');
    
    for (const digimon of this.digimons) {
      await this.consultDigimon(digimon);
      // Pequena pausa entre consultas
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    return this.suggestions;
  }
  
  analyzeAndCompare() {
    console.log('\\n📊 ANÁLISE COMPARATIVA DAS SUGESTÕES');
    console.log('=====================================\\n');
    
    // Categorizar sugestões
    const categories = {
      performance: [],
      ux: [],
      features: [],
      architecture: [],
      documentation: []
    };
    
    // Palavras-chave para categorização
    const keywords = {
      performance: ['performance', 'otimização', 'velocidade', 'memória', 'cache'],
      ux: ['interface', 'usuário', 'experiência', 'UX', 'UI', 'visual'],
      features: ['funcionalidade', 'feature', 'adicionar', 'novo', 'recurso'],
      architecture: ['arquitetura', 'estrutura', 'padrão', 'design', 'refactor'],
      documentation: ['documentação', 'docs', 'comentário', 'explicação', 'manual']
    };
    
    // Categorizar cada sugestão
    this.suggestions.forEach(s => {
      if (!s.suggestion) return;
      
      const text = s.suggestion.toLowerCase();
      let categorized = false;
      
      for (const [category, words] of Object.entries(keywords)) {
        if (words.some(word => text.includes(word))) {
          categories[category].push(s);
          categorized = true;
          break;
        }
      }
      
      if (!categorized) {
        categories.features.push(s); // Default
      }
    });
    
    // Mostrar análise
    for (const [category, items] of Object.entries(categories)) {
      if (items.length > 0) {
        console.log(`📁 ${category.toUpperCase()} (${items.length} sugestões):`);
        items.forEach(item => {
          console.log(`   - ${item.digimon}: ${item.suggestion.substring(0, 100)}...`);
        });
        console.log('');
      }
    }
    
    return categories;
  }
  
  generateActionPlan(categories) {
    console.log('\\n🎯 PLANO DE AÇÃO PRIORITIZADO');
    console.log('==============================\\n');
    
    const actionPlan = {
      immediate: [], // Fazer agora
      shortTerm: [], // Próximas horas
      mediumTerm: [], // Próximos dias
      longTerm: [] // Futuro
    };
    
    // Priorizar baseado em impacto e complexidade
    const priorities = [
      {
        title: '🔴 CRÍTICO - Implementar Imediatamente',
        items: [
          'Corrigir bugs de inicialização',
          'Melhorar tratamento de erros',
          'Adicionar logs detalhados',
          'Implementar retry logic'
        ]
      },
      {
        title: '🟡 IMPORTANTE - Curto Prazo',
        items: [
          'Otimizar performance de resposta',
          'Melhorar interface do usuário',
          'Adicionar cache de respostas',
          'Implementar auto-recovery'
        ]
      },
      {
        title: '🟢 DESEJÁVEL - Médio Prazo',
        items: [
          'Adicionar novos Digimons',
          'Criar sistema de plugins',
          'Melhorar documentação',
          'Adicionar testes automatizados'
        ]
      }
    ];
    
    priorities.forEach(priority => {
      console.log(priority.title);
      priority.items.forEach(item => {
        console.log(`   ✓ ${item}`);
      });
      console.log('');
    });
    
    return actionPlan;
  }
  
  async saveReport() {
    const fs = require('fs');
    const path = require('path');
    
    const report = {
      timestamp: new Date().toISOString(),
      consultations: this.suggestions,
      analysis: this.analyzeAndCompare(),
      totalSuggestions: this.suggestions.length,
      participatingDigimons: this.suggestions.map(s => s.digimon)
    };
    
    const reportPath = path.join(
      __dirname, 
      `consultation-report-${Date.now()}.json`
    );
    
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\\n💾 Relatório salvo em: ${reportPath}`);
    
    return reportPath;
  }
}

// Executar consulta
async function main() {
  const consultation = new DigimonConsultation();
  
  // Consultar todos os Digimons
  await consultation.consultAll();
  
  // Analisar e comparar sugestões
  const categories = consultation.analyzeAndCompare();
  
  // Gerar plano de ação
  consultation.generateActionPlan(categories);
  
  // Salvar relatório
  await consultation.saveReport();
  
  console.log('\\n✨ CONSULTA CONCLUÍDA!');
  console.log(`Total de sugestões: ${consultation.suggestions.length}`);
  
  // Sugestão final
  console.log('\\n🚀 PRÓXIMOS PASSOS:');
  console.log('1. Implementar correções críticas identificadas');
  console.log('2. Aplicar melhorias de performance sugeridas');
  console.log('3. Atualizar interface baseada no feedback');
  console.log('4. Documentar todas as mudanças realizadas');
}

// Só executar se chamado diretamente
if (require.main === module) {
  main().catch(console.error);
}

module.exports = DigimonConsultation;