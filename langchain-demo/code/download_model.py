#!/usr/bin/env python3
"""
下载嵌入模型到本地目录
"""
import os
import time
import sys
from sentence_transformers import SentenceTransformer

def download_model(model_name, local_model_path, max_retries=3):
    """下载模型到本地目录，支持重试机制
    
    Args:
        model_name: 模型名称
        local_model_path: 本地模型路径
        max_retries: 最大重试次数
    """
    print(f"开始下载模型: {model_name}")
    print(f"下载到: {local_model_path}")
    
    # 确保本地目录存在
    os.makedirs(local_model_path, exist_ok=True)
    
    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"尝试下载 (重试 {retry_count+1}/{max_retries})...")
            # 下载模型
            model = SentenceTransformer(
                model_name,
                cache_folder=os.path.join(local_model_path, ".cache"),
                device="cpu"  # 使用CPU下载，避免GPU内存问题
            )
            
            # 保存到本地
            model.save(local_model_path)
            
            print(f"模型下载完成并保存到: {local_model_path}")
            return local_model_path
        except Exception as e:
            retry_count += 1
            print(f"下载失败: {e}")
            if retry_count < max_retries:
                wait_time = 2 ** retry_count  # 指数退避
                print(f"等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"已达到最大重试次数 ({max_retries})，下载失败！")
                return None

if __name__ == "__main__":
    # 模型信息
    model_name = "BAAI/bge-small-en-v1.5"
    local_model_path = "./local_models/bge-small-en-v1.5"
    
    # 检查本地模型是否已经存在
    if os.path.exists(local_model_path) and os.listdir(local_model_path):
        print(f"本地模型已存在: {local_model_path}")
        print("跳过下载")
    else:
        # 下载模型
        result = download_model(model_name, local_model_path)
        if result:
            print("\n模型下载完成！")
            print(f"您可以在代码中使用本地模型路径: {local_model_path}")
        else:
            print("\n模型下载失败！")
            print("建议手动下载模型并放置到指定目录，或使用默认嵌入。")
            sys.exit(1)
