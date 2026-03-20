"""
异常处理模块

该模块负责配置 FastAPI 应用的全局异常处理器。
使用 setup_ 函数模式，将异常处理配置集中管理。

异常处理器 (Exception Handler) 用于捕获应用中未处理的异常，
并返回统一的、格式化的错误响应。

常见的异常类型：
- HTTPException: FastAPI 内置的 HTTP 异常（如 404、401 等）
- RequestValidationError: 请求参数验证失败
- ValidationError: Pydantic 数据验证错误
- Exception: 所有其他未处理的异常（通常返回 500 内部服务器错误）
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from pydantic import ValidationError


def setup_exception_handlers(app: FastAPI):
    """
    配置全局异常处理器

    为不同类型的异常配置专门的处理器，
    确保所有错误都以统一的 JSON 格式返回给前端。

    响应格式：
        {
            "success": false,      # 表示请求失败
            "error": "错误类型",   # 错误类型名称
            "message": "错误消息", # 友好的错误描述
            "details": {...},     # 详细信息（可选）
            "traceback": "..."    # 堆栈跟踪（仅调试模式下显示）
        }

    Args:
        app: FastAPI 应用实例
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        HTTP 异常处理器

        处理 FastAPI 内置的 HTTP 异常（如 404、401、403、500 等）。

        Args:
            request: FastAPI 请求对象
            exc: HTTP 异常对象

        Returns:
            JSONResponse: 标准化的错误响应
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": "HTTP Error",
                "message": exc.detail,
                "status_code": exc.status_code,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常处理器

        处理请求参数不符合 Pydantic 模型定义的情况。
        例如：缺少必填字段、字段类型错误、格式错误等。

        Args:
            request: FastAPI 请求对象
            exc: 验证错误对象

        Returns:
            JSONResponse: 包含详细验证错误信息的响应
        """
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "Validation Error",
                "message": "请求参数验证失败",
                "details": exc.errors(),
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_exception_handler(request: Request, exc: ValidationError):
        """
        Pydantic 验证异常处理器

        处理 Pydantic 数据验证错误。
        通常在程序内部数据处理时触发。

        Args:
            request: FastAPI 请求对象
            exc: Pydantic 验证错误对象

        Returns:
            JSONResponse: 包含详细验证错误信息的响应
        """
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": "Validation Error",
                "message": "数据验证失败",
                "details": exc.errors(),
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """
        通用异常处理器

        处理所有未被其他处理器捕获的异常。
        这是最后一道防线，确保不会有未处理的异常泄漏到客户端。

        Args:
            request: FastAPI 请求对象
            exc: 异常对象

        Returns:
            JSONResponse: 标准化的错误响应

        Note:
            - 生产环境下不会返回详细的错误信息和堆栈跟踪
            - 调试模式下会返回详细信息，便于开发调试
        """
        import traceback
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
                "message": "服务器内部错误",
                # 调试模式下返回详细信息，生产环境只返回通用消息
                "details": str(exc) if app.debug else "请联系管理员",
                # 仅在调试模式下返回堆栈跟踪
                "traceback": traceback.format_exc() if app.debug else None,
            }
        )
