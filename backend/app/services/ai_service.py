from typing import List, Dict
from openai import OpenAI
from app.config import settings
from app.schemas import QuestionCreate
from app.models import DifficultyLevel, QuestionCategory
import json

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url=settings.OPENAI_BASE_URL)
    
    def generate_questions(
        self, 
        category: QuestionCategory, 
        difficulty: DifficultyLevel, 
        count: int
    ) -> List[QuestionCreate]:
        """使用OpenAI API生成面试题目"""
        
        difficulty_prompts = {
            DifficultyLevel.EASY: "基础",
            DifficultyLevel.MEDIUM: "中等",
            DifficultyLevel.HARD: "高级"
        }
        
        category_prompts = {
            QuestionCategory.ALGORITHM: "算法和数据结构",
            QuestionCategory.DATABASE: "数据库",
            QuestionCategory.SYSTEM_DESIGN: "系统设计",
            QuestionCategory.FRONTEND: "前端开发",
            QuestionCategory.BACKEND: "后端开发",
            QuestionCategory.DEVOPS: "运维和DevOps",
            QuestionCategory.MOBILE: "移动开发",
            QuestionCategory.DATA_SCIENCE: "数据科学",
            QuestionCategory.SECURITY: "网络安全",
            QuestionCategory.TESTING: "软件测试"
        }
        
        prompt = f"""
        请生成{count}个{difficulty_prompts[difficulty]}难度的{category_prompts[category]}面试题目。
        
        每个题目需要包含：
        1. 简洁明了的题目标题
        2. 详细的题目描述
        3. 完整的解题思路和分析
        4. 相关的技术标签（3-5个）
        
        请以JSON格式返回，结构如下：
        {{
            "questions": [
                {{
                    "title": "题目标题",
                    "content": "题目详细描述",
                    "category": "{category.value}",
                    "difficulty": "{difficulty.value}",
                    "analysis": "解题思路和分析",
                    "tags": ["标签1", "标签2", "标签3"]
                }}
            ]
        }}
        
        确保题目具有实际工程价值，避免过于理论化的问题。
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的技术面试官，擅长生成高质量的面试题目。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            # 尝试解析JSON响应
            try:
                # 提取JSON部分（如果响应包含其他文本）
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    content = json_match.group()
                
                data = json.loads(content)
                questions = []
                
                for q_data in data.get("questions", []):
                    question = QuestionCreate(
                        title=q_data["title"],
                        content=q_data["content"],
                        category=QuestionCategory(q_data["category"]),
                        difficulty=DifficultyLevel(q_data["difficulty"]),
                        analysis=q_data.get("analysis"),
                        tags=q_data.get("tags", [])
                    )
                    questions.append(question)
                
                return questions
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # 如果JSON解析失败，返回模拟数据
                return self._generate_mock_questions(category, difficulty, count)
                
        except Exception as e:
            # API调用失败时返回模拟数据
            return self._generate_mock_questions(category, difficulty, count)
    
    def _generate_mock_questions(
        self, 
        category: QuestionCategory, 
        difficulty: DifficultyLevel, 
        count: int
    ) -> List[QuestionCreate]:
        """生成模拟题目（当AI服务不可用时）"""
        
        mock_questions = {
            QuestionCategory.ALGORITHM: [
                {
                    "title": "实现二分查找算法",
                    "content": "请实现一个高效的二分查找算法，在有序数组中查找目标值。要求时间复杂度为O(log n)。",
                    "analysis": "二分查找通过反复将搜索范围减半来快速定位目标值。关键要点包括：1) 确定左右边界；2) 计算中间索引；3) 比较并调整边界；4) 处理边界条件。",
                    "tags": ["算法", "数组", "二分查找"]
                },
                {
                    "title": "链表反转",
                    "content": "实现一个函数来反转单链表，要求空间复杂度为O(1)。",
                    "analysis": "使用三个指针(prev, current, next)来迭代反转链表。prev初始为None，current指向头节点，在遍历过程中逐步改变指针方向。",
                    "tags": ["链表", "指针", "迭代"]
                }
            ],
            QuestionCategory.DATABASE: [
                {
                    "title": "数据库索引优化",
                    "content": "如何优化慢查询？请解释索引的工作原理以及何时应该创建索引。",
                    "analysis": "索引优化策略包括：1) 分析查询模式；2) 为WHERE子句中的列创建索引；3) 考虑复合索引的顺序；4) 避免过多的索引；5) 使用EXPLAIN分析查询计划。",
                    "tags": ["数据库", "索引", "性能优化"]
                },
                {
                    "title": "事务ACID特性",
                    "content": "解释数据库事务的ACID特性，以及如何在实际应用中保证这些特性。",
                    "analysis": "ACID特性：原子性(Atomicity)确保操作要么全部完成要么全部不完成；一致性(Consistency)保证数据完整性；隔离性(Isolation)防止并发问题；持久性(Durability)确保已提交事务的永久保存。",
                    "tags": ["事务", "ACID", "并发控制"]
                }
            ],
            QuestionCategory.SYSTEM_DESIGN: [
                {
                    "title": "设计分布式缓存系统",
                    "content": "设计一个高可用的分布式缓存系统，支持数据分片和故障转移。",
                    "analysis": "关键设计考虑：1) 一致性哈希实现数据分片；2) 多副本保证可用性；3) 缓存失效策略；4) 缓存穿透和雪崩防护；5) 监控和告警机制。",
                    "tags": ["系统设计", "分布式", "缓存"]
                },
                {
                    "title": "微服务架构设计",
                    "content": "如何将单体应用拆分为微服务？讨论拆分策略和可能遇到的挑战。",
                    "analysis": "拆分策略：按业务领域拆分，遵循单一职责原则。挑战包括：分布式事务、服务间通信、数据一致性、监控和运维复杂性。需要配套的服务发现、配置管理、熔断降级等组件。",
                    "tags": ["微服务", "架构设计", "分布式系统"]
                }
            ]
        }
        
        questions = []
        templates = mock_questions.get(category, mock_questions[QuestionCategory.ALGORITHM])
        
        for i in range(min(count, len(templates))):
            template = templates[i % len(templates)]
            question = QuestionCreate(
                title=f"{template['title']} - 模拟题目 {i+1}",
                content=template['content'],
                category=category,
                difficulty=difficulty,
                analysis=template['analysis'],
                tags=template['tags']
            )
            questions.append(question)
        
        return questions

# 创建全局实例
ai_service = AIService()