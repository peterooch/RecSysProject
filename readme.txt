Recommender system project

Authors:
    Roi Amzallag
    Evghenii Gaisinschii
    Baruch Rutman

Requirements:
    Backend:
        Python enviroment:
            Python 3.8 or above
        Python packages (as listed in `requirements.txt`):
            lightfm (requires c++ compiler to be installed)
            fastapi
            uvicorn
            joblib
            numpy
            pandas
        All packages (and their dependecies) can be installed using:
            ```
            pip install -r requirements.txt
            ```
    Frontend:
        JavaScript/TypeScript enviroment:
            NodeJS 16.14 or above
        JavaScript/TypeScript packages (primary packages used, all are listed in `client/package.json`):
            ReactJS
            MUI
            Axios
            TypeScript
        All packages (and their dependecies) can be installed using:
            ```
            cd client
            npm install
            ```
Backend can be run by either:
    Executing `main.py`
    Using the following command:
        `python -m uvicorn server.api:app` on Windows
        `python3 -m uvicorn server.api:app` on Unix-based systems (Linux, OS X)

Frontend can be run by:
    Using the command:
        `cd client && npm start`
    Or can be built into a static/deployable build using:
        `cd client && npm run build`
        The build then can be found in the `client/build` directory.

    Posters links are via the TheMovieDB API, which requires getting an api key.
