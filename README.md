# DeepSeek API Arena

A benchmarking tool for comparing different LLM API providers. Currently supports:
- DeepSeek API
- SiliconFlow API
- Ark API
- Tencent Cloud LKE API
- Alibaba Cloud Bailian API

## Features

- Measures Time To First Token (TTFT) and Token Between Time (TBT)
- Supports multiple runs for statistical significance
- Configurable providers via environment variables
- Detailed logging for debugging
- Stream-based API calls for real-time token processing

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install requests python-dotenv
```

## Configuration

Create a `.env` file in the project root with your API keys:

```env
DEEPSEEK_API_KEY=your_deepseek_key
SILICONFLOW_API_KEY=your_siliconflow_key
ARK_API_KEY=your_ark_key
ARK_MODEL_NAME=your_ark_model_name

# Optional: Set logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Optional: Configure proxy if needed
HTTP_PROXY=http://your-proxy:port
HTTPS_PROXY=http://your-proxy:port
```

## Usage

Basic usage:
```bash
python bench.py
```

Run with specific number of iterations:
```bash
python bench.py --num-runs 5
```

Benchmark specific providers:
```bash
python bench.py --providers deepseek siliconflow
python bench.py --providers ark
```

Combined options:
```bash
python bench.py --providers deepseek --num-runs 3
```

## Output

Results are saved to `results_YYYY-MM-DD.txt` with the following format:
```
Provider            Avg TTFT (s)    Avg TBT (s)   
--------------------------------------------------
DeepSeek           0.8532          0.0234
```

- TTFT: Time To First Token (lower is better)
- TBT: Token Between Time (lower is better)

## Debugging

Set `LOG_LEVEL=DEBUG` in your `.env` file for detailed logging output.

## License

MIT License
