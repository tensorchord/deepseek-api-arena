import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Provider:
    name: str
    api_key: str
    api_base: str
    model_name: str

AVAILABLE_PROVIDERS = {
    "deepseek": Provider(
        name="DeepSeek",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        api_base="https://api.deepseek.com/v1",
        model_name="deepseek-reasoner",
    ),
    "siliconflow": Provider(
        name="siliconflow",
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        api_base="https://api.siliconflow.cn/v1",
        model_name="Pro/deepseek-ai/DeepSeek-R1",
    ),
    "ark": Provider(
        name="Ark",
        api_key=os.getenv("ARK_API_KEY"),
        api_base="https://ark.cn-beijing.volces.com/api/v3",
        model_name=os.getenv("ARK_MODEL_NAME"),
    ),
    "bailian": Provider(
        name="Bailian",
        api_key=os.getenv("BAILIAN_API_KEY"),
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_name="deepseek-r1",
    ),
}
