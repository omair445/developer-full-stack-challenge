from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database_config import Base, engine
from app.routes import authentication
from app.routes import book
from app.routes import author
import uvicorn

def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def add_cors_middleware(app: FastAPI):
    """
    Add CORS middleware to the FastAPI app.

    Args:
        app: FastAPI instance
    """
    origins = [
        "http://localhost:3000",  # Local frontend development server
    ]

    # Adding the CORS middleware to the FastAPI app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_routers(app: FastAPI):
    """
    Include routers to the FastAPI app.

    Args:
        app: FastAPI instance
    """

    app.include_router(authentication.router)
    app.include_router(book.router)
    app.include_router(author.router)


# Creating FastAPI app instance
app = FastAPI()

include_routers(app)  # Including routers
# Add CORS middleware before the startup event
add_cors_middleware(app)

# Adding startup event handler
@app.on_event("startup")
async def startup_event():
    """Actions to perform at application startup."""
    create_tables()  # Creating tables
    #include_routers(app)  # Including routers


# Route for root endpoint
@app.get("/")
def read_root():
    """Root endpoint."""
    return {"Hello": "World"}


# Main block to run the app using uvicorn when this script is executed
if __name__ == "__main__":
    # Running FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
