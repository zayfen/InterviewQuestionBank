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
            QuestionCategory.TESTING: "软件测试",
            QuestionCategory.REACT_NATIVE: "React Native",
            QuestionCategory.REACT: "React"
        }
        
        prompt = f"""
        请生成{count}个{difficulty_prompts[difficulty]}难度的{category_prompts[category]}面试题目。
        
        每个题目需要包含：
        1. 简洁明了的题目标题
        2. 详细的题目描述
        3. 完整的解题思路和原理细节剖析。根据需要，生成Markdown格式的 mermaid格式的流程图 以辅助理解。
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
        注意：analysis中可能包含markdown格式代码，请检查编码问题，确保完整的json是正确且可解析的。
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
                raise ValueError(f"AI 返回的数据格式解析失败: {str(e)} RawContent：{content}")
                
        except Exception as e:
            # 如果是自定义的 ValueError，直接向上抛出
            if isinstance(e, ValueError):
                raise
            # 其他异常也抛出，提供更详细的错误信息
            raise Exception(f"AI 服务调用失败: {str(e)}")

# 创建全局实例
ai_service = AIService()
