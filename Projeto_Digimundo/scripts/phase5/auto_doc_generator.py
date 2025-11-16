#!/usr/bin/env python3
"""
📝 AUTO-GENERATED DOCUMENTATION SYSTEM

Nível: ALÉM DO ALÉM DO VALE DO SILÍCIO

Este sistema:
1. Analisa código Python semanticamente (AST)
2. Gera documentação markdown automaticamente
3. Cria diagramas de arquitetura (Mermaid)
4. Documenta APIs, models, services
5. Atualiza docs quando código muda

Usage:
    python3 scripts/phase5/auto_doc_generator.py
    python3 scripts/phase5/auto_doc_generator.py --target app/services
    python3 scripts/phase5/auto_doc_generator.py --format markdown
    python3 scripts/phase5/auto_doc_generator.py --diagrams
"""

import ast
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# Colors
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


class CodeAnalyzer(ast.NodeVisitor):
    """Analyze Python code using AST"""

    def __init__(self):
        self.classes = []
        self.functions = []
        self.imports = []
        self.current_class = None

    def visit_ClassDef(self, node):
        """Visit class definition"""
        class_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'methods': [],
            'bases': [base.id if isinstance(base, ast.Name) else str(base) for base in node.bases],
            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list],
            'line': node.lineno
        }

        self.current_class = class_info
        self.generic_visit(node)
        self.classes.append(class_info)
        self.current_class = None

    def visit_FunctionDef(self, node):
        """Visit function definition"""
        func_info = {
            'name': node.name,
            'docstring': ast.get_docstring(node),
            'args': [arg.arg for arg in node.args.args],
            'decorators': [d.id if isinstance(d, ast.Name) else str(d) for d in node.decorator_list],
            'line': node.lineno,
            'is_async': isinstance(node, ast.AsyncFunctionDef)
        }

        if self.current_class:
            self.current_class['methods'].append(func_info)
        else:
            self.functions.append(func_info)

        self.generic_visit(node)

    def visit_Import(self, node):
        """Visit import statement"""
        for alias in node.names:
            self.imports.append({
                'module': alias.name,
                'alias': alias.asname
            })

    def visit_ImportFrom(self, node):
        """Visit from X import Y statement"""
        for alias in node.names:
            self.imports.append({
                'module': f"{node.module}.{alias.name}" if node.module else alias.name,
                'alias': alias.asname
            })


