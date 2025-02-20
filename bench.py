import os
import time
import json
import requests
import argparse
from dotenv import load_dotenv
import logging
from providers import AVAILABLE_PROVIDERS, Provider

load_dotenv()

# Read the logging level from the environment variable
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Convert the string to a logging level
logging_level = getattr(logging, log_level, logging.INFO)

# Configure logging
logging.basicConfig(
    level=logging_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class Benchmark:
    def __init__(self, providers: list[Provider], num_runs: int = 3):
        self.providers = providers
        self.num_runs = num_runs
        self.logger = logging.getLogger(__name__)
        self.check_if_proxy_is_enabled()

    def check_if_proxy_is_enabled(self):
        proxy = os.getenv("HTTP_PROXY") or os.getenv("http_proxy") or os.getenv(
            "HTTPS_PROXY") or os.getenv("https_proxy")
        if proxy:
            self.logger.warning(f"Proxy is enabled with {proxy}")

    def make_api_call(self, provider: Provider):
        start_time = time.time()
        ttft = None
        token_times = []
        output = ""
        
        response = requests.post(
            f"{provider.api_base}/chat/completions",
            headers={"Authorization": f"Bearer {provider.api_key}"},
            json={
                "model": provider.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Please tell me about the history of the United States, including detailed reasoning "
                            "and analysis, as well as a comprehensive final output. The answer should be structured "
                            "to include both your step-by-step reasoning and the final result, spanning roughly 1k tokens in total."
                        ),
                    }
                ],
                "max_tokens": 100,
                "stream": True
            },
            stream=True
        )

        self.logger.debug(f"Request URL: {response.request.url}")
        self.logger.debug(f"Request Headers: {response.request.headers}")
        self.logger.debug(f"Request Body: {response.request.body}")
        self.logger.debug(f"Response Status: {response.status_code}")
        self.logger.debug(f"Response Headers: {response.headers}")

        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")
                    if decoded_line.startswith("data:"):
                        data = decoded_line[5:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"]
                            token = delta.get("reasoning_content") or delta.get("content")
                            if token:
                                output += token
                                current_time = time.time()
                                if ttft is None:
                                    ttft = current_time - start_time
                                token_times.append(current_time)
                        except json.JSONDecodeError:
                            self.logger.error(f"Error decoding JSON: {decoded_line}")
        else:
            self.logger.error(f"API error: {response.status_code} - {response.text}")

        return output, ttft, token_times

    def is_model_available(self, provider: Provider) -> bool:
        if provider.name == "Ark":
            self.logger.warning("Skipping model availability check for Ark, as it does not provide a model list")
            return True
        
        self.logger.info(f"Verifying model name {provider.model_name}")
        resp = requests.get(
            f"{provider.api_base}/models",
            headers={
                "Authorization": f"Bearer {provider.api_key}"
            },
        )
        self.logger.debug(f"Request URL: {resp.request.url}")
        self.logger.debug(f"Request Headers: {resp.request.headers}")
        self.logger.debug(f"Request Body: {resp.request.body}")
        self.logger.debug(f"Response: {resp}")

        models = resp.json()
        for model in models["data"]:
            if model["id"] == provider.model_name:
                return True
        self.logger.error(f"Model {provider.model_name} not found")
        return False

    @staticmethod
    def calculate_metrics(token_times):
        if len(token_times) > 1:
            intervals = [token_times[i] - token_times[i - 1]
                         for i in range(1, len(token_times))]
            return sum(intervals) / len(intervals)
        return None

    def write_results(self, provider: Provider, ttfts, tbts, filename: str):
        with open(filename, "a") as f:
            if os.path.getsize(filename) == 0:
                f.write(f"{'Provider':<20} {'Avg TTFT (s)':<15} {'Avg TBT (s)':<15}\n")
                f.write("-" * 50 + "\n")
            avg_ttft = sum(ttfts) / len(ttfts) if ttfts else None
            avg_tbt = sum(tbts) / len(tbts) if tbts else None
            f.write(f"{provider.name:<20} {avg_ttft if avg_ttft is not None else 'N/A':<15.4f} {avg_tbt if avg_tbt is not None else 'N/A':<15.4f}\n")

    def benchmark_single_provider(self, provider: Provider):
        ttfts = []
        tbts = []

        if not self.is_model_available(provider):
            self.logger.error(f"Model {provider.model_name} not available")
            return
        
        for run in range(self.num_runs):
            self.logger.debug(f"Run {run + 1}/{self.num_runs}")
            output, ttft, token_times = self.make_api_call(provider)
            tbt = self.calculate_metrics(token_times)

            self.logger.debug(f"Output: {output}")
            ttft_str = f"{ttft:.4f}" if ttft is not None else "N/A"
            tbt_str = f"{tbt:.4f}" if tbt is not None else "N/A"
            self.logger.info(f"Run {run + 1} - TTFT: {ttft_str}s, TBT: {tbt_str}s")

            if ttft is not None:
                ttfts.append(ttft)
            if tbt is not None:
                tbts.append(tbt)

        current_date = time.strftime("%Y-%m-%d")
        filename = f"results_{current_date}.txt"
        self.write_results(provider, ttfts, tbts, filename)

    def run(self):
        for provider in self.providers:
            self.logger.debug(f"Benchmarking {provider.name}...")
            self.benchmark_single_provider(provider)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Benchmark LLM providers')
    parser.add_argument(
        '-n', 
        '--num-runs',
        type=int,
        default=1,
        help='Number of benchmark runs to perform (default: 1)'
    )
    parser.add_argument(
        '-p',
        '--providers',
        nargs='+',
        choices=list(AVAILABLE_PROVIDERS.keys()),
        default=list(AVAILABLE_PROVIDERS.keys()),
        help='List of providers to benchmark (default: all providers)'
    )
    args = parser.parse_args()
    
    selected_providers = [AVAILABLE_PROVIDERS[p] for p in args.providers]
    benchmark = Benchmark(providers=selected_providers, num_runs=args.num_runs)
    benchmark.run()
