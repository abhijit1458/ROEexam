# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi[standard]",
#   "uvicorn",
#   "httpx",
# ]
# ///

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
import httpx



app = FastAPI()

# Enable CORS for all origins (Allows any frontend to access this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api")
async def proxy(url: str):
    """
    Proxy endpoint that fetches data from the provided URL.
    The response will include CORS headers allowing access from any origin.
    """
    try:
        async with httpx.AsyncClient() as client:
            target_response = await client.get(url)
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e}") from e

    # Return the target response content and status.
    # The CORSMiddleware automatically adds the required CORS headers.
    return Response(
        content=target_response.content,
        status_code=target_response.status_code,
        headers=dict(target_response.headers),
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)