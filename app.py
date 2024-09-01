from flask import Flask, render_template, request
import urllib.request, json

app = Flask(__name__)

@app.route('/', methods=["GET"])
def principal():
    filmes_url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-BR&page=1&sort_by=popularity.desc&api_key=8712ef79060d5a6a411a091b11e41d4a"
    series_url = "https://api.themoviedb.org/3/discover/tv?include_adult=false&language=pt-BR&page=1&sort_by=popularity.desc&api_key=8712ef79060d5a6a411a091b11e41d4a"

    filmes_resposta = urllib.request.urlopen(filmes_url)
    series_resposta = urllib.request.urlopen(series_url)

    filmes_dados = filmes_resposta.read()
    series_dados = series_resposta.read()

    filmes_json = json.loads(filmes_dados)
    series_json = json.loads(series_dados)

    # Selecionando os cinco filmes e séries mais populares
    top_filmes = filmes_json['results'][:5]
    top_series = series_json['results'][:5]

    return render_template("index.html", top_filmes=top_filmes, top_series=top_series)

@app.route('/sobre', methods=["GET"])
def sobre():
    descricao_projeto = """
    Este projeto é um aplicativo web desenvolvido usando Flask que se conecta à API do The Movie Database (TMDb) para exibir informações sobre filmes e séries populares. 
    A aplicação possui diferentes rotas que permitem ao usuário visualizar filmes e séries por popularidade e avaliação, e ainda tem uma página inicial que mostra os cinco filmes e séries mais populares.
    """

    descricao_funcionalidades = """
    - **Página Principal**: Exibe os cinco filmes e séries mais populares usando a API do TMDb.
    - **Página de Filmes/Séries**: Exibe listas de filmes ou séries com base em popularidade ou avaliação.
    - **Página Sobre**: Esta página fornece informações sobre o projeto e seu funcionamento.
    """

    return render_template("sobre.html", descricao_projeto=descricao_projeto, descricao_funcionalidades=descricao_funcionalidades)

@app.route('/filmes', methods=["GET"])
@app.route('/filmes/<propriedade>', methods=["GET"])
def filmes(propriedade=None):
    page = request.args.get('page', default=1, type=int)

    if propriedade == 'fpopulares':
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-BR&page={page}&sort_by=popularity.desc&api_key=8712ef79060d5a6a411a091b11e41d4a"
    elif propriedade == 'fvotados':
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=pt-BR&page={page}&sort_by=vote_average.desc&vote_count.gte=200&api_key=8712ef79060d5a6a411a091b11e41d4a"
    elif propriedade == 'spopulares':
        url = f"https://api.themoviedb.org/3/discover/tv?include_adult=false&language=pt-BR&page={page}&sort_by=popularity.desc&api_key=8712ef79060d5a6a411a091b11e41d4a"
    elif propriedade == 'svotadas':
        url = f"https://api.themoviedb.org/3/discover/tv?include_adult=false&language=pt-BR&page={page}&sort_by=vote_average.desc&vote_count.gte=200&api_key=8712ef79060d5a6a411a091b11e41d4a"
    else:
        return "Propriedade não encontrada", 404

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)

    return render_template("filmes.html", filmes=jsondata['results'], page=page, propriedade=propriedade)

@app.route('/detalhes/<tipo>/<int:id>', methods=["GET"])
def detalhes(tipo, id):
    if tipo == 'filme':
        url = f"https://api.themoviedb.org/3/movie/{id}?language=pt-BR&append_to_response=credits,videos&api_key=8712ef79060d5a6a411a091b11e41d4a"
    elif tipo == 'serie':
        url = f"https://api.themoviedb.org/3/tv/{id}?language=pt-BR&append_to_response=credits,videos&api_key=8712ef79060d5a6a411a091b11e41d4a"
    
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    detalhes = json.loads(dados)

    # Buscar o trailer do YouTube
    trailer_url = None
    if 'videos' in detalhes and detalhes['videos']['results']:
        for video in detalhes['videos']['results']:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                break

    return render_template("generico.html", detalhes=detalhes, tipo=tipo, trailer_url=trailer_url)

if __name__ == "__main__":
    app.run(debug=True)
