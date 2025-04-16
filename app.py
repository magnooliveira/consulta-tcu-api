from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/certidao/cnpj/<cnpj>', methods=['GET'])
def consultar_certidao(cnpj):
    try:
        url = f"https://certidoes-apf.apps.tcu.gov.br/api/certidao/cnpj/{cnpj}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://certidoes-apf.apps.tcu.gov.br/",
            "Origin": "https://certidoes-apf.apps.tcu.gov.br",
            "Connection": "keep-alive"
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
