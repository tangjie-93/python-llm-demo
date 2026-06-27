from app.models.response import ApiResponse


def success_response(data=None, message="操作成功"):
    """
    成功响应
    
    Args:
        data: 返回数据
        message: 提示信息
    
    Returns:
        ApiResponse: 统一格式的成功响应
    """
    return ApiResponse(success=True, message=message, data=data)


def error_response(message="操作失败", **kwargs):
    """
    错误响应
    
    Args:
        message: 错误提示信息
        **kwargs: 额外参数（如 error 类型等），会被忽略，仅为兼容现有调用
    
    Returns:
        ApiResponse: 统一格式的错误响应
    """
    return ApiResponse(success=False, message=message, data=None)
