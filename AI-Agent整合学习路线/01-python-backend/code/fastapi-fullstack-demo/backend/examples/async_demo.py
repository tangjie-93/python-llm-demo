"""
asyncio + httpx 异步并发示例

前端类比：JavaScript 的 async/await + Promise.all
JS:  Promise.all([fetch(url1), fetch(url2)])
PY:  await asyncio.gather(fetch(url1), fetch(url2))
"""

import asyncio
import time
import httpx


# ====== 示例 1：基础 async/await ======

async def greet(name: str) -> str:
    """异步函数，类比 JS 的 async function"""
    await asyncio.sleep(0.5)  # 类比 JS 的 await new Promise(r => setTimeout(r, 500))
    return f"Hello, {name}!"


async def demo_basic_async():
    """串行执行（慢）"""
    t0 = time.time()
    result1 = await greet("Alice")
    result2 = await greet("Bob")
    elapsed = time.time() - t0
    print(f"[串行] 耗时 {elapsed:.2f}s | {result1}, {result2}")


async def demo_parallel_async():
    """并行执行（快），类比 JS 的 Promise.all"""
    t0 = time.time()
    results = await asyncio.gather(greet("Alice"), greet("Bob"))
    elapsed = time.time() - t0
    print(f"[并行] 耗时 {elapsed:.2f}s | {', '.join(results)}")


# ====== 示例 2：httpx 异步 HTTP 客户端 ======

API_URLS = [
    "https://httpbin.org/delay/0.5",
    "https://httpbin.org/delay/0.3",
    "https://httpbin.org/delay/0.4",
]

async def fetch_url(client: httpx.AsyncClient, url: str) -> dict:
    """异步请求单个 URL，类比 JS 的 fetch()"""
    start = time.time()
    response = await client.get(url)
    return {
        "url": url,
        "status": response.status_code,
        "elapsed": time.time() - start,
    }


async def demo_sequential_requests():
    """串行请求 3 个 API"""
    t0 = time.time()
    async with httpx.AsyncClient(timeout=10.0) as client:
        for url in API_URLS:
            result = await fetch_url(client, url)
            print(f"  串行: {url} -> {result['status']} ({result['elapsed']:.2f}s)")
    print(f"[串行请求] 总耗时 {time.time() - t0:.2f}s\n")


async def demo_concurrent_requests():
    """并发请求 3 个 API，类比 JS 的 Promise.all"""
    t0 = time.time()
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [fetch_url(client, url) for url in API_URLS]
        results = await asyncio.gather(*tasks)
        for r in results:
            print(f"  并发: {r['url']} -> {r['status']} ({r['elapsed']:.2f}s)")
    print(f"[并发请求] 总耗时 {time.time() - t0:.2f}s\n")


# ====== 示例 3：超时 + 重试 ======

async def fetch_with_retry(
    client: httpx.AsyncClient,
    url: str,
    max_retries: int = 3,
    timeout: float = 5.0,
) -> httpx.Response:
    """带超时和重试的请求"""
    for attempt in range(max_retries):
        try:
            return await client.get(url, timeout=timeout)
        except httpx.TimeoutException:
            if attempt == max_retries - 1:
                raise
            wait = 2 ** attempt  # 指数退避: 1s, 2s, 4s
            print(f"  请求超时，{wait}s 后重试... (第 {attempt + 1} 次)")
            await asyncio.sleep(wait)
    raise RuntimeError("unreachable")


async def demo_retry():
    """演示重试机制"""
    async with httpx.AsyncClient() as client:
        try:
            result = await fetch_with_retry(client, "https://httpbin.org/delay/3", timeout=1.0)
            print(f"  重试成功: {result.status_code}")
        except httpx.TimeoutException:
            print("  所有重试均失败")


# ====== 示例 4：信号量控制并发数 ======

async def rate_limited_fetch(urls: list[str], max_concurrent: int = 2):
    """用信号量控制并发数，避免打爆服务端"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def bounded_fetch(client: httpx.AsyncClient, url: str):
        async with semaphore:
            return await fetch_url(client, url)

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [bounded_fetch(client, url) for url in urls]
        return await asyncio.gather(*tasks)


async def demo_rate_limit():
    """演示并发限制"""
    test_urls = [
        "https://httpbin.org/delay/0.3",
        "https://httpbin.org/delay/0.3",
        "https://httpbin.org/delay/0.3",
        "https://httpbin.org/delay/0.3",
    ]
    t0 = time.time()
    results = await rate_limited_fetch(test_urls, max_concurrent=2)
    print(f"[并发限制 2] 4 个请求总耗时 {time.time() - t0:.2f}s")


# ====== 运行所有示例 ======

async def main():
    print("=== 示例 1: 基础 async/await ===")
    await demo_basic_async()
    await demo_parallel_async()

    print("\n=== 示例 2: httpx 异步并发 ===")
    await demo_sequential_requests()
    await demo_concurrent_requests()

    print("=== 示例 3: 超时重试 ===")
    await demo_retry()

    print("\n=== 示例 4: 信号量并发控制 ===")
    await demo_rate_limit()


if __name__ == "__main__":
    asyncio.run(main())
