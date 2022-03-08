import React from 'react';
import './App.css';
import { Movie } from './types';
import { createTMDBApiClient } from './api';

interface IMovieProps {
    movie: Movie
}
type MovieTileState = {
    poster_url: string
}

const ApiClient = createTMDBApiClient();

const posterCache: Map<number, string> = new Map<number, string>();
export class MovieTile extends React.Component<IMovieProps, MovieTileState> {

    state: MovieTileState = {
        poster_url: ""
    };
    async getPoster() {
        let movieid = this.props.movie.id;

        if (posterCache.has(movieid)) {
            this.setState({ poster_url: posterCache.get(movieid) as string })
        }
        else {
            ApiClient.getPosterUrl(this.props.movie).then(url => {
                posterCache.set(movieid, url);
                this.setState({ poster_url: url })
            });
        }
    }
    render() {
        if (!this.state.poster_url) 
            this.getPoster();
        const movie = this.props.movie;
        
        return (<div className="MovieTile">
                <div className="MovieRect">
                    <a target='_blank'  rel="noreferrer" href={`https://www.imdb.com/title/tt${movie.imdb_id.padStart(7, "0")}`}>
                        {(this.state.poster_url === "" || this.state.poster_url?.includes("null")) ? 
                        <span>No Poster Found</span>
                        :
                        <img className="MovieImg" src={this.state.poster_url} alt={movie.title}/>   
                        }
                    </a>
                </div>
                Title: {movie.title}<br/>
                Genres: {movie.genres.split('|').join(", ")}
        </div>);
    }
};

export default MovieTile;