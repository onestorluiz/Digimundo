#!/usr/bin/env python3
"""
🔍 ANALISADOR DE FEATURES NÃO UTILIZADAS
Determina se features marcadas como não usadas deveriam ser conectadas ou removidas
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple

class UnusedFeaturesAnalyzer:
    """
    Analisa features marcadas como não utilizadas
    """

    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.unused_features = []
        self.connection_opportunities = []
        self.removal_candidates = []

    def analyze_all_unused(self) -> Dict:
        """
        Analisa todas as features marcadas como não utilizadas
        """
        print("\n🔍 ANALISANDO FEATURES NÃO UTILIZADAS")
        print("=" * 60)

        # Encontrar todas as features marcadas
        self._find_unused_features()

        # Analisar cada uma
        for feature in self.unused_features:
            self._analyze_feature(feature)

        # Gerar recomendações
        recommendations = self._generate_recommendations()

        return {
            'total_unused': len(self.unused_features),
            'should_connect': len(self.connection_opportunities),
            'should_remove': len(self.removal_candidates),
            'recommendations': recommendations
        }

    def _find_unused_features(self):
        """
        Encontra todas as features marcadas como não utilizadas
        """
        pattern = re.compile(r'# UNUSED - Candidate for removal\n#?\s*def (\w+)')

        for py_file in self.root.glob("**/*.py"):
            if "backup" in str(py_file) or "test" in str(py_file):
                continue

            try:
                content = py_file.read_text()
                matches = pattern.finditer(content)

                for match in matches:
                    func_name = match.group(1) if match.lastindex >= 1 else "unknown"

                    # Extrair mais contexto
                    lines = content.split('\n')
                    line_num = content[:match.start()].count('\n')

                    # Pegar as próximas 10 linhas para entender a função
                    func_lines = lines[line_num:line_num+15]
                    func_content = '\n'.join(func_lines)

                    self.unused_features.append({
                        'file': py_file,
                        'function': func_name,
                        'line': line_num,
                        'content': func_content,
                        'file_name': py_file.name
                    })

            except Exception as e:
                pass

    def _analyze_feature(self, feature: Dict):
        """
        Analisa uma feature específica para determinar se deve ser conectada ou removida
        """
        func_name = feature['function']
        content = feature['content']
        file_name = feature['file_name']

        # Critérios para CONECTAR (não remover):
        connect_indicators = [
            ('knowledge' in func_name.lower(), "Função de conhecimento pode ser útil"),
            ('get_' in func_name, "Getter pode ser necessário para API"),
            ('analyze' in func_name.lower(), "Função de análise pode complementar sistema"),
            ('cache' in func_name.lower(), "Função de cache pode melhorar performance"),
            ('validate' in func_name.lower(), "Validação é sempre útil"),
            ('export' in func_name.lower(), "Export pode ser necessário no futuro"),
            ('import' in func_name.lower(), "Import pode ser necessário no futuro"),
            ('config' in file_name.lower(), "Configurações podem ser necessárias"),
            ('return' in content and 'Dict' in content, "Retorna dados estruturados"),
            ('screenplay' in content.lower(), "Relacionado a roteiros - core do sistema")
        ]

        # Critérios para REMOVER:
        remove_indicators = [
            ('test_' in func_name, "Função de teste antiga"),
            ('debug_' in func_name, "Função de debug"),
            ('_old' in func_name, "Versão antiga"),
            ('_deprecated' in func_name, "Marcado como deprecated"),
            ('pass' in content and content.count('\n') < 5, "Função vazia"),
            ('raise NotImplementedError' in content, "Não implementado"),
            ('TODO' in content, "Nunca foi completado"),
            (file_name == '__init__.py', "Import não usado em __init__"),
            ('START_CLAUDE' in file_name, "Script de inicialização antigo")
        ]

        # Calcular scores
        connect_score = sum(1 for indicator, _ in connect_indicators if indicator)
        remove_score = sum(1 for indicator, _ in remove_indicators if indicator)

        # Decidir
        if connect_score > remove_score:
            reasons = [reason for indicator, reason in connect_indicators if indicator]
            self.connection_opportunities.append({
                'feature': feature,
                'score': connect_score,
                'reasons': reasons
            })
        else:
            reasons = [reason for indicator, reason in remove_indicators if indicator]
            self.removal_candidates.append({
                'feature': feature,
                'score': remove_score,
                'reasons': reasons
            })

    def _generate_recommendations(self) -> List[Dict]:
        """
        Gera recomendações específicas
        """
        recommendations = []

        # Features que deveriam ser CONECTADAS
        for opp in sorted(self.connection_opportunities, key=lambda x: x['score'], reverse=True)[:5]:
            feature = opp['feature']
            recommendations.append({
                'action': 'CONNECT',
                'function': feature['function'],
                'file': str(feature['file'].relative_to(self.root)),
                'reasons': opp['reasons'][:2],
                'suggestion': self._suggest_connection(feature)
            })

        # Features que podem ser REMOVIDAS
        for cand in sorted(self.removal_candidates, key=lambda x: x['score'], reverse=True)[:5]:
            feature = cand['feature']
            recommendations.append({
                'action': 'REMOVE',
                'function': feature['function'],
                'file': str(feature['file'].relative_to(self.root)),
                'reasons': cand['reasons'][:2],
                'suggestion': "Deletar função com segurança"
            })

        return recommendations

    def _suggest_connection(self, feature: Dict) -> str:
        """
        Sugere como conectar a feature
        """
        func_name = feature['function']

        if 'knowledge' in func_name.lower():
            return "Integrar com meta_learning_framework.py"
        elif 'get_' in func_name:
            return "Expor via integrated_system.py como API"
        elif 'analyze' in func_name.lower():
            return "Adicionar ao pipeline de análise paralela"
        elif 'cache' in func_name.lower():
            return "Integrar com intelligent_cache_manager.py"
        elif 'validate' in func_name.lower():
            return "Usar em pipeline de validação"
        else:
            return "Avaliar caso de uso e integrar se necessário"

    def generate_report(self, results: Dict) -> str:
        """
        Gera relatório detalhado
        """
        report = f"""# 🔍 ANÁLISE DE FEATURES NÃO UTILIZADAS

