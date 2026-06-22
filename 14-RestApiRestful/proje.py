from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    description: str
    price: float

# Create a fake database to store the products
products_db = []

@app.get("/products/")
async def read_products():
    return {"products": products_db}

@app.post("/products/")
async def create_product(product: Product):
    product_dict = product.dict()
    products_db.append(product_dict)
    return {"product": product_dict}

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    product_dict = product.dict()
    for i, stored_product in enumerate(products_db):
        if i == product_id:
            products_db[i] = product_dict
            return {"product": product_dict}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    for i, product in enumerate(products_db):
        if i == product_id:
            del products_db[i]
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
@app.get("/products/{product_id}")
async def read_product(product_id: int):
    for i, product in enumerate(products_db):
        if i == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")