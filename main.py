import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

# 🔴 آدرس کامل وب‌هوک ربات خود در هاگینگ فیس را اینجا قرار دهید
HF_SPACE_WEBHOOK_URL = (
    "https://YOUR_HF_USERNAME-YOUR_SPACE_NAME.hf.space/YOUR_BOT_ROUTE"
)


@app.post("/")
async def proxy_telegram_to_hf(request: Request):
    # ۱. دریافت دیتای خام از تلگرام
    body = await request.body()

    # ۲. فوروارد کردن به هاگینگ فیس با استفاده از httpx
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                HF_SPACE_WEBHOOK_URL,
                content=body,
                headers={"Content-Type": "application/json"},
                timeout=15.0,
            )
            # ۳. برگرداندن پاسخ هاگینگ فیس به تلگرام
            return Response(
                content=response.content,
                status_code=response.status_code,
                media_type="application/json",
            )
        except httpx.HTTPError as exc:
            return Response(content=f"Error forwarding: {exc}", status_code=500)


@app.get("/")
def home():
    return {"status": "پروکسی رندر فعال است!"}
