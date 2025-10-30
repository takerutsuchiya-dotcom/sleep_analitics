from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64, os
from openai import OpenAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/upload")
async def analyze_image(data: ImageData):
    b64 = data.image.split(",")[1]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは睡眠データ解析の専門家です。"},
            {"role": "user", "content": [
                {"type": "text", "text": "以下の睡眠グラフから睡眠傾向・睡眠効率・健康リスクを分析し、改善アドバイスをください。"},
                {"type": "image_url", "image_url": "data:image/png;base64," + b64}
            ]}
        ]
    )
    result = response.choices[0].message.content
    return {"report": result}
