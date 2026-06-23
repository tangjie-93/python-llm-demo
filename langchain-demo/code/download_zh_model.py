#!/usr/bin/env python3
"""
下载中文嵌入模型 BAAI/bge-small-zh-v1.5
"""
import os
import time
from huggingface_hub import snapshot_download

def download_model_hf(model_name, local_model_path, max_retries=5):
    """
    使用 huggingface_hub 下载模型，支持重试机制
    
    Args:
        model_name: 模型名称
        local_model_path: 本地保存路径
        max_retries: 最大重试次数
    
    Returns:
        本地模型路径
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"开始下载模型: {model_name}")
            print(f"保存路径: {local_model_path}")
            
            # 确保保存目录存在
            os.makedirs(local_model_path, exist_ok=True)
            
            # 下载模型
            snapshot_download(
                repo_id=model_name,
                local_dir=local_model_path,
                local_dir_use_symlinks=False,
                resume_download=True,
                max_workers=4
            )
            
            print(f"模型下载完成: {model_name}")
            print(f"本地模型路径: {local_model_path}")
            return local_model_path
        except Exception as e:
            retry_count += 1
            print(f"下载失败 (尝试 {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                wait_time = 2 ** retry_count  # 指数退避
                print(f"{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print("达到最大重试次数，下载失败")
                raise

if __name__ == "__main__":
    # 中文嵌入模型
    model_name = "BAAI/bge-small-zh-v1.5"
    local_model_path = "./local_models/bge-small-zh-v1.5"
    
    # 检查模型是否已存在
    if os.path.exists(local_model_path) and os.listdir(local_model_path):
        print(f"模型已存在: {local_model_path}")
        print("跳过下载")
    else:
        download_model_hf(model_name, local_model_path)
    
    print("\n=== 下载完成 ===")
