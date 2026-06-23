import requests
import json

# 测试获取用户列表
print("测试获取用户列表:")
response = requests.get("http://localhost:8000/api/users")
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# 测试创建用户
print("测试创建用户:")
user_data = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
}
response = requests.post("http://localhost:8000/api/users", json=user_data)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# 测试获取物品列表
print("测试获取物品列表:")
response = requests.get("http://localhost:8000/api/items")
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
print()

# 测试登录
print("测试登录:")
login_data = {
    "username": "testuser",
    "password": "password123"
}
response = requests.post("http://localhost:8000/api/auth/login", data=login_data)
print(f"状态码: {response.status_code}")
print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
