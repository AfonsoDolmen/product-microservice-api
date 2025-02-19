from fastapi import FastAPI, status
from app.routes.category_routes import router as categories_routes
from app.routes.product_routes import router as products_routes
from app.routes.user_routes import router as user_router

app = FastAPI(
    title='Gerenciamento de Produto',
    description='API para gerenciamento de produtos e categorias.',
    version='0.0.1',
    docs_url='/api/docs'
)

# Rotas
app.include_router(categories_routes, prefix='/api/v1')
app.include_router(products_routes, prefix='/api/v1')
app.include_router(user_router)


@app.get('/health-check', status_code=status.HTTP_200_OK, description='Status da API', tags=['Health Check'])
def health_check():
    """
    Verifica o status da API
    """
    return True


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app')
