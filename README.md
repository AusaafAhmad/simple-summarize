# simple-summarize

## Quickstart
 
**1. Clone the repo**
```bash
git clone https://github.com/AusaafAhmad/simple-summarize.git
cd simple-summarize
```
 
**2. Create and activate a virtual environment**
```bash
python -m venv venv
 
# Linux / macOS
source venv/bin/activate
 
# Windows
venv\Scripts\activate
```
 
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
 
---

Start the Flask server:
```bash
python app.py
```

> then open the html file directly or preferably through live server

### CLI
 
Summarize a file:
```bash
python summarizer.py article.txt
```
 
Control the number of sentences:
```bash
python summarizer.py article.txt --sentences 5
```
 
Print token stats alongside the summary:
```bash
python summarizer.py article.txt --stats
```
 
Read from stdin (pipe):
```bash
cat article.txt | python summarizer.py -
```

 ---
 
## API
 
The server exposes two endpoints.
 
### `POST /api/summarize`
 
**Request body:**
```json
{
  "text": "Your article text here...",
  "n_sentences": 3
}
```
 
**Response:**
```json
{
  "summary": "Extracted summary text.",
  "stats": {
    "original_tokens": 215,
    "summary_tokens": 80,
    "tokens_removed": 135,
    "kept_pct": 37.2,
    "removed_pct": 62.8,
    "compression_ratio": 2.69
  }
}
```
 
### `GET /api/health`
 
Returns `{ "status": "ok" }` — useful for checking the server is running.
 
---
