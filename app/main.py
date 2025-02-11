from fastapi import FastAPI
from app.routes.category_routes import router as categories_routes


app = FastAPI()
app.include_router(categories_routes)


@app.get('/health-check')
def health_check():
    return True


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app')
