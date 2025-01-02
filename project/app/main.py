import logging

from api.endpoints import router
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

# ログ設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)


# カスタムHTTPエラーハンドラー
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred: {exc.detail} (status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "path": request.url.path,
        },
    )


# カスタム汎用エラーハンドラー
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logger.error("Unexpected error occurred", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred.",
            "error": repr(exc),  # reprを使用してオブジェクトの完全な情報を取得
            "path": request.url.path,
        },
    )
