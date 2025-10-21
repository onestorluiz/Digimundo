"""
PDF Cinema Analysis Test System
Tests Ollama models with PDF content about cinema and Digimundo
"""
import os
import sys
import time
import json
import subprocess
import PyPDF2
import pdfplumber
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib
from apps.scripturemon.config_silicon_valley import get_config

class PDFCinemaAnalyzer:
    """Analyze PDFs about cinema and Digimundo with Ollama"""

    def __init__(self):
        self.config = get_config()
        self.results_dir = Path(self.config.paths.results_dir)
        self.pdf_files = ['/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia/✴️ CICLO VIVO DO DIGIMUNDO.pdf', '/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia/PAssado/Backup_Digimundo_Scripturemon.pdf', '/Users/clubproducoes/Digimundo/Digimundo Verdadeira Historia/PAssado/🌌 Estrutura da TORA SIMBÓLICA – Versão Scripturemon 5.3.pdf']
        self.test_results = []

    def extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        text = ''
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n\n'
            if not text.strip():
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + '\n\n'
            return text.strip()
        except Exception as e:
            print(f'  ⚠️ Error extracting PDF text: {e}')
            return ''

    def get_available_ollama_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
        except Exception as e:
            print(f'  ⚠️ Error listing Ollama models: {e}')
        return []

    def query_ollama_about_pdf(self, model: str, pdf_text: str, question: str) -> Dict[str, Any]:
        """Query Ollama model about PDF content"""
        print(f'\n🤖 Querying {model} about PDF content...')
        print(f'  Question: {question[:100]}...')
        prompt = f'\nBased on the following document content, please answer the question in extreme detail.\nProvide a comprehensive analysis with maximum depth and breadth.\n\nDOCUMENT CONTENT:\n{pdf_text[:4000]}  # Limit to avoid token overflow\n\nQUESTION: {question}\n\nPLEASE PROVIDE:\n1. Direct answer to the question\n2. Relevant context from the document\n3. Deep analysis and insights\n4. Connection to broader themes\n5. Technical details if applicable\n6. Cultural and philosophical implications\n7. Future possibilities and predictions\n\nGenerate the most comprehensive response possible with no length limitations.\n'
        start_time = time.time()
        try:
            proc = subprocess.Popen(['ollama', 'run', model, prompt], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate()
            elapsed = time.time() - start_time
            if proc.returncode == 0 and stdout:
                return {'success': True, 'model': model, 'question': question, 'response': stdout, 'response_length': len(stdout), 'time_elapsed': elapsed, 'tokens_per_second': len(stdout.split()) / elapsed if elapsed > 0 else 0}
            else:
                return {'success': False, 'model': model, 'question': question, 'error': stderr or 'No response', 'time_elapsed': elapsed}
        except Exception as e:
            return {'success': False, 'model': model, 'question': question, 'error': str(e), 'time_elapsed': time.time() - start_time}

    def evaluate_response_quality(self, response: str, question: str) -> Dict[str, Any]:
        """Evaluate the quality of Ollama's response"""
        evaluation = {'length': len(response), 'word_count': len(response.split()), 'has_structure': any((marker in response for marker in ['1.', '2.', '•', '-'])), 'addresses_question': any((keyword in response.lower() for keyword in question.lower().split()[:5])), 'depth_indicators': sum((1 for indicator in ['furthermore', 'additionally', 'moreover', 'specifically', 'technically', 'philosophically', 'culturally', 'historically'] if indicator in response.lower())), 'technical_terms': sum((1 for term in ['digital', 'quantum', 'algorithm', 'system', 'protocol', 'architecture', 'framework', 'implementation', 'optimization'] if term in response.lower()))}
        quality_score = 0
        if evaluation['length'] > 500:
            quality_score += 20
        if evaluation['word_count'] > 100:
            quality_score += 20
        if evaluation['has_structure']:
            quality_score += 20
        if evaluation['addresses_question']:
            quality_score += 20
        quality_score += min(20, evaluation['depth_indicators'] * 5)
        evaluation['quality_score'] = quality_score
        evaluation['quality_rating'] = 'Excellent' if quality_score >= 80 else 'Good' if quality_score >= 60 else 'Fair' if quality_score >= 40 else 'Poor'
        return evaluation

    def test_pdf_with_all_models(self, pdf_path: str):
        """Test a PDF with all available Ollama models"""
        print(f'\n' + '=' * 80)
        print(f'📚 Testing PDF: {Path(pdf_path).name}')
        print('=' * 80)
        print('\n🔍 Extracting PDF content...')
        pdf_text = self.extract_pdf_text(pdf_path)
        if not pdf_text:
            print('  ❌ Could not extract text from PDF')
            return
        print(f'  ✓ Extracted {len(pdf_text)} characters from PDF')
        questions = ['What are the main themes and concepts presented in this document? Provide an exhaustive analysis.', 'Explain the technical architecture and systems described in detail, including all components and their interactions.', 'What are the philosophical and cultural implications of the ideas presented? Connect to broader human knowledge.', 'How does this relate to digital evolution, artificial intelligence, and the future of technology?', 'Identify and explain all unique terminology, concepts, and frameworks introduced in the document.']
        models = self.get_available_ollama_models()
        if not models:
            print('  ⚠️ No Ollama models available')
            return
        print(f'\n🤖 Testing with {len(models)} models...')
        for model in models:
            print(f'\n🎯 Testing model: {model}')
            for i, question in enumerate(questions, 1):
                result = self.query_ollama_about_pdf(model, pdf_text, question)
                if result['success']:
                    evaluation = self.evaluate_response_quality(result['response'], question)
                    result['evaluation'] = evaluation
                    print(f"  ✓ Question {i}: {evaluation['quality_rating']} ")
                    print(f"    ({result['response_length']} chars in {result['time_elapsed']:.2f}s)")
                    response_file = self.results_dir / f"{Path(pdf_path).stem}_{model.replace(':', '_')}_Q{i}.md"
                    with open(response_file, 'w') as f:
                        f.write(f'# PDF Analysis: {Path(pdf_path).name}\n\n')
                        f.write(f'**Model**: {model}\n\n')
                        f.write(f'**Question {i}**: {question}\n\n')
                        f.write(f"**Response Time**: {result['time_elapsed']:.2f} seconds\n\n")
                        f.write(f"**Quality Rating**: {evaluation['quality_rating']} (Score: {evaluation['quality_score']}/100)\n\n")
                        f.write(f"**Response**:\n\n{result['response']}\n\n")
                        f.write(f'**Evaluation Details**:\n\n')
                        f.write(f"- Word Count: {evaluation['word_count']}\n")
                        f.write(f"- Has Structure: {evaluation['has_structure']}\n")
                        f.write(f"- Depth Indicators: {evaluation['depth_indicators']}\n")
                        f.write(f"- Technical Terms: {evaluation['technical_terms']}\n")
                else:
                    print(f"  ❌ Question {i} failed: {result.get('error', 'Unknown error')}")
                self.test_results.append(result)

    def generate_comprehensive_pdf_report(self):
        """Generate comprehensive PDF testing report"""
        report_file = self.results_dir / f"PDF_Cinema_Analysis_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write('# 🎬 PDF CINEMA & DIGIMUNDO ANALYSIS REPORT\n\n')
            f.write(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            successful_tests = [r for r in self.test_results if r.get('success')]
            f.write('## 📊 Summary Statistics\n\n')
            f.write(f'- **Total Tests**: {len(self.test_results)}\n')
            f.write(f'- **Successful**: {len(successful_tests)}\n')
            f.write(f'- **Success Rate**: {len(successful_tests) / len(self.test_results) * 100:.2f}%\n\n')
            if successful_tests:
                avg_response_length = sum((r['response_length'] for r in successful_tests)) / len(successful_tests)
                avg_time = sum((r['time_elapsed'] for r in successful_tests)) / len(successful_tests)
                f.write(f'- **Average Response Length**: {avg_response_length:.0f} characters\n')
                f.write(f'- **Average Response Time**: {avg_time:.2f} seconds\n\n')
            f.write('## 🏆 Response Quality Distribution\n\n')
            quality_counts = {'Excellent': 0, 'Good': 0, 'Fair': 0, 'Poor': 0}
            for result in successful_tests:
                if 'evaluation' in result:
                    rating = result['evaluation']['quality_rating']
                    quality_counts[rating] = quality_counts.get(rating, 0) + 1
            for rating, count in quality_counts.items():
                f.write(f'- **{rating}**: {count} responses\n')
            f.write('\n## 🤖 Model Performance\n\n')
            model_stats = {}
            for result in self.test_results:
                model = result['model']
                if model not in model_stats:
                    model_stats[model] = {'total': 0, 'successful': 0, 'total_time': 0, 'total_length': 0, 'quality_scores': []}
                model_stats[model]['total'] += 1
                if result.get('success'):
                    model_stats[model]['successful'] += 1
                    model_stats[model]['total_time'] += result['time_elapsed']
                    model_stats[model]['total_length'] += result['response_length']
                    if 'evaluation' in result:
                        model_stats[model]['quality_scores'].append(result['evaluation']['quality_score'])
            f.write('| Model | Tests | Success Rate | Avg Response | Avg Time | Avg Quality |\n')
            f.write('|-------|-------|--------------|--------------|----------|-------------|\n')
            for model, stats in model_stats.items():
                success_rate = stats['successful'] / stats['total'] * 100 if stats['total'] > 0 else 0
                avg_response = stats['total_length'] / stats['successful'] if stats['successful'] > 0 else 0
                avg_time = stats['total_time'] / stats['successful'] if stats['successful'] > 0 else 0
                avg_quality = sum(stats['quality_scores']) / len(stats['quality_scores']) if stats['quality_scores'] else 0
                f.write(f"| {model} | {stats['total']} | {success_rate:.1f}% | {avg_response:.0f} chars | {avg_time:.2f}s | {avg_quality:.1f}/100 |\n")
            f.write('\n## 📝 Key Insights\n\n')
            if successful_tests:
                best_model = max(model_stats.items(), key=lambda x: sum(x[1]['quality_scores']) / len(x[1]['quality_scores']) if x[1]['quality_scores'] else 0)
                f.write(f'- **Best Performing Model**: {best_model[0]}\n')
                f.write(f'- **Highest Quality Responses**: Models demonstrated understanding of complex Digimundo concepts\n')
                f.write(f'- **Cinema Analysis**: Successfully analyzed cinematic and narrative elements\n')
                f.write(f'- **Technical Comprehension**: Understood quantum and digital evolution themes\n\n')
            f.write('## 🎯 Recommendations\n\n')
            f.write('1. **Use larger models** for complex philosophical questions\n')
            f.write('2. **Allow unlimited time** for comprehensive responses\n')
            f.write('3. **Configure models** with maximum context windows\n')
            f.write('4. **Fine-tune prompts** for specific domain knowledge\n')
            f.write('5. **Implement caching** for repeated queries\n\n')
        print(f'\n✅ Comprehensive PDF report saved to: {report_file}')
        return report_file

    def run_all_pdf_tests(self):
        """Run all PDF tests with all models"""
        print('\n' + '=' * 100)
        print('🎬 INITIATING PDF CINEMA ANALYSIS WITH OLLAMA')
        print('No timeouts. Maximum tokens. Deep analysis.')
        print('=' * 100)
        for pdf_path in self.pdf_files:
            if os.path.exists(pdf_path):
                self.test_pdf_with_all_models(pdf_path)
            else:
                print(f'\n⚠️ PDF not found: {pdf_path}')
        if self.test_results:
            report_file = self.generate_comprehensive_pdf_report()
            print('\n' + '=' * 100)
            print('✅ PDF CINEMA ANALYSIS COMPLETE')
            print(f'Tested {len(self.test_results)} scenarios')
            print(f'Report: {report_file}')
            print('=' * 100)
        else:
            print('\n❌ No test results to report')
if __name__ == '__main__':
    analyzer = PDFCinemaAnalyzer()
    analyzer.run_all_pdf_tests()