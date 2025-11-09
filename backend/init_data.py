#!/usr/bin/env python3
"""
初始化数据脚本
用于添加示例题目数据到数据库
"""

import os
import sys
import json
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Question, DifficultyLevel, QuestionCategory

# 创建数据库表
Base.metadata.create_all(bind=engine)

def init_sample_data():
    """初始化示例数据"""
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 条数据，跳过初始化")
            return
        
        # 示例题目数据
        sample_questions = [
            # 算法题目
            {
                "title": "实现二分查找算法",
                "content": """请实现一个高效的二分查找算法，在有序数组中查找目标值。

**要求：**
- 时间复杂度为 O(log n)
- 空间复杂度为 O(1)
- 如果找到目标值，返回其索引；否则返回 -1

**示例：**
```
输入: nums = [-1,0,3,5,9,12], target = 9
输出: 4
解释: 9 出现在 nums 中并且下标为 4
```

**提示：**
- 你可以假设数组中的所有元素是不重复的
- n 将在 [1, 10000] 之间
- nums 的每个元素都将在 [-9999, 9999] 之间""",
                "category": QuestionCategory.ALGORITHM,
                "difficulty": DifficultyLevel.EASY,
                "analysis": """二分查找是一种在有序数组中查找特定元素的高效算法。

**算法步骤：**
1. 初始化左指针 left = 0，右指针 right = n-1
2. 当 left <= right 时：
   - 计算中间位置 mid = left + (right - left) // 2
   - 如果 nums[mid] == target，返回 mid
   - 如果 nums[mid] < target，说明目标在右半部分，left = mid + 1
   - 如果 nums[mid] > target，说明目标在左半部分，right = mid - 1
3. 如果循环结束仍未找到，返回 -1

**关键点：**
- 循环条件是 left <= right，不是 left < right
- 计算 mid 时使用 left + (right - left) // 2 可以防止整数溢出
- 更新指针时要注意边界条件

**时间复杂度分析：**
- 每次都将搜索范围减半，所以时间复杂度是 O(log n)
- 只使用了常数级别的额外空间，空间复杂度是 O(1)""",
                "tags": ["二分查找", "数组", "算法"]
            },
            {
                "title": "链表反转",
                "content": """实现一个函数来反转单链表，要求空间复杂度为 O(1)。

**示例：**
```
输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
```

**进阶：**
- 你可以迭代或递归地反转链表
- 你能否同时实现迭代和递归的解决方案？""",
                "category": QuestionCategory.ALGORITHM,
                "difficulty": DifficultyLevel.MEDIUM,
                "analysis": """链表反转是链表操作中的经典问题，有多种解法。

**迭代解法（推荐）：**
使用三个指针：prev、current、next
1. 初始化 prev = None，current = head
2. 遍历链表：
   - 保存 next = current.next
   - 反转指针：current.next = prev
   - 移动指针：prev = current，current = next
3. 最后返回 prev 作为新的头节点

**递归解法：**
1. 递归基：如果 head 为空或 head.next 为空，返回 head
2. 递归反转剩余的链表：new_head = reverseList(head.next)
3. 处理当前节点：head.next.next = head，head.next = None
4. 返回 new_head

**迭代解法优势：**
- 空间复杂度 O(1)
- 不会栈溢出
- 更直观易懂

**注意事项：**
- 要处理好头尾节点的边界条件
- 递归解法虽然简洁，但有栈溢出的风险""",
                "tags": ["链表", "指针", "迭代"]
            },
            
            # 数据库题目
            {
                "title": "数据库索引优化",
                "content": """如何优化慢查询？请解释索引的工作原理以及何时应该创建索引。

**问题描述：**
假设你有一个用户表，包含以下字段：
- id (主键)
- username (用户名)
- email (邮箱)
- created_at (创建时间)
- status (状态)

查询语句：
```sql
SELECT * FROM users WHERE username = 'john' AND status = 'active';
```

这个查询执行很慢，请分析原因并提供优化方案。""",
                "category": QuestionCategory.DATABASE,
                "difficulty": DifficultyLevel.MEDIUM,
                "analysis": """数据库索引优化是提升查询性能的关键。

**索引工作原理：**
- 索引是一种数据结构（通常是B+树），用于快速定位数据
- 类比书籍的目录，可以快速找到内容所在页码
- 索引存储了索引列的值和对应行的物理位置

**优化方案：**
1. **创建复合索引**：
   ```sql
   CREATE INDEX idx_username_status ON users(username, status);
   ```

2. **索引列顺序**：
   - 选择性高的列放在前面
   - WHERE子句中经常使用的列优先

3. **其他优化建议：**
   - 避免SELECT *，只查询需要的列
   - 考虑覆盖索引（包含所有查询列）
   - 定期分析和优化表：ANALYZE TABLE users
   - 监控慢查询日志
   - 使用EXPLAIN分析查询计划

**何时创建索引：**
- WHERE子句中频繁使用的列
- JOIN操作的连接列
- ORDER BY和GROUP BY的列
- 选择性高的列（唯一值多）

**何时不创建索引：**
- 表数据量很小
- 频繁更新的列
- 低选择性的列（如性别、状态）
- 很少查询的列""",
                "tags": ["数据库", "索引", "性能优化", "SQL"]
            },
            {
                "title": "事务ACID特性",
                "content": """解释数据库事务的ACID特性，以及如何在实际应用中保证这些特性。

**问题描述：**
在转账操作中，需要从一个账户扣款，向另一个账户存款。如何保证这个操作的原子性和一致性？

**要求：**
- 详细解释ACID四个特性
- 提供具体的实现方案
- 讨论并发情况下的处理""",
                "category": QuestionCategory.DATABASE,
                "difficulty": DifficultyLevel.HARD,
                "analysis": """ACID是数据库事务的四个基本特性，确保数据的可靠性和一致性。

**ACID特性详解：**

1. **原子性 (Atomicity)**
   - 事务中的所有操作要么全部完成，要么全部不完成
   - 不存在中间状态
   - 实现：通过undo log，失败时回滚已执行的操作

2. **一致性 (Consistency)**
   - 事务执行前后，数据库的完整性约束没有被破坏
   - 数据从一个一致状态转换到另一个一致状态
   - 实现：通过约束、触发器、业务逻辑保证

3. **隔离性 (Isolation)**
   - 并发执行的事务之间互不干扰
   - 一个事务的中间状态对其他事务不可见
   - 实现：通过锁机制或MVCC（多版本并发控制）

4. **持久性 (Durability)**
   - 已提交的事务修改是永久性的
   - 即使系统崩溃，已提交的数据也不会丢失
   - 实现：通过redo log，崩溃恢复时重做已提交的事务

**转账事务示例：**
```sql
BEGIN TRANSACTION;

-- 检查账户A余额
SELECT balance FROM accounts WHERE id = 'A';

-- 从账户A扣款
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';

-- 向账户B存款
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';

-- 记录转账日志
INSERT INTO transfer_log (from_account, to_account, amount) VALUES ('A', 'B', 100);

COMMIT;
```

**并发控制：**
- 使用适当的隔离级别（如READ COMMITTED）
- 乐观锁：使用版本号机制
- 悲观锁：使用SELECT ... FOR UPDATE""",
                "tags": ["事务", "ACID", "并发控制", "数据库"]
            },
            
            # 系统设计题目
            {
                "title": "设计分布式缓存系统",
                "content": """设计一个高可用的分布式缓存系统，支持数据分片和故障转移。

**需求：**
- 支持海量数据存储（TB级别）
- 高可用性，单点故障不影响服务
- 支持水平扩展
- 低延迟读写（<10ms）
- 支持多种淘汰策略

**请设计：**
1. 系统架构图
2. 数据分片策略
3. 故障转移机制
4. 缓存淘汰策略""",
                "category": QuestionCategory.SYSTEM_DESIGN,
                "difficulty": DifficultyLevel.HARD,
                "analysis": """分布式缓存系统设计需要考虑性能、可用性、一致性等多个方面。

**系统架构：**
```
客户端 -> 负载均衡器 -> 代理层 -> 缓存节点集群
                            |
                            v
                        持久化存储
```

**核心组件：**
1. **代理层（Proxy）**：
   - 请求路由和负载均衡
   - 协议转换
   - 监控和限流

2. **缓存节点集群**：
   - 数据存储节点
   - 支持主从复制
   - 自动故障检测

3. **配置中心**：
   - 集群配置管理
   - 节点状态监控
   - 动态配置更新

**数据分片策略：**
1. **一致性哈希**：
   - 解决传统哈希扩缩容问题
   - 虚拟节点减少数据倾斜
   - 顺时针查找数据节点

2. **分片算法：**
   ```python
   def get_node(key):
       hash_value = hash(key)
       # 在哈希环上顺时针查找第一个节点
       for node in sorted(hash_ring):
           if hash_value <= node:
               return hash_ring[node]
       # 如果没有找到，返回第一个节点
       return hash_ring[min(hash_ring.keys())]
   ```

**故障转移机制：**
1. **主从复制**：
   - 每个主节点配置多个从节点
   - 主节点故障时自动提升从节点
   - 异步复制，保证性能

2. **故障检测：**
   - 心跳机制检测节点状态
   - 客户端超时重试
   - 熔断器防止雪崩

**缓存淘汰策略：**
1. **LRU（最近最少使用）**：适合热点数据
2. **LFU（最不经常使用）**：适合长期热点
3. **TTL（过期时间）**：适合时效性数据
4. **Random**：简单高效

**高可用性保证：**
- 多副本存储
- 跨机房部署
- 自动故障恢复
- 降级策略""",
                "tags": ["系统设计", "分布式", "缓存", "高可用"]
            },
            
            # 前端题目
            {
                "title": "虚拟DOM实现原理",
                "content": """解释虚拟DOM的工作原理，以及它如何提高前端性能。

**问题：**
1. 什么是虚拟DOM？
2. 虚拟DOM如何工作？
3. 相比直接操作真实DOM的优势？
4. 虚拟DOM的diff算法原理？

**请用代码示例说明虚拟DOM的实现。**""",
                "category": QuestionCategory.FRONTEND,
                "difficulty": DifficultyLevel.MEDIUM,
                "analysis": """虚拟DOM是现代前端框架的核心概念，用于提高DOM操作效率。

**虚拟DOM定义：**
虚拟DOM是用JavaScript对象表示DOM结构的轻量级副本。它是对真实DOM的抽象表示。

**工作原理：**
1. **创建虚拟DOM**：将模板编译成虚拟DOM对象
2. **状态变更**：当数据变化时，创建新的虚拟DOM树
3. **diff算法**：比较新旧虚拟DOM树的差异
4. **批量更新**：将差异应用到真实DOM

**虚拟DOM结构示例：**
```javascript
// 虚拟DOM节点结构
const vNode = {
  type: 'div',
  props: {
    className: 'container',
    onClick: handleClick
  },
  children: [
    {
      type: 'h1',
      props: {},
      children: ['Hello World']
    }
  ]
}
```

**Diff算法原理：**
1. **同层比较**：只比较同一层级的节点
2. **key优化**：使用key标识节点，提高比较效率
3. **类型不同**：直接替换整个子树
4. **类型相同**：比较属性，递归比较子节点

**简化版Diff算法：**
```javascript
function diff(oldVNode, newVNode) {
  // 1. 节点类型不同
  if (oldVNode.type !== newVNode.type) {
    return { type: 'REPLACE', newNode: newVNode }
  }
  
  // 2. 比较属性
  const propsDiff = diffProps(oldVNode.props, newVNode.props)
  
  // 3. 比较子节点
  const childrenDiff = diffChildren(oldVNode.children, newVNode.children)
  
  return {
    type: 'UPDATE',
    props: propsDiff,
    children: childrenDiff
  }
}
```

**性能优势：**
1. **减少DOM操作**：批量更新，减少重排重绘
2. **跨平台**：虚拟DOM可以渲染到不同平台（Web、Native、小程序）
3. **开发效率**：声明式编程，专注于数据逻辑

**劣势：**
- 额外的内存开销
- 首次渲染性能略低于直接操作DOM
- 学习成本较高""",
                "tags": ["前端", "虚拟DOM", "性能优化", "React"]
            },
            
            # 后端题目
            {
                "title": "微服务架构设计",
                "content": """如何将单体应用拆分为微服务？讨论拆分策略和可能遇到的挑战。

**背景：**
假设你有一个电商系统，包含用户管理、商品管理、订单管理、支付处理等模块。

**要求：**
1. 设计微服务拆分方案
2. 说明拆分原则和依据
3. 讨论服务间通信方式
4. 分析可能遇到的挑战和解决方案

**请提供具体的拆分方案和架构图。**""",
                "category": QuestionCategory.BACKEND,
                "difficulty": DifficultyLevel.HARD,
                "analysis": """微服务架构是现代分布式系统的主流架构模式。

**拆分原则：**
1. **单一职责原则**：每个服务只负责一个业务领域
2. **服务自治**：独立开发、部署、扩展
3. **业务边界清晰**：基于业务能力划分
4. **数据隔离**：每个服务拥有自己的数据库

**电商系统拆分方案：**
```
用户服务 (User Service)
├── 用户注册/登录
├── 用户信息管理
└── 权限控制

商品服务 (Product Service)
├── 商品信息管理
├── 库存管理
└── 商品分类

订单服务 (Order Service)
├── 订单创建/查询
├── 订单状态管理
└── 订单详情

支付服务 (Payment Service)
├── 支付处理
├── 退款处理
└── 支付记录

通知服务 (Notification Service)
├── 邮件通知
├── 短信通知
└── 推送通知
```

**服务间通信：**
1. **同步通信**（RPC）：
   - REST API
   - gRPC
   - GraphQL

2. **异步通信**（消息队列）：
   - RabbitMQ
   - Apache Kafka
   - Redis Pub/Sub

**技术栈选择：**
- **服务注册发现**：Consul、Eureka、Nacos
- **API网关**：Kong、Zuul、Spring Cloud Gateway
- **配置中心**：Apollo、Nacos、Consul
- **监控告警**：Prometheus + Grafana
- **链路追踪**：Jaeger、Zipkin
- **容器化**：Docker + Kubernetes

**挑战与解决方案：**

1. **分布式事务**：
   - 挑战：跨服务的数据一致性
   - 方案：SAGA模式、TCC模式、可靠消息最终一致性

2. **服务治理**：
   - 挑战：服务发现、负载均衡、熔断降级
   - 方案：Service Mesh（Istio）、Hystrix

3. **数据一致性**：
   - 挑战：分布式环境下的数据同步
   - 方案：事件驱动、CQRS模式

4. **运维复杂性**：
   - 挑战：部署、监控、调试困难
   - 方案：DevOps、自动化部署、集中化日志

5. **性能问题**：
   - 挑战：网络延迟、服务调用链长
   - 方案：缓存、异步处理、服务网格优化

**实施建议：**
1. 循序渐进，先从边缘服务开始拆分
2. 建立完善的监控和告警体系
3. 重视自动化测试和部署
4. 加强团队技术能力建设""",
                "tags": ["微服务", "架构设计", "分布式系统", "后端"]
            }
        ]
        
        # 添加示例数据到数据库
        for question_data in sample_questions:
            # 将 tags 列表转换为 JSON 字符串
            if 'tags' in question_data and isinstance(question_data['tags'], list):
                question_data['tags'] = json.dumps(question_data['tags'], ensure_ascii=False)
            question = Question(**question_data)
            db.add(question)
        
        db.commit()
        print(f"成功添加 {len(sample_questions)} 条示例题目数据")
        
    except Exception as e:
        db.rollback()
        print(f"添加数据失败: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("开始初始化示例数据...")
    init_sample_data()
    print("数据初始化完成！")