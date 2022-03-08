import uvicorn

# subsitute for "python -m uvicorn server.api:app"
if __name__ == "__main__":
    uvicorn.run("server.api:app", host="127.0.0.1", port=8000)