**Total Analisado:** {results['total_unused']} features
**Devem ser CONECTADAS:** {results['should_connect']} features
**Podem ser REMOVIDAS:** {results['should_remove']} features

---

## 🔗 FEATURES QUE DEVERIAM SER CONECTADAS

"""

        for rec in results['recommendations']:
            if rec['action'] == 'CONNECT':
                report += f"""
### `{rec['function']}` em {rec['file']}
**Razões para conectar:**
{chr(10).join(f"- {r}" for r in rec['reasons'])}
**Sugestão:** {rec['suggestion']}
"""

        report += """
---

## 🗑️ FEATURES QUE PODEM SER REMOVIDAS

"""

        for rec in results['recommendations']:
            if rec['action'] == 'REMOVE':
                report += f"""
### `{rec['function']}` em {rec['file']}
**Razões para remover:**
{chr(10).join(f"- {r}" for r in rec['reasons'])}
**Ação:** {rec['suggestion']}
"""

        report += """
---

## 🎯 CONCLUSÃO

"""

        if results['should_connect'] > results['should_remove']:
            report += """
**A MAIORIA das features marcadas como não usadas TEM VALOR e deveria ser CONECTADA ao sistema!**

Isso acontece porque:
1. São funções auxiliares que complementam o sistema
2. São getters/setters que formam APIs completas
3. São validações que aumentam robustez
4. São funções de análise que podem enriquecer resultados

**RECOMENDAÇÃO:** Revisar e conectar as features valiosas antes de remover.
"""
        else:
            report += """
**A MAIORIA das features pode ser REMOVIDA com segurança.**

São principalmente:
1. Código de teste/debug antigo
2. Funções vazias ou não implementadas
3. Imports não usados em __init__.py
4. Scripts de inicialização obsoletos
"""

        report += "\n---\n**DIGIMUNDO PRESENTE** 🥷"

        return report


def main():
    """
    Executa análise de features não utilizadas
    """
    analyzer = UnusedFeaturesAnalyzer()

    # Analisar
    results = analyzer.analyze_all_unused()

    # Gerar relatório
    report = analyzer.generate_report(results)

    # Salvar
    report_path = Path("docs/UNUSED_FEATURES_ANALYSIS.md")
    report_path.write_text(report)

    print(f"\n📊 RESULTADO DA ANÁLISE:")
    print(f"  Total marcadas: {results['total_unused']}")
    print(f"  ✅ Deveriam ser CONECTADAS: {results['should_connect']}")
    print(f"  ❌ Podem ser REMOVIDAS: {results['should_remove']}")

    print(f"\n💡 RECOMENDAÇÕES:")
    for rec in results['recommendations'][:3]:
        emoji = "🔗" if rec['action'] == 'CONNECT' else "🗑️"
        print(f"  {emoji} {rec['function']}: {rec['action']}")
        print(f"     → {rec['suggestion']}")

    print(f"\n📄 Relatório completo: {report_path}")

    return results


if __name__ == "__main__":
    main()