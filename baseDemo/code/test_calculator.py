#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试重构后的计算器工具
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_demo import safe_eval, Agent


def test_basic_operations():
    """测试基本四则运算"""
    print("测试基本四则运算...")
    test_cases = [
        ("2+3", 5),
        ("10-5", 5),
        ("4*6", 24),
        ("15/3", 5),
        ("10%3", 1),
        ("2**3", 8),
    ]
    
    for expression, expected in test_cases:
        try:
            result = safe_eval(expression)
            status = "✓" if result == expected else "✗"
            print(f"{status} {expression} = {result} (预期: {expected})")
        except Exception as e:
            print(f"✗ {expression} 错误: {e}")
    print()


def test_complex_expressions():
    """测试复杂表达式"""
    print("测试复杂表达式...")
    test_cases = [
        ("(2+3)*(4-1)", 15),
        ("10+20/5-3", 11),
        ("(5+3)*(10-2)/4", 16),
        ("1+2*3-4/2", 5),
    ]
    
    for expression, expected in test_cases:
        try:
            result = safe_eval(expression)
            status = "✓" if result == expected else "✗"
            print(f"{status} {expression} = {result} (预期: {expected})")
        except Exception as e:
            print(f"✗ {expression} 错误: {e}")
    print()


def test_unary_operations():
    """测试一元运算"""
    print("测试一元运算...")
    test_cases = [
        ("-5+3", -2),
        ("+10-2", 8),
        ("-(-5)", 5),
        ("-10*2", -20),
    ]
    
    for expression, expected in test_cases:
        try:
            result = safe_eval(expression)
            status = "✓" if result == expected else "✗"
            print(f"{status} {expression} = {result} (预期: {expected})")
        except Exception as e:
            print(f"✗ {expression} 错误: {e}")
    print()


def test_float_operations():
    """测试浮点数运算"""
    print("测试浮点数运算...")
    test_cases = [
        ("3.14*2", 6.28),
        ("10.5/2.5", 4.2),
        ("0.1+0.2", 0.3),
        ("2.5*3.5", 8.75),
    ]
    
    for expression, expected in test_cases:
        try:
            result = safe_eval(expression)
            # 浮点数比较允许一定误差
            status = "✓" if abs(result - expected) < 0.0001 else "✗"
            print(f"{status} {expression} = {result} (预期: {expected})")
        except Exception as e:
            print(f"✗ {expression} 错误: {e}")
    print()


def test_error_cases():
    """测试错误情况"""
    print("测试错误情况...")
    test_cases = [
        "2++3",  # 语法错误
        "(2+3",  # 括号不匹配
        "2+3)",  # 括号不匹配
        "10/0",  # 除零错误
        "2+x",   # 非法字符
        "print(1)",  # 函数调用
        "__import__('os').system('ls')",  # 代码注入
    ]
    
    for expression in test_cases:
        try:
            result = safe_eval(expression)
            print(f"✗ {expression} 应该失败但返回了: {result}")
        except ValueError as e:
            print(f"✓ {expression} 正确失败: {e}")
        except Exception as e:
            print(f"? {expression} 意外错误: {e}")
    print()


def test_agent_integration():
    """测试与Agent的集成"""
    print("测试与Agent的集成...")
    agent = Agent()
    test_cases = [
        "2+3",
        "10-5",
        "4*6",
        "15/3",
        "(2+3)*(4-1)",
        "10/0",
        "2+x",
    ]
    
    for expression in test_cases:
        result = agent._calculator(expression)
        print(f"{expression} → {result}")
    print()


if __name__ == "__main__":
    print("开始测试重构后的计算器工具...\n")
    
    test_basic_operations()
    test_complex_expressions()
    test_unary_operations()
    test_float_operations()
    test_error_cases()
    test_agent_integration()
    
    print("测试完成！")
