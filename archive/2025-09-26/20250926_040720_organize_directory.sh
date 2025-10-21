#!/bin/bash
# Script to organize scripturemon-ultimate directory

echo "🎬 ORGANIZING SCRIPTUREMON ULTIMATE DIRECTORY"
echo "============================================"

# Create organized structure
echo "📁 Creating organized directories..."
mkdir -p archive/test_outputs
mkdir -p archive/old_tests
mkdir -p archive/temp_files
mkdir -p docs
mkdir -p test_scripts

# ESSENTIAL FILES TO KEEP IN ROOT (System Core)
ESSENTIAL_FILES=(
    "scripturemon_ultimate_system.py"
    "quality_evaluator_ultimate.py"
    "scripturemon_ollama_hybrid.py"
    "generate_modelfiles.py"
    "orchestrator_ultimate.py"
    "orchestrator_with_memory.py"
    "ollama_with_memory.py"
    "quality_synthesizer.py"
    "rag_integration.py"
    "enhanced_json_parser.py"
    "symbiotic_fusion_strategies.py"
    "setup.py"
)

# Move test outputs to archive
echo "📦 Archiving test outputs..."
for file in *_test_*.txt *_test_*.json; do
    if [[ -f "$file" ]]; then
        echo "  Moving $file to archive/test_outputs/"
        mv "$file" archive/test_outputs/ 2>/dev/null
    fi
done

# Move numbered/timestamp outputs
for file in *_[0-9]*.txt; do
    if [[ -f "$file" ]]; then
        # Check if it's not an essential file
        is_essential=false
        for essential in "${ESSENTIAL_FILES[@]}"; do
            if [[ "$file" == "$essential" ]]; then
                is_essential=true
                break
            fi
        done

        if [[ "$is_essential" == false ]]; then
            echo "  Moving $file to archive/test_outputs/"
            mv "$file" archive/test_outputs/ 2>/dev/null
        fi
    fi
done

# Move test Python scripts
echo "📝 Moving test scripts..."
for file in test_*.py; do
    if [[ -f "$file" ]]; then
        echo "  Moving $file to test_scripts/"
        mv "$file" test_scripts/ 2>/dev/null
    fi
done

# Move comparison and method files
echo "📊 Archiving comparison files..."
for file in *comparison*.* *method*.* *forensic*.* *surgeon*.*; do
    if [[ -f "$file" ]]; then
        echo "  Moving $file to archive/old_tests/"
        mv "$file" archive/old_tests/ 2>/dev/null
    fi
done

# Move log files
echo "📋 Organizing log files..."
for file in *.log; do
    if [[ -f "$file" ]]; then
        echo "  Moving $file to archive/"
        mv "$file" archive/ 2>/dev/null
    fi
done

# Move documentation to docs
echo "📚 Organizing documentation..."
for file in *.md; do
    if [[ -f "$file" ]]; then
        # Keep README in root
        if [[ "$file" != "README.md" ]]; then
            echo "  Moving $file to docs/"
            mv "$file" docs/ 2>/dev/null
        fi
    fi
done

# Clean up temp files
echo "🧹 Cleaning temporary files..."
for file in *.tmp *.temp *.cache .DS_Store; do
    if [[ -f "$file" ]]; then
        rm "$file" 2>/dev/null
        echo "  Removed $file"
    fi
done

# Create README if doesn't exist
if [[ ! -f "README.md" ]]; then
    echo "📝 Creating README..."
    cat > README.md << 'EOF'
# Scripturemon Ultimate System

## Overview
Professional screenplay analysis system with 23 specialized AI analysts.

## Main Components

### Core System Files
- `scripturemon_ultimate_system.py` - Main sequential analysis system
- `quality_evaluator_ultimate.py` - 70B model final evaluator
- `scripturemon_ollama_hybrid.py` - Ollama integration for chat

### Orchestrators
- `orchestrator_ultimate.py` - Main orchestrator
- `orchestrator_with_memory.py` - Memory-enhanced version

### Integration
- `generate_modelfiles.py` - Creates Ollama modelfiles
- `ollama_with_memory.py` - Ollama with memory system
- `rag_integration.py` - RAG system integration

## Directory Structure
```
scripturemon-ultimate/
├── super_specialists/     # 23 specialist prompts
├── modelfiles/           # Ollama model definitions
├── analysis_reports/     # Generated analysis reports
├── test_scripts/         # Test scripts
├── archive/             # Archived tests and outputs
└── docs/                # Documentation
```

## Usage

### Basic Analysis
```bash
python3 scripturemon_ultimate_system.py screenplay.txt "Title"
```

### Ollama Chat Mode
```bash
ollama run scripturemon-master
```

### Generate Modelfiles
```bash
python3 generate_modelfiles.py
cd modelfiles && ./register_models.sh
```

## Requirements
- Python 3.8+
- Ollama
- 32GB+ RAM recommended
- Mixtral 8x7b and Llama 70B models

## 23 Specialists
1. DIALOGUE - McKee, Sorkin, Tarantino
2. CHARACTER - Truby, Egri, Campbell
3. PACING - Field, Snyder, Goldman
4. THEME - Truby, McKee, Kaufman
5. ACTION - Cameron, Miller, Nolan
6. STRUCTURE - Field, McKee, Snyder
7. CONFLICT - McKee, Truby, Mamet
8. TENSION - Hitchcock, Fincher, Nolan
9. SUBTEXT - Kazan, Bergman, Lynch
10. EXPOSITION - Goldman, Sorkin
11. TRANSITIONS - Eisenstein, Kurosawa
12. OPENING - McKee, Snyder
13. CLIMAX - Aristotle, McKee
14. RESOLUTION - Field, Truby
15. WORLD-BUILDING - Lucas, Cameron, Nolan
16. STAKES - Snyder, McKee
17. MOTIVATION - Stanislavski, Meisner
18. BACKSTORY - Truby, McKee
19. FORESHADOWING - Hitchcock, Shyamalan
20. TWIST - Shyamalan, Nolan, Fincher
21. SYMBOLISM - Jung, Campbell, Lynch
22. TONE - Coen, Anderson, Tarantino
23. GENRE - Snyder, McKee, Truby
EOF
fi

# Summary
echo ""
echo "✅ ORGANIZATION COMPLETE!"
echo ""
echo "📊 Directory Structure:"
echo "  ├── Core system files: kept in root"
echo "  ├── super_specialists/: specialist prompts"
echo "  ├── modelfiles/: Ollama models"
echo "  ├── analysis_reports/: analysis outputs"
echo "  ├── test_scripts/: all test*.py files"
echo "  ├── archive/: old tests and outputs"
echo "  └── docs/: documentation"
echo ""
echo "🎯 Essential files preserved in root:"
for file in "${ESSENTIAL_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "  ✓ $file"
    fi
done
echo ""
echo "Run 'ls -la' to see the clean structure!"