from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.api.index import mount_static_files
from src.api.index import router as index_router
from src.api.routes import router as api_router
from src.config.limiter import limiter
from src.config.settings import SETTINGS

app = FastAPI(title="Khair 2048 Backend")

# Initialize Rate Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add CORS allow origins middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.app.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow methods
    allow_headers=["*"],  # allow headers
    expose_headers=[
        "Retry-After",
        "X-RateLimit-Reset",
        "X-RateLimit-Remaining",
        "X-RateLimit-Limit",
    ],
)

# Include the API router with the prefix
app.include_router(api_router, prefix="/api")

# Mount static files
mount_static_files(app)

# Include the index router (for root "/")
app.include_router(index_router)
