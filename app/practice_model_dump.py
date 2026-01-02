from datetime import datetime
from typing import List

from pydantic import BaseModel


class Tag(BaseModel):
    name: str


class Article(BaseModel):
    title: str
    content: str
    published_at: datetime
    tags: List[Tag]


# 實例化模型
article = Article(
    title="FastAPI教學",
    content="詳細解說...",
    published_at=datetime(2025, 12, 30, 10, 0, 0),
    tags=[Tag(name="Python"), Tag(name="Config")],
)

# 轉換為 Dict
data = article.model_dump()

print(data)
