#!/usr/bin/env python3
"""
Teste do sistema de scoring com exemplos variados.
Demonstra pontuação variável e breakdown detalhado.
"""

import sys
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validator.scoring import ScriptScorer, score


def create_sample_analyses():
    """Cria análises de exemplo para teste."""
    
    # Exemplo 1: Roteiro Excelente
    excellent = {
        "estrutura": {
            "response": """
            Estrutura narrativa magistral com três atos perfeitamente equilibrados.
            Os pontos de virada são surpreendentes mas orgânicos, emergindo naturalmente
            da progressão dramática. O arco do protagonista demonstra transformação profunda
            e crível. Clímax posicionado com precisão cirúrgica no terceiro ato.
            Resolução satisfatória que honra a jornada sem ser previsível.
            Setup e payoff brilhantes, com elementos plantados sutilmente no primeiro ato
            que florescem no clímax. Conflito central claro e stakes bem estabelecidas.
            """
        },
        "emoção": {
            "response": """
            Conexão empática excepcional com os personagens, criando investimento emocional
            genuíno do público. Curva emocional envolvente com picos e vales bem calibrados.
            Momentos de impacto emocional que ressoam profundamente. Autenticidade nas emoções
            retratadas, sem manipulação barata. Catarse poderosa e merecida no clímax.
            Variedade emocional rica, explorando todo o espectro humano.
            """
        },
        "técnica": {
            "response": """
            Diálogos naturais e significativos que revelam caráter e avançam a trama.
            Descrições visuais evocativas e econômicas. Formatação impecável seguindo
            padrões profissionais. Show don't tell aplicado com maestria.
            Voz única e distintiva do autor. Transições fluidas entre cenas.
            Abertura cativante que estabelece tom e promessa. Fechamento memorável.
            """
        },
        "tema": {
            "response": """
            Exploração temática profunda e original sobre a condição humana.
            Relevância contemporânea sem ser panfletário. Subtexto rico em camadas
            de significado. Metáforas visuais poderosas que amplificam o tema.
            Mensagem clara mas não didática, permitindo interpretação.
            Capacidade excepcional de provocar reflexão duradoura.
            """
        }
    }
    
    # Exemplo 2: Roteiro Mediano
    average = {
        "estrutura": {
            "response": """
            Estrutura competente seguindo padrões convencionais de três atos.
            Pontos de virada presentes mas previsíveis. Arco do protagonista existe
            mas falta profundidade. Clímax adequado mas sem grande impacto.
            Resolução funcional mas comum. Ritmo irregular em alguns momentos.
            Conflito básico estabelecido mas stakes poderiam ser mais claras.
            """
        },
        "emoção": {
            "response": """
            Conexão empática regular com personagens. Alguns momentos emocionais
            funcionam mas falta consistência. Curva emocional presente mas mecânica.
            Emoções por vezes artificiais. Catarse presente mas poderia ser mais impactante.
            Variedade emocional limitada, ficando em território seguro.
            """
        },
        "técnica": {
            "response": """
            Diálogos funcionais mas sem brilho particular. Algumas linhas soam
            expositivas e forçadas. Descrições adequadas mas genéricas.
            Formatação correta. Tendência a tell em vez de show em momentos cruciais.
            Voz do autor não distintiva. Transições básicas.
            """
        },
        "tema": {
            "response": """
            Tema presente mas tratamento superficial. Abordagem comum de questões
            já muito exploradas. Pouca originalidade na perspectiva.
            Subtexto raso. Mensagem óbvia e por vezes didática.
            Limitada capacidade de provocar reflexão além do momento.
            """
        }
    }
    
    # Exemplo 3: Roteiro Fraco
    weak = {
        "estrutura": {
            "response": """
            Estrutura confusa e desestruturada. Atos desbalanceados com segundo ato
            arrastado. Pontos de virada fracos ou ausentes. Arco do protagonista
            inconsistente ou inexistente. Personagem permanece estático.
            Clímax anticlimático e mal posicionado. Resolução abrupta com deus ex machina.
            Falta de setup adequado. Conflito mal definido e stakes pouco claras.
            """
        },
        "emoção": {
            "response": """
            Conexão emocional fraca com personagens distantes e artificiais.
            Curva emocional plana sem variação significativa. Momentos que deveriam
            impactar caem vazios. Emoções forçadas e não críveis.
            Ausência de catarse. Tentativas de humor caem flat.
            Tom emocional monotônico e desengajante.
            """
        },
        "técnica": {
            "response": """
            Diálogos artificiais, expositivos e clichê. Personagens falam todos
            da mesma forma. Descrições excessivas ou inadequadas.
            Formatação com erros. Excesso de tell, pouco show.
            Economia narrativa pobre com cenas desnecessárias.
            Transições abruptas e confusas.
            """
        },
        "tema": {
            "response": """
            Tema ausente ou extremamente raso. Tratamento simplista de questões complexas.
            Clichês abundantes sem nova perspectiva. Falta de subtexto.
            Mensagem confusa ou contraditória. Didatismo excessivo.
            Incapacidade de engajar intelectualmente.
            """
        }
    }
    
    return {
        "excellent": excellent,
        "average": average,
        "weak": weak
    }


