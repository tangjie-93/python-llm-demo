from typing import Generic, Optional, TypeVar, Any
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一 API 响应模型
    
    Attributes:
        code: HTTP 状态码
        msg: 用户提示信息
        data: 返回数据，类型根据具体接口确定
    """
    code: int
    msg: str
    data: Optional[T] = None
