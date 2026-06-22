from flask import Flask, jsonify, request
import dados
biblioteca = dados.carregar_do_arquivo()
app = Flask(__name__)

@app.route("/biblioteca", methods=["GET","POST"])
@app.route("/biblioteca/<isbn>", methods=["POST","DELETE","PUT"])
def manipula_livro(isbn = None):
    if request.method == "GET":
        if not isbn:
            return jsonify(biblioteca)
        else:
            for livro in biblioteca:
                if livro["isbn"] == isbn:
                    return livro
            return jsonify("Livro não encontrado"), 404
    elif request.method == "POST":
        novo_livro = request.get_json()
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("Livro criado com sucesso"), 201
    elif request.method == "DELETE":
        for livro in biblioteca:
            if livro["isbn"] == isbn:
                biblioteca.remove(livro)
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro deletado com sucesso"), 200
    elif request.method == "PUT":
        novo_livro = request.get_json()
        for livro in biblioteca:
            if livro["isbn"] == isbn:
                for key, value in novo_livro.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("Livro alterado com sucesso")


if __name__ == "__main__":
    app.run()