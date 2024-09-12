import os
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.base import api_router
from core.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


async def main():
    config = uvicorn.Config("main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
    server = uvicorn.Server(config)
    
    # Run uvicorn within asyncio's event loop
    await server.serve()


if __name__ == "__main__":
    # Check if running locally or in a server environment
    if os.getenv('VERCEL_ENV') is None:
        # Run the asyncio main function
        asyncio.run(main())
