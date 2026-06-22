from dataclasses import dataclass


@dataclass
class ToolResult:
    ok: bool
    message: str
    dry_run: bool = True


def read_customer_resource(customer_id: str) -> dict[str, str]:
    return {
        "id": customer_id,
        "name": "示例客户",
        "owner": "sales@example.com",
    }


def update_customer_owner(customer_id: str, owner_email: str, dry_run: bool = True) -> ToolResult:
    if dry_run:
        return ToolResult(
            ok=True,
            message=f"将客户 {customer_id} 的负责人改为 {owner_email}",
            dry_run=True,
        )
    return ToolResult(
        ok=True,
        message=f"已更新客户 {customer_id} 的负责人为 {owner_email}",
        dry_run=False,
    )


def approval_prompt(action: str) -> str:
    return f"请确认是否执行以下高风险操作：{action}"


if __name__ == "__main__":
    customer = read_customer_resource("C-1001")
    result = update_customer_owner(customer["id"], "new-owner@example.com", dry_run=True)
    print(customer)
    print(result)
    print(approval_prompt(result.message))

