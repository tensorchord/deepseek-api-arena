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
    price_per_1m_input_tokens: float
    price_per_1m_output_tokens: float
    price_per_1m_input_tokens_cache: float = -1.0

AVAILABLE_PROVIDERS = {
    "deepseek": Provider(
        name="DeepSeek",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        api_base="https://api.deepseek.com/v1",
        model_name="deepseek-reasoner",
        price_per_1m_input_tokens=4.0,
        price_per_1m_input_tokens_cache=1.0,
        price_per_1m_output_tokens=16.0,
    ),
    "siliconflow": Provider(
        name="siliconflow",
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        api_base="https://api.siliconflow.cn/v1",
        model_name="Pro/deepseek-ai/DeepSeek-R1",
        price_per_1m_input_tokens=4.0,
        price_per_1m_output_tokens=16.0,
    ),
    "ark": Provider(
        name="Ark",
        api_key=os.getenv("ARK_API_KEY"),
        api_base="https://ark.cn-beijing.volces.com/api/v3",
        model_name=os.getenv("ARK_MODEL_NAME"),
        price_per_1m_input_tokens=2.0,
        price_per_1m_output_tokens=8.0,
    ),
    "bailian": Provider(
        name="Bailian",
        api_key=os.getenv("BAILIAN_API_KEY"),
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_name="deepseek-r1",
        price_per_1m_input_tokens=2.0,
        price_per_1m_output_tokens=8.0,
    ),
    "lke": Provider(
        name="LKE",
        api_key=os.getenv("LKE_API_KEY"),
        api_base="https://api.lkeap.cloud.tencent.com/v1",
        model_name="deepseek-r1",
        price_per_1m_input_tokens=4.0,
        price_per_1m_output_tokens=16.0,
    ),
}
