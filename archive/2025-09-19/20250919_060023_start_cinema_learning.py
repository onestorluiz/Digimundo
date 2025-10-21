#!/usr/bin/env python3
"""
🎓 START CINEMA LEARNING - Inicializa aprendizado contínuo
Sistema automatizado de treinamento com PDFs de cinema
"""

import sys
import asyncio
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def main():
    print("🎬 CINEMA LEARNING SYSTEM")
    print("=" * 60)

    try:
        from src.learning.ollama_cinema_trainer import OllamaCinemaTrainer
        from src.core.config import get_config

        # Verificar configuração
        config = get_config()
        print(f"📁 Data directory: {config.paths.pdfs_dir}")
        print(f"📚 PDFs available: {len(list(config.paths.pdfs_dir.glob('*.pdf')))}")

        # Verificar TXTs convertidos
        screenplays_dir = Path(config.paths.pdfs_dir.parent / "screenplays")
        txt_files = list(screenplays_dir.glob("*.txt")) if screenplays_dir.exists() else []
        print(f"📄 TXTs available: {len(txt_files)}")

        if not txt_files:
            print("\n⚠️ No TXT files found!")
            print("Please convert PDFs to TXT first:")
            print("  python3 scripts/convert_pdf_to_txt.py")
            return

        # Inicializar trainer
        print("\n🧠 Initializing Cinema Trainer...")
        trainer = OllamaCinemaTrainer()

        # Menu de opções
        print("\nSelect training mode:")
        print("1. Quick learning (5 minutes)")
        print("2. Standard learning (30 minutes)")
        print("3. Deep learning (2 hours)")
        print("4. Single document test")
        print("5. Evolve existing models")

        choice = input("\nChoice (1-5): ").strip()

        if choice == "1":
            print("\n🚀 Starting quick learning session...")
            await trainer.continuous_learning_session(duration_minutes=5)

        elif choice == "2":
            print("\n🚀 Starting standard learning session...")
            await trainer.continuous_learning_session(duration_minutes=30)

        elif choice == "3":
            print("\n🚀 Starting deep learning session...")
            await trainer.continuous_learning_session(duration_minutes=120)

        elif choice == "4":
            print("\n📄 Available documents:")
            for i, txt in enumerate(txt_files[:10], 1):
                print(f"  {i}. {txt.name}")

            doc_choice = input("\nSelect document (1-10): ").strip()
            if doc_choice.isdigit() and 1 <= int(doc_choice) <= len(txt_files):
                doc_path = txt_files[int(doc_choice) - 1]
                print(f"\n📖 Training on: {doc_path.name}")
                knowledge = await trainer.train_on_document(doc_path)
                print(f"✅ Extracted {len(knowledge)} concepts")

        elif choice == "5":
            print("\n🧬 Evolving models with accumulated knowledge...")

            # Evoluir modelos principais
            models_to_evolve = [
                "scripturemon-cpu-themes",
                "scripturemon-cpu-structure",
                "scripturemon-cpu-dialogue",
                "scripturemon-cpu-symbolism"
            ]

            for model in models_to_evolve:
                print(f"\n  Evolving {model}...")
                try:
                    modelfile = await trainer.evolve_model(model)
                    print(f"  ✅ Created: {modelfile}")
                except Exception as e:
                    print(f"  ❌ Error: {e}")

        # Mostrar estatísticas finais
        print("\n📊 LEARNING STATISTICS:")

        # Recuperar conhecimento acumulado
        knowledge_items = trainer.get_accumulated_knowledge()
        print(f"  Total concepts: {len(knowledge_items)}")

        # Mostrar top 10 conceitos
        if knowledge_items:
            print("\n  Top concepts learned:")
            for i, item in enumerate(knowledge_items[:10], 1):
                print(f"    {i}. {item.concept} (confidence: {item.confidence:.2f})")

        print("\n✅ Cinema Learning Complete!")
        print("Models enriched with cinematic knowledge")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting Cinema Learning System...")
    asyncio.run(main())