---
name: "typescript-coding-standards"
description: "强制执行TypeScript编码规范，包括类型定义、接口、泛型、命名规范和错误处理。当编写或审查TypeScript代码时触发此技能。"
trigger:
  - "*.ts"
  - "*.tsx"
  - "*.vue"
  - "TypeScript编码"
  - "TypeScript规范"
  - "TypeScript审查"
  - "TS类型定义"
  - "TS接口"
  - "TS泛型"
  - "命名规范"
---

# TypeScript编码规范

## 一、命名规范

### 1.1 变量命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 变量 | 小驼峰 (camelCase) | `userName`, `orderList` |
| 常量 | 全大写下划线 | `MAX_LENGTH`, `API_BASE_URL` |
| 布尔值 | is/has/can 开头 | `isActive`, `hasPermission`, `canEdit` |
| 函数 | 动词开头 | `getUser()`, `calculateTotal()` |

### 1.2 类和接口命名

- **类命名**: 大驼峰 (PascalCase)，如 `UserService`, `OrderManager`
- **接口命名**: 大驼峰，可选 `I` 前缀，如 `User` 或 `IUser`
- **私有成员**: `_` 前缀，如 `_privateMethod()`

### 1.3 文件命名

- **通用文件**: 小驼峰，如 `dateUtil.ts`, `httpClient.ts`
- **常量文件**: 大驼峰或全大写，如 `Constants.ts`, `CONFIG.ts`

## 二、类型定义规范

### 2.1 避免使用 `any` 类型

```typescript
// 不好
const data: any = fetchData();

// 好
interface UserData {
    id: string;
    name: string;
    age: number;
}
const data: UserData = fetchData();
```

### 1.2 使用 `unknown` 替代 `any`

```typescript
// 不好
function processValue(value: any) {
    value.toUpperCase();
}

// 好
function processValue(value: unknown) {
    if (typeof value === 'string') {
        value.toUpperCase();
    }
}
```

### 1.3 类型推断优先

```typescript
// 不好
const name: string = 'John';
const age: number = 25;

// 好
const name = 'John';
const age = 25;
```

### 1.4 显式类型注解场景

```typescript
// 函数返回值需要显式注解
function calculateTotal(prices: number[]): number {
    return prices.reduce((sum, price) => sum + price, 0);
}

// 复杂对象需要显式注解
const config: Config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000
};
```

## 二、接口/类型定义

### 2.1 接口命名

```typescript
// 好
interface User {
    id: string;
    name: string;
}

// 或者使用 I 前缀（可选）
interface IUser {
    id: string;
    name: string;
}
```

### 2.2 接口 vs 类型别名

```typescript
// 接口：用于对象类型定义，支持继承
interface User {
    id: string;
    name: string;
}

interface AdminUser extends User {
    role: 'admin';
    permissions: string[];
}

// 类型别名：用于联合类型、交叉类型、工具类型
type Status = 'pending' | 'active' | 'inactive';
type UserWithRole = User & { role: string };
```

### 2.3 可选属性

```typescript
interface User {
    id: string;
    name: string;
    email?: string; // 可选属性
    phone?: string;
}
```

### 2.4 只读属性

```typescript
interface Config {
    readonly apiUrl: string;
    readonly timeout: number;
}
```

## 三、泛型使用规范

### 3.1 泛型函数

```typescript
// 好
function identity<T>(arg: T): T {
    return arg;
}

// 使用示例
const num = identity<number>(42);
const str = identity('hello');
```

### 3.2 泛型约束

```typescript
interface Lengthwise {
    length: number;
}

function logLength<T extends Lengthwise>(arg: T): void {
    console.log(arg.length);
}
```

### 3.3 泛型接口

```typescript
interface ApiResponse<T> {
    code: number;
    message: string;
    data: T;
}

// 使用
const response: ApiResponse<User> = await fetchUser();
```

## 四、函数类型定义

### 4.1 函数参数类型

```typescript
// 好
function greet(name: string, age: number): string {
    return `Hello ${name}, you are ${age} years old`;
}
```

### 4.2 可选参数和默认值

```typescript
function greet(name: string, age?: number, greeting: string = 'Hello'): string {
    if (age) {
        return `${greeting} ${name}, you are ${age} years old`;
    }
    return `${greeting} ${name}`;
}
```

### 4.3 剩余参数

```typescript
function sum(...numbers: number[]): number {
    return numbers.reduce((total, num) => total + num, 0);
}
```

### 4.4 函数类型别名

```typescript
type GreetFunction = (name: string, age?: number) => string;

const greet: GreetFunction = (name, age) => {
    return `Hello ${name}`;
};
```

## 五、联合类型和交叉类型

### 5.1 联合类型

```typescript
type Status = 'pending' | 'active' | 'inactive';
type Result = string | number | boolean;

// 类型守卫
function processResult(result: Result) {
    if (typeof result === 'string') {
        return result.toUpperCase();
    } else if (typeof result === 'number') {
        return result * 2;
    }
    return result;
}
```

### 5.2 可辨识联合

```typescript
interface Circle {
    kind: 'circle';
    radius: number;
}

interface Square {
    kind: 'square';
    sideLength: number;
}

type Shape = Circle | Square;

function getArea(shape: Shape): number {
    switch (shape.kind) {
        case 'circle':
            return Math.PI * shape.radius ** 2;
        case 'square':
            return shape.sideLength ** 2;
    }
}
```

### 5.3 交叉类型

