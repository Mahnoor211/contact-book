import uvicorn

if __name__ == "__main__":
    uvicorn.run("routes.base:app", reload=True,)