class DocumentationGenerator:
    """Generate documentation from code"""

    def __init__(self, target_dir: str = "app"):
        self.project_root = self._detect_project_root()
        self.target_dir = self.project_root / target_dir
        self.docs_dir = self.project_root.parent / 'docs' / 'auto_generated'
        self.docs_dir.mkdir(exist_ok=True)

    def _detect_project_root(self) -> Path:
        """Auto-detect project root"""
        current = Path.cwd()

        if (current / 'app').exists() and (current / 'tests').exists():
            return current

        if (current / 'cineprod-flask').exists():
            return current / 'cineprod-flask'

        if current.name == 'scripts':
            parent = current.parent.parent
            if (parent / 'cineprod-flask').exists():
                return parent / 'cineprod-flask'

        return current

    def analyze_file(self, filepath: Path) -> Optional[CodeAnalyzer]:
        """Analyze a Python file"""
        try:
            content = filepath.read_text(encoding='utf-8')
            tree = ast.parse(content)

            analyzer = CodeAnalyzer()
            analyzer.visit(tree)

            return analyzer

        except Exception as e:
            print(f"⚠️  Failed to analyze {filepath}: {e}")
            return None

    def generate_service_docs(self) -> str:
        """Generate documentation for services"""
        print(f"{BLUE}📝 Generating service documentation...{RESET}")

        services_dir = self.target_dir / 'services'
        if not services_dir.exists():
            print(f"{YELLOW}⚠️  Services directory not found{RESET}")
            return ""

        services = []

        for service_file in sorted(services_dir.glob('*_service.py')):
            print(f"  Analyzing {service_file.name}...")

            analyzer = self.analyze_file(service_file)
            if not analyzer:
                continue

            services.append({
                'filename': service_file.name,
                'analyzer': analyzer
            })

        # Generate markdown
        doc = "# 📦 Services Documentation\n\n"
        doc += f"**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        doc += "---\n\n"

        for service in services:
            filename = service['filename']
            analyzer = service['analyzer']

            doc += f"## {filename}\n\n"

            # Classes
            for cls in analyzer.classes:
                doc += f"### `{cls['name']}`\n\n"

                if cls['docstring']:
                    doc += f"{cls['docstring']}\n\n"

                if cls['bases']:
                    doc += f"**Inherits from**: `{', '.join(cls['bases'])}`\n\n"

                # Methods
                if cls['methods']:
                    doc += "**Methods**:\n\n"
                    for method in cls['methods']:
                        args = ', '.join(method['args'])
                        doc += f"- `{method['name']}({args})`"

                        if method['docstring']:
                            first_line = method['docstring'].split('\n')[0]
                            doc += f" - {first_line}"

                        doc += "\n"

                    doc += "\n"

            # Standalone functions
            if analyzer.functions:
                doc += "**Functions**:\n\n"
                for func in analyzer.functions:
                    args = ', '.join(func['args'])
                    doc += f"- `{func['name']}({args})`"

                    if func['docstring']:
                        first_line = func['docstring'].split('\n')[0]
                        doc += f" - {first_line}"

                    doc += "\n"

                doc += "\n"

            doc += "---\n\n"

        print(f"{GREEN}✅ Generated documentation for {len(services)} services{RESET}")

        return doc

    def generate_model_docs(self) -> str:
        """Generate documentation for models"""
        print(f"{BLUE}📝 Generating model documentation...{RESET}")

        models_dir = self.target_dir / 'models'
        if not models_dir.exists():
            print(f"{YELLOW}⚠️  Models directory not found{RESET}")
            return ""

        models = []

        for model_file in sorted(models_dir.glob('*.py')):
            if model_file.name == '__init__.py':
                continue

            print(f"  Analyzing {model_file.name}...")

            analyzer = self.analyze_file(model_file)
            if not analyzer:
                continue

            models.append({
                'filename': model_file.name,
                'analyzer': analyzer
            })

        # Generate markdown
        doc = "# 📊 Models Documentation\n\n"
        doc += f"**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        doc += "---\n\n"

        for model in models:
            filename = model['filename']
            analyzer = model['analyzer']

            for cls in analyzer.classes:
                doc += f"## `{cls['name']}` Model\n\n"
                doc += f"**File**: `app/models/{filename}`\n\n"

                if cls['docstring']:
                    doc += f"{cls['docstring']}\n\n"

                if cls['bases']:
                    doc += f"**Inherits from**: `{', '.join(cls['bases'])}`\n\n"

                doc += "---\n\n"

        print(f"{GREEN}✅ Generated documentation for {len(models)} models{RESET}")

        return doc

    def generate_architecture_diagram(self) -> str:
        """Generate Mermaid architecture diagram"""
        print(f"{BLUE}📊 Generating architecture diagram...{RESET}")

        # Scan project structure
        services = list((self.target_dir / 'services').glob('*_service.py'))
        models = list((self.target_dir / 'models').glob('*.py'))
        routes = list((self.target_dir / 'routes').glob('*.py'))

        diagram = "```mermaid\ngraph TB\n"
        diagram += "    subgraph Client Layer\n"
        diagram += "        API[REST API]\n"
        diagram += "    end\n\n"

        diagram += "    subgraph Routes Layer\n"

        for route in routes[:5]:  # Limit to first 5
            name = route.stem.replace('_', ' ').title()
            diagram += f"        R{route.stem}[{name}]\n"

        diagram += "    end\n\n"

        diagram += "    subgraph Services Layer\n"

        for service in services[:5]:
            name = service.stem.replace('_service', '').replace('_', ' ').title()
            diagram += f"        S{service.stem}[{name} Service]\n"

        diagram += "    end\n\n"

        diagram += "    subgraph Models Layer\n"

        for model in models[:5]:
            if model.name != '__init__.py':
                name = model.stem.replace('_', ' ').title()
                diagram += f"        M{model.stem}[{name}]\n"

        diagram += "    end\n\n"

        diagram += "    subgraph Database\n"
        diagram += "        DB[(PostgreSQL)]\n"
        diagram += "    end\n\n"

        # Connections
        diagram += "    API --> R{routes[0].stem if routes else 'routes'}\n"

        if services:
            diagram += f"    R{routes[0].stem if routes else 'routes'} --> S{services[0].stem}\n"

        if services and models:
            diagram += f"    S{services[0].stem} --> M{models[0].stem}\n"

        diagram += "    M{} --> DB\n".format(models[0].stem if models else 'models')

        diagram += "```\n"

        print(f"{GREEN}✅ Generated architecture diagram{RESET}")

        return diagram

    def generate_api_docs(self) -> str:
        """Generate API documentation from routes"""
        print(f"{BLUE}📝 Generating API documentation...{RESET}")

        routes_dir = self.target_dir / 'routes'
        if not routes_dir.exists():
            print(f"{YELLOW}⚠️  Routes directory not found{RESET}")
            return ""

        doc = "# 🌐 API Documentation\n\n"
        doc += f"**Auto-generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        doc += "---\n\n"

        endpoints = []

        for route_file in sorted(routes_dir.glob('*.py')):
            if route_file.name == '__init__.py':
                continue

            content = route_file.read_text()

            # Extract route decorators
            route_pattern = r"@\w+\.route\('([^']+)'(?:,\s*methods=\[([^\]]+)\])?\)"
            matches = re.findall(route_pattern, content)

            for path, methods in matches:
                methods_list = [m.strip().strip("'\"") for m in methods.split(',')] if methods else ['GET']

                endpoints.append({
                    'path': path,
                    'methods': methods_list,
                    'file': route_file.name
                })

        # Group by file
        by_file = defaultdict(list)
        for ep in endpoints:
            by_file[ep['file']].append(ep)

        for filename, eps in sorted(by_file.items()):
            doc += f"## {filename.replace('.py', '').replace('_', ' ').title()}\n\n"

            for ep in eps:
                methods_str = ', '.join(ep['methods'])
                doc += f"### `{methods_str}` {ep['path']}\n\n"

            doc += "---\n\n"

        print(f"{GREEN}✅ Generated API documentation for {len(endpoints)} endpoints{RESET}")

        return doc

    def run(self) -> int:
        """Run documentation generation"""
        print(f"{BOLD}{MAGENTA}{'='*80}{RESET}")
        print(f"{BOLD}{MAGENTA}📝 AUTO-DOCUMENTATION GENERATOR{RESET}")
        print(f"{BOLD}{MAGENTA}{'='*80}{RESET}\n")

        # Generate all docs
        services_doc = self.generate_service_docs()
        models_doc = self.generate_model_docs()
        api_doc = self.generate_api_docs()
        architecture = self.generate_architecture_diagram()

        # Save files
        if services_doc:
            services_path = self.docs_dir / 'SERVICES.md'
            services_path.write_text(services_doc)
            print(f"{GREEN}💾 Saved: {services_path}{RESET}")

        if models_doc:
            models_path = self.docs_dir / 'MODELS.md'
            models_path.write_text(models_doc)
            print(f"{GREEN}💾 Saved: {models_path}{RESET}")

        if api_doc:
            api_path = self.docs_dir / 'API.md'
            api_path.write_text(api_doc)
            print(f"{GREEN}💾 Saved: {api_path}{RESET}")

        # Create index with architecture
        index_doc = "# 📚 Auto-Generated Documentation Index\n\n"
        index_doc += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        index_doc += "## 🏗️ Architecture Overview\n\n"
        index_doc += architecture
        index_doc += "\n## 📖 Documentation\n\n"
        index_doc += "- [Services Documentation](./SERVICES.md)\n"
        index_doc += "- [Models Documentation](./MODELS.md)\n"
        index_doc += "- [API Documentation](./API.md)\n"

        index_path = self.docs_dir / 'README.md'
        index_path.write_text(index_doc)
        print(f"{GREEN}💾 Saved: {index_path}{RESET}")

        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{GREEN}✅ Documentation generation complete!{RESET}")
        print(f"{'='*80}\n")

        return 0


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Auto-generate documentation')
    parser.add_argument('--target', default='app', help='Target directory to analyze')
    parser.add_argument('--format', default='markdown', help='Output format')
    parser.add_argument('--diagrams', action='store_true', help='Generate diagrams only')

    args = parser.parse_args()

    generator = DocumentationGenerator(target_dir=args.target)
    return generator.run()


if __name__ == '__main__':
    exit(main())
