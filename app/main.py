from fastapi import FastAPI


app = FastAPI()


@app.get('/health-check')
def health_check():
    return True


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app')
