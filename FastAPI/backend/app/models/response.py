from typing import Generic, Optional, TypeVar, Any
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一 API 响应模型
    
    Attributes:
        success: 操作是否成功
        message: 用户提示信息
        data: 返回数据，类型根据具体接口确定
        error: 错误类型（可选）
        details: 详细信息（可选）
    """
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None
    details: Optional[Any] = None
