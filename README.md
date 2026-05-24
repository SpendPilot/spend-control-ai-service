# Spend Control AI-Service

Standalone AI assistance service for explanations, summaries, receipt post-processing, and chat.

## Run

```powershell
cd c:\Users\lijaz\Desktop\PROJECT2\spend-control-ai-service
py -3.13 -m pip install -e .
$env:DATABASE_URL='postgresql+psycopg://spendcontrol:spendcontrol@localhost:5432/spend_control'
$env:JWT_SECRET_KEY='dev-secret-change-me'
$env:OLLAMA_BASE_URL='http://localhost:11434'
alembic upgrade head
uvicorn app.main:app --reload --port 8002
```

## Test

```powershell
$env:DATABASE_URL='sqlite:///./ai-test.db'
$env:JWT_SECRET_KEY='test-secret'
py -3.13 -m pytest tests
```

