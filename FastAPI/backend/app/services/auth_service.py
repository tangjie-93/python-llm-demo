"""
认证服务模块

提供认证相关的业务逻辑服务，包括：
- 登录失败追踪和限流
- 密码强度验证
- 用户认证业务逻辑
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import threading

from collections import defaultdict


class LoginAttemptTracker:
    """
    登录失败追踪器
    
    用于记录每个用户的登录失败次数，防止暴力破解。
    使用内存存储，生产环境建议使用 Redis。
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.failed_attempts: Dict[str, list] = defaultdict(list)
        self.max_attempts = 5  # 最大失败次数
        self.lockout_duration = timedelta(hours=1)  # 锁定时长
    
    def record_failed_attempt(self, username: str) -> None:
        """记录一次失败尝试"""
        with self._lock:
            now = datetime.now(timezone.utc)
            self.failed_attempts[username].append(now)
            # 清理 1 小时前的记录
            cutoff = now - timedelta(hours=1)
            self.failed_attempts[username] = [
                t for t in self.failed_attempts[username] if t > cutoff
            ]
    
    def get_failed_count(self, username: str) -> int:
        """获取当前失败次数"""
        with self._lock:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
            recent_attempts = [
                t for t in self.failed_attempts[username] if t > cutoff
            ]
            return len(recent_attempts)
    
    def is_locked_out(self, username: str) -> tuple[bool, Optional[int]]:
        """
        检查是否被锁定
        
        Returns:
            tuple[bool, Optional[int]]: (是否锁定，剩余锁定时间（分钟）)
        """
        with self._lock:
            cutoff = datetime.now(timezone.utc) - timedelta(hours=1)
            recent_attempts = [
                t for t in self.failed_attempts[username] if t > cutoff
            ]
            # 计算最近 1 小时内的失败次数
            failed_count = len(recent_attempts)
            
            if failed_count >= self.max_attempts:
                # 计算最早失败时间
                if self.failed_attempts[username]:
                    earliest = min(self.failed_attempts[username])
                    now = datetime.now(timezone.utc)
                    remaining = self.lockout_duration - (now - earliest)
                    
                    if remaining.total_seconds() > 0:
                        return True, int(remaining.total_seconds() / 60)
                
                # 锁定时间已过，重置计数
                self.failed_attempts[username] = []
            
            return False, None
    
    def reset_failed_attempts(self, username: str) -> None:
        """重置失败计数（登录成功后调用）"""
        with self._lock:
            self.failed_attempts[username] = []


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    验证密码强度

    密码必须满足：
    - 至少 8 位
    - 包含大小写字母
    - 包含数字

    Args:
        password: 待验证的密码

    Returns:
        tuple[bool, str]: (是否通过，错误消息)
    """
    if len(password) < 8:
        return False, "密码长度至少为 8 位"
    
    if not re.search(r'[a-z]', password):
        return False, "密码必须包含小写字母"
    
    if not re.search(r'[A-Z]', password):
        return False, "密码必须包含大写字母"
    
    if not re.search(r'\d', password):
        return False, "密码必须包含数字"
    
    return True, ""


def validate_username(username: str) -> bool:
    """
    验证用户名格式
    
    用户名必须为 4-32 位字母、数字或下划线

    Args:
        username: 待验证的用户名

    Returns:
        bool: 验证是否通过
    """
    return bool(re.match(r'^[a-zA-Z0-9_]{4,32}$', username))


def validate_email(email: str) -> bool:
    """
    验证邮箱格式

    Args:
        email: 待验证的邮箱地址

    Returns:
        bool: 验证是否通过
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


# 全局登录失败追踪器实例
login_tracker = LoginAttemptTracker()
