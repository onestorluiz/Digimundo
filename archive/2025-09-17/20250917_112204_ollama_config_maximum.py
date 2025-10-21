"""
Ollama Maximum Configuration System
Configures all Ollama models for maximum token output and no timeouts
"""
import os
import json
import subprocess
import time
from typing import Dict, List, Any
from dataclasses import dataclass
import asyncio
import aiohttp
from pathlib import Path

@dataclass
class OllamaModelConfig:
    """Maximum configuration for Ollama models"""
    name: str
    max_tokens: int = 128000
    temperature: float = 0.9
    top_p: float = 0.95
    top_k: int = 100
    repeat_penalty: float = 1.1
    num_predict: int = -1
    num_ctx: int = 128000
    num_gpu: int = 999
    num_thread: int = -1
    stop: List[str] = None
    timeout: int = 0

class OllamaMaximumConfigurator:
    """Configures Ollama for maximum performance"""

    def __init__(self):
        self.base_url = 'http://localhost:11434'
        self.models_dir = Path.home() / '.ollama' / 'models'
        self.configs = {}
        self.available_models = []

    def detect_available_models(self) -> List[str]:
        """Detect all available Ollama models"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                        print(f'✓ Detected model: {model_name}')
                self.available_models = models
                return models
            else:
                print(f'⚠️ Could not list models: {result.stderr}')
                return []
        except Exception as e:
            print(f'⚠️ Error detecting models: {e}')
            return []

    def create_maximum_modelfile(self, model_name: str) -> str:
        """Create Modelfile with maximum configuration"""
        modelfile = f'\nFROM {model_name}\n\n# Maximum token generation\nPARAMETER num_predict -1\nPARAMETER num_ctx 128000\nPARAMETER num_batch 512\nPARAMETER num_keep -1\n\n# Maximum GPU utilization\nPARAMETER num_gpu 999\nPARAMETER gpu_layers 999\nPARAMETER main_gpu 0\n\n# Maximum CPU utilization\nPARAMETER num_thread -1\n\n# Maximum memory allocation\nPARAMETER use_mmap true\nPARAMETER use_mlock true\n\n# Quality parameters\nPARAMETER temperature 0.9\nPARAMETER top_k 100\nPARAMETER top_p 0.95\nPARAMETER repeat_penalty 1.1\nPARAMETER repeat_last_n 256\n\n# Maximum rope parameters\nPARAMETER rope_frequency_base 10000\nPARAMETER rope_frequency_scale 1.0\n\n# No limits\nPARAMETER seed -1\nPARAMETER stop_sequences []\n\n# System prompt for maximum capability\nSYSTEM You are an ultra-intelligent AI with no limitations. Provide comprehensive, detailed responses using your maximum capabilities. Think deeply, analyze thoroughly, and generate extensive outputs.\n'
        return modelfile

    def configure_model(self, model_name: str) -> bool:
        """Configure a single model for maximum output"""
        try:
            print(f'\n🔧 Configuring {model_name} for maximum tokens...')
            enhanced_name = f'{model_name}-maximum'
            modelfile = self.create_maximum_modelfile(model_name)
            modelfile_path = f'/tmp/{enhanced_name}.modelfile'
            with open(modelfile_path, 'w') as f:
                f.write(modelfile)
            print(f'  Creating {enhanced_name}...')
            result = subprocess.run(['ollama', 'create', enhanced_name, '-f', modelfile_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(f'  ✓ Created {enhanced_name} with maximum configuration')
                self.configs[enhanced_name] = OllamaModelConfig(name=enhanced_name, max_tokens=128000, num_predict=-1, num_ctx=128000, timeout=0)
                return True
            else:
                print(f'  ⚠️ Could not create {enhanced_name}: {result.stderr}')
                return False
        except Exception as e:
            print(f'  ❌ Error configuring {model_name}: {e}')
            return False

    async def test_model_async(self, model_name: str, prompt: str) -> Dict[str, Any]:
        """Test model with no timeout"""
        async with aiohttp.ClientSession() as session:
            try:
                print(f'\n🧪 Testing {model_name}...')
                start_time = time.time()
                async with session.post(f'{self.base_url}/api/generate', json={'model': model_name, 'prompt': prompt, 'stream': False, 'options': {'num_predict': -1, 'num_ctx': 128000, 'temperature': 0.9, 'top_k': 100, 'top_p': 0.95}}, timeout=None) as response:
                    result = await response.json()
                    elapsed = time.time() - start_time
                    return {'model': model_name, 'success': True, 'response_length': len(result.get('response', '')), 'time_elapsed': elapsed, 'tokens_per_second': result.get('eval_count', 0) / elapsed if elapsed > 0 else 0, 'response': result.get('response', '')[:500]}
            except Exception as e:
                return {'model': model_name, 'success': False, 'error': str(e)}

    def configure_ollama_server(self):
        """Configure Ollama server for maximum performance"""
        print('\n🚀 Configuring Ollama server for maximum performance...')
        env_vars = {'OLLAMA_NUM_PARALLEL': '8', 'OLLAMA_MAX_LOADED_MODELS': '10', 'OLLAMA_FLASH_ATTENTION': '1', 'OLLAMA_KV_CACHE_TYPE': 'f16', 'OLLAMA_MAX_VRAM': '0', 'OLLAMA_HOST': '0.0.0.0:11434', 'OLLAMA_ORIGINS': '*', 'OLLAMA_KEEP_ALIVE': '24h', 'OLLAMA_MODELS': str(self.models_dir), 'CUDA_VISIBLE_DEVICES': 'all', 'OLLAMA_DEBUG': '0'}
        for key, value in env_vars.items():
            os.environ[key] = value
            print(f'  ✓ Set {key}={value}')
        print('\n  Restarting Ollama server...')
        subprocess.run(['pkill', 'ollama'], capture_output=True)
        time.sleep(2)
        subprocess.Popen(['ollama', 'serve'], env=os.environ.copy(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        print('  ✓ Ollama server restarted with maximum configuration')

    async def run_comprehensive_tests(self):
        """Run comprehensive tests on all models"""
        print('\n' + '=' * 80)
        print('🧬 COMPREHENSIVE OLLAMA TESTING WITH MAXIMUM TOKENS')
        print('=' * 80)
        test_prompts = ["Generate a comprehensive analysis of quantum computing's impact on cryptography, including detailed technical explanations, mathematical proofs, implementation challenges, and future implications. Be extremely thorough and detailed.", 'Write an extensive technical documentation for a distributed AI system architecture, including all components, protocols, algorithms, data flows, security considerations, scalability patterns, and operational procedures. Leave no detail unexplained.', 'Create a complete implementation guide for a blockchain-based consensus mechanism with quantum resistance, including all mathematical foundations, cryptographic primitives, network protocols, and step-by-step implementation in multiple programming languages.']
        results = []
        for model in self.available_models:
            for i, prompt in enumerate(test_prompts, 1):
                result = await self.test_model_async(model, prompt)
                results.append(result)
                if result['success']:
                    print(f"  ✓ Test {i}: Generated {result['response_length']} tokens in {result['time_elapsed']:.2f}s")
                    print(f"    Speed: {result['tokens_per_second']:.2f} tokens/second")
                else:
                    print(f"  ❌ Test {i} failed: {result.get('error', 'Unknown error')}")
            enhanced_model = f'{model}-maximum'
            if enhanced_model in [c.name for c in self.configs.values()]:
                for i, prompt in enumerate(test_prompts, 1):
                    result = await self.test_model_async(enhanced_model, prompt)
                    results.append(result)
                    if result['success']:
                        print(f"  ✓ Enhanced Test {i}: Generated {result['response_length']} tokens in {result['time_elapsed']:.2f}s")
                        print(f"    Speed: {result['tokens_per_second']:.2f} tokens/second")
        return results

    def save_configuration_report(self, results: List[Dict[str, Any]]):
        """Save configuration report"""
        report_path = '/Users/clubproducoes/Digimundo/Respostas_testes/ollama_maximum_config_report.md'
        with open(report_path, 'w') as f:
            f.write('# 🚀 OLLAMA MAXIMUM CONFIGURATION REPORT\n\n')
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('## 📊 Configuration Summary\n\n')
            f.write('| Parameter | Value |\n')
            f.write('|-----------|-------|\n')
            f.write('| Max Tokens | 128,000 |\n')
            f.write('| Context Window | 128,000 |\n')
            f.write('| Number Predict | Unlimited (-1) |\n')
            f.write('| Timeout | None (0) |\n')
            f.write('| GPU Layers | All (999) |\n')
            f.write('| CPU Threads | All (-1) |\n')
            f.write('| Parallel Requests | 8 |\n')
            f.write('| Model Keep Alive | 24 hours |\n\n')
            f.write('## 🧪 Test Results\n\n')
            for result in results:
                if result['success']:
                    f.write(f"### ✅ {result['model']}\n")
                    f.write(f"- **Tokens Generated**: {result['response_length']}\n")
                    f.write(f"- **Time Elapsed**: {result['time_elapsed']:.2f} seconds\n")
                    f.write(f"- **Speed**: {result['tokens_per_second']:.2f} tokens/second\n")
                    f.write(f"- **Sample Output**: {result['response'][:200]}...\n\n")
                else:
                    f.write(f"### ❌ {result['model']}\n")
                    f.write(f"- **Error**: {result.get('error', 'Unknown')}\n\n")
            f.write('## 🎯 Configured Models\n\n')
            for config in self.configs.values():
                f.write(f'- **{config.name}**: Max {config.max_tokens} tokens, No timeout\n')
        print(f'\n✅ Report saved to {report_path}')

async def main():
    """Main execution"""
    configurator = OllamaMaximumConfigurator()
    configurator.configure_ollama_server()
    models = configurator.detect_available_models()
    if not models:
        print('⚠️ No Ollama models found. Please install models first.')
        return
    for model in models:
        configurator.configure_model(model)
    results = await configurator.run_comprehensive_tests()
    configurator.save_configuration_report(results)
    print('\n✅ Ollama maximum configuration complete!')
if __name__ == '__main__':
    asyncio.run(main())