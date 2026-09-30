# Mourad.Soltani
"""QuoteFence HTTP API."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from quotefence import __version__
from quotefence.engine import fence_quote

app = FastAPI(title="QuoteFence", version=__version__)


class FenceRequest(BaseModel):
    brief: str = Field(..., min_length=8, max_length=8000)
    title: str = Field(default="Untitled engagement", max_length=160)
    validity_days: int = Field(default=14, ge=1, le=90)


class RiskOut(BaseModel):
    code: str
    message: str
    snippet: str


class FenceResponse(BaseModel):
    title: str
    included: list[str]
    excluded: list[str]
    assumptions: list[str]
    validity_days: int
    change_order: str
    risks: list[RiskOut]
    risk_score: int
    markdown: str
    author: str = "Mourad.Soltani"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "quotefence", "author": "Mourad.Soltani"}


@app.post("/v1/fence", response_model=FenceResponse)
def create_fence(payload: FenceRequest) -> FenceResponse:
    try:
        result = fence_quote(
            brief=payload.brief,
            title=payload.title,
            validity_days=payload.validity_days,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return FenceResponse(
        title=result.title,
        included=result.included,
        excluded=result.excluded,
        assumptions=result.assumptions,
        validity_days=result.validity_days,
        change_order=result.change_order,
        risks=[
            RiskOut(code=r.code, message=r.message, snippet=r.snippet)
            for r in result.risks
        ],
        risk_score=result.risk_score,
        markdown=result.to_markdown(),
    )
