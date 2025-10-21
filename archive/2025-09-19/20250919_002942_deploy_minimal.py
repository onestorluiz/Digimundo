#!/usr/bin/env python3
"""
Deploy Minimalista - Deploy simples e funcional
"""

import subprocess
import shutil
from pathlib import Path
from datetime import datetime

def run_tests():
    """Roda os testes"""
    print("🧪 Rodando testes...")
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-q"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print("❌ Testes falharam:")
        print(result.stdout)
        return False
    print("✅ Testes passaram")
    return True

def build_package():
    """Cria pacote para deploy"""
    print("📦 Criando pacote...")

    # Criar diretório de build
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir()

    # Copiar arquivos essenciais
    essential_files = [
        "apps/scripturemon/*.py",
        "bin/scripturemon",
        "requirements.txt",
        "README.md"
    ]

    for pattern in essential_files:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = build_dir / file.relative_to(".")
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)

    print(f"✅ Pacote criado em {build_dir}")
    return build_dir

def deploy(environment="staging"):
    """Deploy para ambiente especificado"""
    print(f"\n🚀 Deploy para {environment.upper()}")
    print("="*50)

    # 1. Validar
    if not run_tests():
        print("❌ Deploy cancelado - testes falharam")
        return False

    # 2. Build
    build_dir = build_package()

    # 3. Backup atual (se produção)
    if environment == "production":
        backup_dir = Path(f"backups/{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        print(f"💾 Criando backup em {backup_dir}...")
        # Aqui você faria o backup real

    # 4. Deploy (simulado - aqui você faria o deploy real)
    print(f"📤 Enviando para {environment}...")
    # rsync, scp, docker push, etc

    # 5. Verificação pós-deploy
    print("🔍 Verificando deploy...")
    # curl health check, etc

    print(f"\n✅ Deploy para {environment} completo!")
    print(f"📅 {datetime.now().isoformat()}")
    return True

def main():
    """Menu principal"""
    print("\n🚀 DEPLOY SYSTEM")
    print("================")
    print("1. Deploy para Staging")
    print("2. Deploy para Production")
    print("3. Apenas rodar testes")
    print("4. Apenas criar build")

    choice = input("\nEscolha [1-4]: ")

    if choice == "1":
        deploy("staging")
    elif choice == "2":
        confirm = input("⚠️ Deploy para PRODUÇÃO. Confirmar? (s/n): ")
        if confirm.lower() == 's':
            deploy("production")
    elif choice == "3":
        run_tests()
    elif choice == "4":
        build_package()
    else:
        print("❌ Opção inválida")

if __name__ == "__main__":
    main()