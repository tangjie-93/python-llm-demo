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


def error_response(message="操作失败", error=None, details=None):
    """
    错误响应
    
    Args:
        message: 错误提示信息
        error: 错误类型
        details: 详细信息
    
    Returns:
        ApiResponse: 统一格式的错误响应
    """
    return ApiResponse(success=False, message=message, error=error, details=details, data=None)
