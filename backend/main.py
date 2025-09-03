from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from backend.bot import run_bot, get_validated_articles

app = FastAPI(title="En Pôle Position API")

# Serve React build
app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")

@app.get("/validated")
async def validated_articles():
    try:
        articles = get_validated_articles()
        return JSONResponse(content=articles)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.on_event("startup")
async def startup_event():
    import threading
    threading.Thread(target=run_bot, daemon=True).start()
