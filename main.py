import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

TELEGRAM_API_URL = "https://api.telegram.org"


@app.api_route("/{path:path}", methods=["GET", "POST"])
async def proxy_to_telegram(request: Request, path: str):
    url = f"{TELEGRAM_API_URL}/{path}"
    body = await request.body()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=url,
                content=body,
                params=request.query_params,
                headers={
                    "Content-Type": request.headers.get(
                        "content-type", "application/json"
                    )
                },
                timeout=60.0,
            )
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type=response.headers.get("content-type", "application/json"),
            )
        except Exception as exc:
            return Response(content=str(exc), status_code=500)
