# RAG MULTI-AGENT API 

## Setup
0. cd ocy

1. create virtual environment

```Terminal
python -m venv env
```

2. Create a `.env` file:

```env
RIVALZ_SECRET_TOKEN=your_secret_token_here
```

3. Install dependencies:

```bash
pip install -r requirements.txt
``` 

4. Run the server

```
uvicorn src.main:app --reload
```













