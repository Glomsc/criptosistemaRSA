import random
import math

def eh_primo(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def inverso_modular(e, z):
    def mdc_estendido(a, b):
        if a == 0:
            return b, 0, 1
        mdc, x1, y1 = mdc_estendido(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return mdc, x, y

    _, d, _ = mdc_estendido(e, z)
    return d % z if d > 0 else d + z

def gerar_primos():
    while True:
        p = random.randint(10, 100)
        q = random.randint(10, 100)
        if eh_primo(p) and eh_primo(q) and p != q:
            return p, q

def gerar_chaves(p, q):
    if not (eh_primo(p) and eh_primo(q) and p != q):
        raise ValueError("p e q devem ser primos diferentes.")
    n = p * q
    z = (p - 1) * (q - 1)
    e = 7
    while math.gcd(e, z) != 1:
        e += 2
        if e >= z:
            raise ValueError("Não foi possível encontrar um e coprimo com z.")
    d = inverso_modular(e, z)
    return (n, e), (n, d)

def gerar_chaves_automatico():
    p, q = gerar_primos()
    n = p * q
    z = (p - 1) * (q - 1)
    e = 7
    while math.gcd(e, z) != 1:
        e += 2
        if e >= z:
            raise ValueError("Não foi possível encontrar um e coprimo com z.")
    d = inverso_modular(e, z)
    return (n, e), (n, d)

def numero_para_base36(numero):
    if numero == 0:
        return '0'
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    resultado = ""
    num = abs(numero)
    while num:
        resultado = chars[num % 36] + resultado
        num //= 36
    return resultado if numero >= 0 else '-' + resultado

def base36_para_numero(texto):
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    resultado = 0
    for char in texto.lower():
        resultado = resultado * 36 + chars.index(char)
    return resultado

def criptografar(texto_claro, e, n):
    numeros_cifrados = [pow(ord(caractere), e, n) for caractere in texto_claro]
    return '-'.join(numero_para_base36(num) for num in numeros_cifrados)

def decifrar(texto_cifrado, d, n):
    numeros = [base36_para_numero(num) for num in texto_cifrado.split('-')]
    return ''.join(chr(pow(num, d, n)) for num in numeros)
