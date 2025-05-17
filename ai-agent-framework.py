'''
Documentation, License etc.

@package ai-agent-framework
'''

# ai-agent-framework.py  (or main.py)
from fastapi import FastAPI
from models import Initiative, Task, Agent, Asset, Document
from crud import CRUDRouter
import db  # ensures engine & tables are created

app = FastAPI(title="AI Agent Framework API")

# mount generic CRUD routers
for Model, prefix in [
    (Initiative, "/initiatives"),
    (Task,       "/tasks"),
    (Agent,      "/agents"),
    (Asset,      "/assets"),
    (Document,   "/documents"),
]:
    router = CRUDRouter(Model, prefix).router
    app.include_router(router)

# optional landing page
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "AI Agent Framework API is up—visit /docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ai-agent-framework:app", host="127.0.0.1", port=8000, reload=True)