```typescript
interface User {
    id: string;
    name: string;
}

interface Employee {
    employeeId: string;
    department: string;
}

type EmployeeUser = User & Employee;

const employee: EmployeeUser = {
    id: '123',
    name: 'John',
    employeeId: 'E456',
    department: 'Engineering'
};
```

## 六、类型守卫

### 6.1 typeof 类型守卫

```typescript
function processValue(value: string | number) {
    if (typeof value === 'string') {
        return value.toUpperCase();
    }
    return value * 2;
}
```

### 6.2 instanceof 类型守卫

```typescript
class Dog {
    bark() { }
}

class Cat {
    meow() { }
}

function makeSound(animal: Dog | Cat) {
    if (animal instanceof Dog) {
        animal.bark();
    } else {
        animal.meow();
    }
}
```

### 6.3 自定义类型守卫

```typescript
interface User {
    id: string;
    name: string;
}

function isUser(value: unknown): value is User {
    return (
        typeof value === 'object' &&
        value !== null &&
        'id' in value &&
        'name' in value
    );
}

function processValue(value: unknown) {
    if (isUser(value)) {
        console.log(value.name);
    }
}
```

## 七、工具类型

### 7.1 Partial - 所有属性变为可选

```typescript
interface User {
    id: string;
    name: string;
    email: string;
}

type PartialUser = Partial<User>;
// { id?: string; name?: string; email?: string }
```

### 7.2 Required - 所有属性变为必需

```typescript
interface PartialUser {
    id?: string;
    name?: string;
}

type FullUser = Required<PartialUser>;
// { id: string; name: string }
```

### 7.3 Pick - 选择部分属性

```typescript
interface User {
    id: string;
    name: string;
    email: string;
    age: number;
}

type UserPreview = Pick<User, 'id' | 'name'>;
// { id: string; name: string }
```

### 7.4 Omit - 排除部分属性

```typescript
interface User {
    id: string;
    name: string;
    email: string;
    password: string;
}

type SafeUser = Omit<User, 'password'>;
// { id: string; name: string; email: string }
```

### 7.5 Record - 构造对象类型

```typescript
type UserMap = Record<string, User>;
const users: UserMap = {
    '1': { id: '1', name: 'John' },
    '2': { id: '2', name: 'Jane' }
};
```

### 7.6 Exclude - 排除类型

```typescript
type T = Exclude<'a' | 'b' | 'c', 'a'>;
// 'b' | 'c'
```

### 7.7 Extract - 提取类型

```typescript
type T = Extract<'a' | 'b' | 'c', 'a' | 'b'>;
// 'a' | 'b'
```

## 八、枚举使用规范

### 8.1 数字枚举

```typescript
enum Status {
    Pending, // 0
    Active,  // 1
    Inactive // 2
}
```

### 8.2 字符串枚举

```typescript
enum Status {
    Pending = 'pending',
    Active = 'active',
    Inactive = 'inactive'
}
```

### 8.3 使用常量枚举（推荐用于编译优化）

```typescript
const enum Status {
    Pending = 'pending',
    Active = 'active',
    Inactive = 'inactive'
}
```

## 九、类型断言

### 9.1 as 语法

```typescript
const value: unknown = 'hello';
const strLength = (value as string).length;
```

### 9.2 避免过度使用类型断言

```typescript
// 不好
const data = fetchData() as any;

// 好
const data = fetchData() as UserData;
```

## 十、模块声明

### 10.1 声明全局类型

```typescript
// src/types/global.d.ts
declare global {
    interface Window {
        __APP_VERSION__: string;
    }
}

export {};
```

### 10.2 声明第三方模块

```typescript
// src/types/third-party.d.ts
declare module 'some-untyped-library' {
    export function doSomething(): void;
}
```

## 十一、最佳实践

### 11.1 类型文件组织

```
src/
├── types/
│   ├── index.ts          # 导出所有类型
│   ├── user.ts           # 用户相关类型
│   ├── order.ts          # 订单相关类型
│   └── api.ts            # API 相关类型
```

### 11.2 类型导出

```typescript
// src/types/user.ts
export interface User {
    id: string;
    name: string;
}

export type UserRole = 'admin' | 'user';

// src/types/index.ts
export * from './user';
export * from './order';
```

### 11.3 类型守卫集中管理

```typescript
// src/utils/typeGuards.ts
export function isUser(value: unknown): value is User {
    // ...
}

export function isOrder(value: unknown): value is Order {
    // ...
}
```

## 十二、严格模式建议

### 12.1 tsconfig.json 配置

```json
{
    "compilerOptions": {
        "strict": true,
        "noImplicitAny": true,
        "strictNullChecks": true,
        "strictFunctionTypes": true,
        "strictBindCallApply": true,
        "strictPropertyInitialization": true,
        "noImplicitThis": true,
        "alwaysStrict": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true
    }
}
```

### 12.2 strictNullChecks

```typescript
// 启用 strictNullChecks 后
function getUser(id: string): User | null {
    // ...
}

const user = getUser('123');
if (user) {
    console.log(user.name); // 安全访问
}
```

## 十三、错误处理规范

### 13.1 始终处理错误

```typescript
try {
    await fetchData();
} catch (error) {
    console.error('获取数据失败:', error);
    // 或显示用户提示
    message.error('获取数据失败');
}
```

### 13.2 Promise 错误处理

```typescript
fetchData()
    .then(data => console.log(data))
    .catch(error => console.error(error));
```

### 13.3 错误处理最佳实践

- 不要忽略 catch 块中的错误
- 提供有意义的错误信息
- 区分用户错误和系统错误
- 在适当层级处理错误，不要所有错误都在最上层处理
