from flask import Flask, request, jsonify, render_template
import rsa

app = Flask(__name__)

@app.route('/')
def menu():
    return render_template('index.html')

@app.route('/criptografar')
def pagina_criptografar():
    return render_template('crypt.html')

@app.route('/decifrar')
def pagina_decifrar():
    return render_template('decrypt.html')

@app.route('/api/crypt', methods=['POST'])
def criptografar_endpoint():
    dados = request.get_json()
    texto = dados.get("texto")
    p = dados.get("p")
    q = dados.get("q")

    if not texto:
        return jsonify({"erro": "Campo 'texto' e obrigatorio"}), 400

    try:
        if not p or not q:
            publica, privada = rsa.gerar_chaves_automatico()
        else:
            p = int(p)
            q = int(q)
            publica, privada = rsa.gerar_chaves(p, q)

        n, e = publica
        d = privada[1]
        textoBase = rsa.criptografar(texto, e, n)

        return jsonify({
            "Chave-pública": f"{e}-{n}",
            "Chave-privada": f"{d}-{n}",
            "texto_criptografado": textoBase
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@app.route('/api/dcrypt', methods=['POST'])
def decifrar_endpoint():
    dados = request.get_json()
    texto_criptografado = dados.get("texto_criptografado")
    d = dados.get("d")
    n = dados.get("n")

    if not all([texto_criptografado, d, n]):
        return jsonify({"erro": "Campos 'texto_criptografado', 'd' e 'n' sao obrigatorios"}), 400

    try:
        d = int(d)
        n = int(n)
        texto_decifrado = rsa.decifrar(texto_criptografado, d, n)
        return jsonify({"texto_decifrado": texto_decifrado})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
