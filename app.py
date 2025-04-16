from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/certidao/cnpj/<cnpj>', methods=['GET'])
def consultar_certidao(cnpj):
    try:
        url = f"https://certidoes-apf.apps.tcu.gov.br/api/certidao/cnpj/{cnpj}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({"erro": "CNPJ não encontrado"}), 404
        elif response.status_code == 401:
            return jsonify({"erro": "Não autorizado. A API recusou a chamada."}), 401
        else:
            return jsonify({"erro": f"Erro inesperado: {response.status_code}"}), response.status_code

    except Exception as e:
        return jsonify({"erro": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
