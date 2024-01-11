from flask import jsonify


def test_controller():
    nome = 'jonata'  # Atribua o valor da chave 'nome' a uma variável chamada nome
    return jsonify({
        "nome": "jonatas",  # Use a variável nome
        "code": 200
    }), 200


