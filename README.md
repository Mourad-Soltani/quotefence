# QuoteFence

Signature: **Mourad.Soltani**

Micro-SaaS for independent consultants and boutique agencies.

Paste a messy client brief. QuoteFence returns a fenced quote:

- included work extracted from the brief
- default exclusions that stop scope creep
- assumptions and a change-order clause
- risk flags for phrases like `unlimited`, `ASAP`, `etc.`, `make it pop`
- a 1–100 risk score
- copy-ready Markdown

No LLM key is required. Rules run locally so a solo operator can ship on a $5 VPS.

## Why this exists

2026 micro-SaaS lists keep pointing at vertical workflow tools with a reachable buyer. Freelancers already lose margin to vague briefs. Existing GitHub repos are either construction-fence estimators, giant AI SOW platforms, or prompt libraries. QuoteFence is a single-purpose API plus engine.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. uvicorn quotefence.app:app --reload --port 8080
```

Health:

```bash
curl -s http://127.0.0.1:8080/health
```

Fence a brief:

```bash
curl -s http://127.0.0.1:8080/v1/fence \
  -H 'content-type: application/json' \
  -d '{"title":"Site rebuild","validity_days":14,"brief":"Rebuild the marketing site with unlimited revisions and ship ASAP."}'
```

## Tests

```bash
PYTHONPATH=. pytest -q
```

## Product shape (v0)

| Surface | Status |
| --- | --- |
| `GET /health` | shipped |
| `POST /v1/fence` | shipped |
| Rule engine | shipped |
| Auth / Stripe | next |
| Hosted UI | next |

Suggested price test: $19 / month for 200 fences, or $9 one-off packs.

## Author

Mourad.Soltani
