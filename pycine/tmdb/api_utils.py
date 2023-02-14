import requests
from tmdb.models import TMDBMovie, Genre
import json
from service import Service

key = 'd1da20fbfa65312b857fb7b517bf855c'


class RequestApi:
    """

    Esta classe faz request para a API do tmdb,
    de acordo com funções pre-definidas do nosso app

    """
    @staticmethod
    def test():
        print('[ok] from RequestApi')

    @staticmethod
    def get_movie_popular_by_genre(genre: int):
        endpoint = f'https://api.themoviedb.org/3/discover/movie/?api_key={key}&certification_country=US&certification=R&sort_by=vote_count.desc&with_genres={genre}'
        r = requests.get(endpoint)
        # print(r.status_code) # deve retornar 200
        data = r.json()
        results = data['results']
        return results

    # nome do artista: "Arnold Schwarzenegger"
    # def get_artista_by_name(name)
    #     endpoint: search_person

    @staticmethod
    def get_artista(person_id):
        endpoint = f'https://api.themoviedb.org/3/person/{person_id}?api_key={key}'
        r = requests.get(endpoint)
        data = r.json()
        results = data
        return results

    @staticmethod
    def get_filmes_artista(person_id):
        endpoint = f'https://api.themoviedb.org/3/discover/movie/?api_key={key}&certification_country=US&certification=R&sort_by=vote_count.desc&with_cast={person_id}'
        r = requests.get(endpoint)
        data = r.json()
        results = data['results']
        return results


    @staticmethod
    def get_artista_by_name(name):
        # Cria-ser uma variável "endpoint" que é uma string contendo a URL
        # para a API do MovieDB, que é construída com a string de formato para incluir 
        # o valor da variável key (chave da API) e o valor da 
        # string name passada como argumento.
        endpoint = f'https://api.themoviedb.org/3/search/person?api_key={key}&query={name}'
        # Em seguida, é feita uma solicitação GET para a URL armazenada em endpoint usando
        # o método requests.get(endpoint). A resposta da solicitação é armazenada 
        # na variável r.
        r = requests.get(endpoint)
        # A variável data é então definida como o resultado da chamada ao método json()
        # em r. Isso decodifica a resposta da solicitação da API em formato JSON para
        # um dicionário em Python.
        data = r.json()
        # A variável results é definida como o ID da primeira pessoa 
        # retornada pela busca, acessando a lista de resultados em 
        # data e o ID da primeira pessoa na lista.
        results = data['results'][0]['id']
        # If que verifica se a lista de resultados não está vazia. Se não estiver vazia, a variável results é redefinida como o ID da primeira pessoa retornada.
        if data['results'] != []:
            results = data['results'][0]['id']
            # Então, uma nova variável endpoint é definida, 
            # desta vez para obter detalhes sobre uma pessoa
            # específica usando o ID armazenado em results.
            endpoint = f'https://api.themoviedb.org/3/person/{results}?api_key={key}'
            # Novamente, uma solicitação GET é feita usando a URL armazenada em  e a resposta é     decodificada em um dicionário em Python e armazenada em data.
            r = requests.get(endpoint)
            # Finalmente, a variável results é redefinida como um dicionário contendo informações sobre a pessoa, incluindo o ID, nome, caminho da imagem de perfil, popularidade, biografia, data de nascimento e local de nascimento. 
            data = r.json()
            results = {'id': data['id'], 'nome': data['name'],
                'imagem': data['profile_path'],
                'popularidade': data['popularity'],
                'biografia': data['biography'], 'birthday': data['birthday'],
                'local_nascimento': data['place_of_birth'], 'popularidade': data['popularity']}
            # Este dicionário é então retornado como resultado do método.    
            return results

class MovieUtils:
    """
    classe utilitaria para ser usada no fastapi
    """
    @staticmethod
    def get_genres(genre_ids):
        genres = Service.get_genres()
        genres_names = [g['name'] for g in genres if g['id'] in genre_ids]
        return " | ".join(genres_names)

    @staticmethod
    def get_image_path(poster_path):
        return f"https://image.tmdb.org/t/p/w185{poster_path}"

    @staticmethod
    def get_movies(genre: int):
        # obter o titulo (original_title)
        # percorremos a lista de filmes (results)
        results = RequestApi.get_movie_popular_by_genre(genre)
        movies = []  # lista que armazena os filmes
        for movie in results:
            m = TMDBMovie(
                movie['id'],
                movie['original_title'],
                genres=MovieUtils.get_genres(
                    movie['genre_ids']
                ),
                poster_path=MovieUtils.get_image_path(
                    movie['poster_path']
                )
            )
            movies.append(m)
            # title = movie['original_title']
            # print(m.title, m.id)
        # print(f'Filmes encontrados: {len(results)}')
        return movies
