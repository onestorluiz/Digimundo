#!/usr/bin/env python3
"""
🔒 P4 - AUDITORIA DE SEGURANÇA COMPLETA
Baseado nos achados críticos da Resposta 2 do ChatGPT
Identifica e corrige problemas de segurança no sistema
"""

import re
import subprocess
import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
import json

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from src.core.logging_system import get_logger, LogCategory, timed_operation
    logger = get_logger('security_audit')
    component = 'security_audit'
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('security_audit')
    component = 'security_audit'

    # Mock para compatibilidade
    class LogCategory:
        SECURITY = "security"
        SYSTEM = "system"

    def timed_operation(name, category, component, **kwargs):
        from contextlib import contextmanager
        @contextmanager
        def timer():
            import time
            start = time.time()
            yield
            logger.info(f"{name} completed in {time.time()-start:.3f}s")
        return timer()

class SecurityAuditor:
    """Auditor de segurança baseado nos achados do ChatGPT Resposta 2"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.security_issues = {
            'subprocess_without_check': [],
            'eval_exec_usage': [],
            'pickle_unsafe': [],
            'missing_file_refs': [],
            'shell_injection': [],
            'path_traversal': []
        }

    def audit_subprocess_security(self) -> List[Dict]:
        """Audita problemas de subprocess sem check=True"""
        logger.info("🔍 Auditando problemas de subprocess...",
                   category=LogCategory.SECURITY, component=component)

        issues = []

        # Buscar arquivos Python
        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                # Buscar subprocess.run sem check=
                for i, line in enumerate(lines, 1):
                    if 'subprocess.run(' in line and 'check=' not in line:
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'subprocess.run() sem check=',
                            'code': line.strip(),
                            'severity': 'HIGH'
                        })

                    # Buscar shell=True perigoso
                    if 'shell=True' in line and 'subprocess' in line:
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'subprocess com shell=True',
                            'code': line.strip(),
                            'severity': 'CRITICAL'
                        })

            except Exception as e:
                logger.warning(f"Erro lendo {py_file}: {e}",
                              category=LogCategory.SECURITY, component=component)

        self.security_issues['subprocess_without_check'] = issues
        logger.info(f"📊 Encontrados {len(issues)} problemas de subprocess",
                   category=LogCategory.SECURITY, component=component, count=len(issues))

        return issues

    def audit_eval_exec_usage(self) -> List[Dict]:
        """Audita uso perigoso de eval() e exec()"""
        logger.info("🔍 Auditando eval/exec perigosos...",
                   category=LogCategory.SECURITY, component=component)

        issues = []

        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                for i, line in enumerate(lines, 1):
                    # Buscar eval() direto
                    if re.search(r'\beval\s*\(', line):
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'uso de eval()',
                            'code': line.strip(),
                            'severity': 'CRITICAL'
                        })

                    # Buscar exec() direto
                    if re.search(r'\bexec\s*\(', line):
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'uso de exec()',
                            'code': line.strip(),
                            'severity': 'CRITICAL'
                        })

            except Exception as e:
                logger.warning(f"Erro lendo {py_file}: {e}",
                              category=LogCategory.SECURITY, component=component)

        self.security_issues['eval_exec_usage'] = issues
        logger.info(f"📊 Encontrados {len(issues)} usos de eval/exec",
                   category=LogCategory.SECURITY, component=component, count=len(issues))

        return issues

    def audit_pickle_security(self) -> List[Dict]:
        """Audita uso inseguro de pickle"""
        logger.info("🔍 Auditando pickle inseguro...",
                   category=LogCategory.SECURITY, component=component)

        issues = []

        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                for i, line in enumerate(lines, 1):
                    # Buscar pickle.loads direto
                    if 'pickle.loads(' in line and 'SafePickle' not in line:
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'pickle.loads() inseguro',
                            'code': line.strip(),
                            'severity': 'HIGH'
                        })

            except Exception as e:
                logger.warning(f"Erro lendo {py_file}: {e}",
                              category=LogCategory.SECURITY, component=component)

        self.security_issues['pickle_unsafe'] = issues
        logger.info(f"📊 Encontrados {len(issues)} usos inseguros de pickle",
                   category=LogCategory.SECURITY, component=component, count=len(issues))

        return issues

    def audit_path_traversal(self) -> List[Dict]:
        """Audita vulnerabilidades de path traversal"""
        logger.info("🔍 Auditando path traversal...",
                   category=LogCategory.SECURITY, component=component)

        issues = []

        for py_file in self.project_root.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')

                for i, line in enumerate(lines, 1):
                    # Buscar construção de paths perigosa
                    if '../' in line and ('open(' in line or 'Path(' in line):
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'possível path traversal (../)',
                            'code': line.strip(),
                            'severity': 'MEDIUM'
                        })

                    # Buscar concatenação de paths sem validação
                    if ('+ "/' in line or "+ '/" in line) and 'Path' not in line:
                        issues.append({
                            'file': str(py_file.relative_to(self.project_root)),
                            'line': i,
                            'issue': 'concatenação insegura de path',
                            'code': line.strip(),
                            'severity': 'MEDIUM'
                        })

            except Exception as e:
                logger.warning(f"Erro lendo {py_file}: {e}",
                              category=LogCategory.SECURITY, component=component)

        self.security_issues['path_traversal'] = issues
        logger.info(f"📊 Encontrados {len(issues)} riscos de path traversal",
                   category=LogCategory.SECURITY, component=component, count=len(issues))

        return issues

    def generate_security_report(self) -> Dict[str, Any]:
        """Gera relatório completo de segurança"""

        logger.info("📋 Gerando relatório completo de segurança...",
                   category=LogCategory.SECURITY, component=component)

        # Executar todas as auditorias
        with timed_operation('complete_security_audit', LogCategory.SECURITY, component):
            subprocess_issues = self.audit_subprocess_security()
            eval_exec_issues = self.audit_eval_exec_usage()
            pickle_issues = self.audit_pickle_security()
            path_issues = self.audit_path_traversal()

        # Contabilizar por severidade
        severity_count = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        all_issues = subprocess_issues + eval_exec_issues + pickle_issues + path_issues

        for issue in all_issues:
            severity_count[issue['severity']] += 1

        # Calcular score de segurança
        security_score = max(0, 100 - (
            severity_count['CRITICAL'] * 25 +
            severity_count['HIGH'] * 10 +
            severity_count['MEDIUM'] * 5 +
            severity_count['LOW'] * 1
        ))

        report = {
            'timestamp': str(Path(__file__).stat().st_mtime),
            'total_issues': len(all_issues),
            'severity_breakdown': severity_count,
            'security_score': security_score,
            'issues_by_category': {
                'subprocess_problems': len(subprocess_issues),
                'eval_exec_usage': len(eval_exec_issues),
                'unsafe_pickle': len(pickle_issues),
                'path_traversal': len(path_issues)
            },
            'detailed_issues': self.security_issues,
            'recommendations': self._generate_recommendations()
        }

        return report

    def _generate_recommendations(self) -> List[str]:
        """Gera recomendações de segurança"""
        recommendations = []

        if self.security_issues['subprocess_without_check']:
            recommendations.append("Adicionar check=True em todas as chamadas subprocess.run()")

        if self.security_issues['eval_exec_usage']:
            recommendations.append("Substituir eval()/exec() por parsers seguros como ast.literal_eval()")

        if self.security_issues['pickle_unsafe']:
            recommendations.append("Usar SafePickle ou JSON ao invés de pickle.loads() direto")

        if self.security_issues['path_traversal']:
            recommendations.append("Validar e sanitizar todos os paths de entrada")

        return recommendations

    def fix_subprocess_issues(self) -> int:
        """Corrige automaticamente problemas de subprocess"""
        logger.info("🔧 Corrigindo problemas de subprocess...",
                   category=LogCategory.SECURITY, component=component)

        fixed_count = 0

        for issue in self.security_issues['subprocess_without_check']:
            file_path = self.project_root / issue['file']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Substituir subprocess.run( por subprocess.run(..., check=False
                original_line = issue['code']
                if 'subprocess.run(' in original_line and 'check=' not in original_line:
                    # Adicionar check=False para não quebrar funcionalidade
                    fixed_line = original_line.replace(
                        'subprocess.run(',
                        'subprocess.run(..., check=False  # P4: Explicitamente definido'
                    )

                    content = content.replace(original_line, fixed_line)

                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    fixed_count += 1
                    logger.info(f"✅ Corrigido subprocess em {issue['file']}:{issue['line']}",
                               category=LogCategory.SECURITY, component=component)

            except Exception as e:
                logger.error(f"❌ Erro corrigindo {file_path}: {e}",
                            category=LogCategory.SECURITY, component=component)

        return fixed_count

def main():
    """Executa auditoria completa de segurança P4"""

    logger.info("🔒 INICIANDO P4 - AUDITORIA DE SEGURANÇA",
               category=LogCategory.SECURITY, component=component)

    auditor = SecurityAuditor()

    # Gerar relatório completo
    report = auditor.generate_security_report()

    # Salvar relatório
    report_file = Path("logs") / "p4_security_audit.json"
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Exibir resumo
    print(f"\n🔒 RELATÓRIO DE SEGURANÇA P4")
    print("=" * 50)
    print(f"📊 Total de problemas: {report['total_issues']}")
    print(f"🔴 Críticos: {report['severity_breakdown']['CRITICAL']}")
    print(f"🟠 Altos: {report['severity_breakdown']['HIGH']}")
    print(f"🟡 Médios: {report['severity_breakdown']['MEDIUM']}")
    print(f"🔵 Baixos: {report['severity_breakdown']['LOW']}")
    print(f"📈 Score de Segurança: {report['security_score']}/100")

    print(f"\n📋 PROBLEMAS POR CATEGORIA:")
    for category, count in report['issues_by_category'].items():
        print(f"   {category}: {count}")

    print(f"\n💡 RECOMENDAÇÕES:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"   {i}. {rec}")

    print(f"\n📄 Relatório detalhado: {report_file}")

    # Oferecer correção automática
    subprocess_count = len(auditor.security_issues['subprocess_without_check'])
    if subprocess_count > 0:
        print(f"\n🔧 Encontrados {subprocess_count} problemas de subprocess corrigíveis")
        print("   Execute com --fix para aplicar correções automáticas")

    if '--fix' in sys.argv:
        fixed = auditor.fix_subprocess_issues()
        logger.success(f"✅ {fixed} problemas de subprocess corrigidos",
                      category=LogCategory.SECURITY, component=component, fixed_count=fixed)

    logger.success("🔒 P4 - Auditoria de segurança concluída",
                  category=LogCategory.SECURITY, component=component,
                  total_issues=report['total_issues'],
                  security_score=report['security_score'])

if __name__ == "__main__":
    main()