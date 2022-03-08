import React from 'react';
import './App.css';
import {createApiClient, SERVER} from './api';
import { Autocomplete, Button, createFilterOptions, FormControlLabel, Radio, RadioGroup, TextField } from '@mui/material';
import { Movie, UserList } from './types';
import MovieTile from './MovieTile';

const api = createApiClient();

export type AppState = {
    userlist?: UserList,
    movielist?: string[],
    selecteduser: Number,
    recommendations?: Movie[],
    method: string,
    param: string
};

export class App extends React.Component<{}, AppState> {

    state: AppState = {
        userlist: undefined,
        selecteduser: 0,
        method: "userid",
        param: ""
    }

    async componentDidMount() {
        this.updateUserList();
        this.updateMovieList();
    }

    async updateMovieList() {
        let list = await api.getMovies();
        this.setState({
            movielist: list
        });
    }

    async updateUserList() {
        let list = await api.getUsers();
        this.setState({
            userlist: list
        });
    }

    async getRecommendations() {
        /* this may be redundant with the autocomplete */
        if (this.state.method === "userid") {
            if (!this.state.userlist)
                return;
            let userid = parseInt(this.state.param)
            if (!this.state.userlist.users.includes(userid)) {
                alert(`UserID "${userid}" not in user list`);
                return;
            }
        }
        else {
            if (!this.state.movielist)
                return;
            if (!this.state.movielist.includes(this.state.param)) {
                alert(`Movie "${this.state.param}" not in movie list`);
            }
        }

        let rec_list = await api.getRecommendations(this.state.method, this.state.param, 10);
        console.log(rec_list);
        this.setState({
            recommendations: rec_list
        })
    }

    async radioSelect(e: any) {
        this.setState({
            method: (e.target as HTMLInputElement).value,
            param: ""
        });
    }

    async inputChange(e: any, value?: string | null) {
        if (value === null)
            return;

        if (!value)
            value = (e.target as HTMLInputElement).value;

        console.log(value);
        this.setState({
            param: value
        });
    }
    render() {
        return (
            <div>
                <nav>
                    <div className='horizontal'>
                        <RadioGroup row defaultValue="userid" onChange={this.radioSelect.bind(this)}>
                            <FormControlLabel value="userid" control={<Radio />} label="User ID" />
                            <FormControlLabel value="movie" control={<Radio />} label="Movie Title" />
                        </RadioGroup>
                        <Autocomplete
                            id='input-userid'
                            filterOptions={createFilterOptions({matchFrom: 'any', limit: 200})}
                            className={this.state.method === "userid" ? '': 'hidden'}
                            disablePortal
                            options={this.state.userlist?.users.map(uid => uid.toString()) ?? []} 
                            sx={{width: 300}}
                            renderInput={(params) => <TextField {...params} label='User ID' />}
                            onChange={this.inputChange.bind(this)}/>
                        <Autocomplete
                            id='input-movie'
                            filterOptions={createFilterOptions({matchFrom: 'any', limit: 200})}
                            className={this.state.method !== "userid" ? '': 'hidden'}
                            disablePortal
                            options={this.state.movielist ?? []}
                            sx={{width: 500}}
                            renderInput={(params) => <TextField {...params} label='Movie'/>}
                            onChange={this.inputChange.bind(this)} />
                        <Button onClick={() => this.getRecommendations()}>
                            Get Recommendations
                        </Button>
                        <a target='_blank'  rel="noreferrer" href={`${SERVER}/redoc`} id="ApiDoc">Server API Documentation</a>
                    </div>
                </nav>
                <hr/>
                <div className="MovieTiles">
                    {this.state.recommendations ? this.state.recommendations.map(movie => (
                        <MovieTile key={movie.id.toString()} movie={movie} />
                    )): null}
                </div>
            </div>
        );
    }
}
export default App;