def test_scoring_system():
    """Testa o sistema de scoring com diferentes exemplos."""
    
    print("=" * 70)
    print("🎯 TESTE DO SISTEMA DE SCORING")
    print("=" * 70)
    
    # Criar scorer
    scorer = ScriptScorer()
    
    # Obter análises de exemplo
    samples = create_sample_analyses()
    
    # Testar cada exemplo
    for name, analysis in samples.items():
        print(f"\n{'='*70}")
        print(f"📝 Testando: {name.upper()}")
        print("="*70)
        
        # Calcular score
        result = scorer.score(analysis)
        
        # Exibir resultados
        print(f"\n🎯 PONTUAÇÃO TOTAL: {result['total']}/100")
        print(f"📊 GRADE: {result['grade']}")
        
        print("\n📈 BREAKDOWN POR CATEGORIA:")
        print("-" * 40)
        for category, score in result['breakdown'].items():
            weight = result['weights'][category]
            weighted = score * weight
            print(f"  {category.capitalize():12} {score:5.1f}/100 (peso {weight:.2f}) = {weighted:5.1f} pontos")
        
        print("\n🔍 DETALHES DA AVALIAÇÃO:")
        for category, details in result['details'].items():
            if isinstance(details, dict) and 'percentage' in details:
                print(f"\n  {category.capitalize()}:")
                print(f"    Pontos: {details.get('total_earned', 0)}/{details.get('total_possible', 0)}")
                print(f"    Percentual: {details['percentage']}%")
    
    # Teste de variação
    print("\n" + "="*70)
    print("🔄 TESTE DE VARIAÇÃO DE SCORES")
    print("="*70)
    
    # Criar múltiplas análises com qualidades diferentes
    test_cases = [
        ("Apenas estrutura boa", {"estrutura": samples["excellent"]["estrutura"]}),
        ("Apenas técnica fraca", {"técnica": samples["weak"]["técnica"]}),
        ("Mix alto-baixo", {
            "estrutura": samples["excellent"]["estrutura"],
            "emoção": samples["weak"]["emoção"],
            "técnica": samples["average"]["técnica"],
            "tema": samples["excellent"]["tema"]
        }),
        ("Todas médias", samples["average"]),
        ("Vazio (sem análise)", {})
    ]
    
    print("\n📊 Resultados de Variação:")
    print("-" * 40)
    for desc, analysis in test_cases:
        result = scorer.score(analysis)
        print(f"  {desc:25} → {result['total']:5.1f}/100 - {result['grade']}")
    
    # Teste com configurações customizadas
    print("\n" + "="*70)
    print("⚙️ TESTE COM PESOS CUSTOMIZADOS")
    print("="*70)
    
    custom_settings = {
        "scoring": {
            "weights": {
                "estrutura": 0.40,  # Mais peso para estrutura
                "emoção": 0.30,     # Mais peso para emoção
                "técnica": 0.15,    # Menos peso para técnica
                "tema": 0.15        # Menos peso para tema
            }
        }
    }
    
    custom_scorer = ScriptScorer(custom_settings)
    
    print("\n🔧 Pesos Customizados:")
    for cat, weight in custom_scorer.weights.items():
        print(f"  {cat}: {weight:.2f}")
    
    # Comparar scores com pesos diferentes
    print("\n📊 Comparação Default vs Custom:")
    print("-" * 40)
    
    for name, analysis in samples.items():
        default_result = scorer.score(analysis)
        custom_result = custom_scorer.score(analysis)
        diff = custom_result['total'] - default_result['total']
        sign = "+" if diff > 0 else ""
        
        print(f"  {name:10} Default: {default_result['total']:5.1f} | Custom: {custom_result['total']:5.1f} ({sign}{diff:.1f})")
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 70)


def main():
    """Função principal."""
    test_scoring_system()
    return 0


if __name__ == "__main__":
    sys.exit(main())