# Arquivo de teste para Claude Code
print("Hello World!")

def calcular_fibonacci(n):
    """Função simples para testar o Claude Code"""
    if n <= 1:
        return n
    return calcular_fibonacci(n-1) + calcular_fibonacci(n-2)

# TODO: Otimizar esta função usando programação dinâmica
if __name__ == "__main__":
    print(f"Fibonacci(10) = {calcular_fibonacci(10)}")
