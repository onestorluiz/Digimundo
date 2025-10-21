#!/bin/bash
# Register all Scripturemon Ultimate models with Ollama

echo "🎬 Registering Scripturemon Ultimate models..."
echo "This will create 25 models (23 specialists + orchestrator + evaluator)"
echo ""

# Counter for progress
count=0
total=25

# Register orchestrator
echo "[1/$total] Creating orchestrator..."
ollama create scripturemon-orchestrator -f 00_orchestrator.modelfile
((count++))

# Register all specialists
for file in [0-9][0-9]_*.modelfile; do
    if [[ "$file" != "00_orchestrator.modelfile" && "$file" != "24_evaluator_70b.modelfile" ]]; then
        # Extract name without number prefix and extension
        name=$(basename "$file" .modelfile)
        name_clean=${name#*_}  # Remove number prefix

        ((count++))
        echo "[$count/$total] Creating specialist: $name_clean..."
        ollama create "scripturemon-$name_clean" -f "$file"
    fi
done

# Register evaluator
((count++))
echo "[$count/$total] Creating 70B evaluator..."
ollama create scripturemon-evaluator -f 24_evaluator_70b.modelfile

echo ""
echo "✅ Registration complete!"
echo ""
echo "To list all Scripturemon models:"
echo "  ollama list | grep scripturemon"
echo ""
echo "To test a specialist:"
echo "  ollama run scripturemon-dialogue < test_screenplay.txt"
echo ""
echo "To remove all Scripturemon models:"
echo "  ollama list | grep scripturemon | awk '{print $1}' | xargs -I {} ollama rm {}"
