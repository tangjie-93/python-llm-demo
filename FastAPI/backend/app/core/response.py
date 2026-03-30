from fastapi import status
from app.models.response import ApiResponse


def success_response(data=None, msg="操作成功", code=status.HTTP_200_OK):
    """
    成功响应
    
    Args:
        data: 返回数据
        msg: 提示信息
        code: HTTP状态码
    
    Returns:
        ApiResponse: 统一格式的成功响应
    """
    return ApiResponse(code=code, msg=msg, data=data)


def error_response(msg="操作失败", code=status.HTTP_400_BAD_REQUEST):
    """
    错误响应
    
    Args:
        msg: 错误提示信息
        code: HTTP状态码
    
    Returns:
        ApiResponse: 统一格式的错误响应
    """
    return ApiResponse(code=code, msg=msg, data=None)
