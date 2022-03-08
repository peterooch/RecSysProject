import axios from 'axios';
import { UserList, Movie } from './types';

/* API Server location (powered by FastAPI) */
export const SERVER: string = "http://localhost:8000";
/* TheMovieDB apikey and API location */
const tmdbApiKey: string = process.env.REACT_APP_TMDB_KEY as string; // store this at client/.env
const TMDBApi: string = "https://api.themoviedb.org/3"

export type ApiClient = {
    getUsers: () => Promise<UserList>;
    getMovies: () => Promise<string[]>;
    getRecommendations: (method: string, param: string, n: number) => Promise<Movie[]>;
}

export type TMDBApiClient = {
    getPosterUrl: (movie: Movie) => Promise<string>;
}

export const createApiClient = (): ApiClient => {
    return {
        getUsers: async () => {
            const response = await axios.get(`${SERVER}/users`);
            return response.data;
        },
        getMovies: async () => {
            const response = await axios.get(`${SERVER}/movies`);
            return response.data;
        },
        getRecommendations: async (method: string, param: string, n: number) => {
            const response = await axios.get(`${SERVER}/recommendations/?method=${method}&param=${param}&n_recommends=${n}`);
            return response.data;
        }
    }
}

export const createTMDBApiClient = (): TMDBApiClient => {
    let config: any = undefined;

    axios.get(`${TMDBApi}/configuration?api_key=${tmdbApiKey}`)
         .then(response => {
             config = response.data;
         });
    return {
        getPosterUrl: async (movie: Movie) => {
            if (!config) return ""
            let imdb_id_proper = "tt" + movie.imdb_id.padStart(7, "0");
            return await axios.get(`${TMDBApi}/find/${imdb_id_proper}?api_key=${tmdbApiKey}&external_source=imdb_id`)
                                 .then(response => {
                                     let data = response.data.movie_results[0];
                                     let base_url = config.images.base_url;
                                     return `${base_url}w342${data.poster_path}`;
                                 });
        }
    }
}