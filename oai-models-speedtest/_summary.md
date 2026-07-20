OpenAI Models Speedtest is a browser-based tool that benchmarks the streaming response performance of OpenAI models via API calls, measuring metrics like time to first token (TTFT), total latency, tokens per second, and cost. Users input an API key, choose models/modes, and set spending limits; the tool shuffles and tests requests across selected model/mode pairs to ensure fair comparison, retrying rate-limited responses where possible. Pricing fields are editable due to frequent OpenAI changes, and the tool’s restrictive Content Security Policy enhances security—connections are only made to OpenAI’s API, with script execution governed by strict hashing. No backend or build step is required; you can run the benchmark locally or through the [demo interface](https://rdslw.github.io/risercz/oai-models-speedtest/demo.html).

**Key Features:**
- Benchmarks TTFT, throughput, and cost across model streaming modes, including priority processing.
- Editable pricing/adaptive cost cap; partial results preserved if spending limits are hit.
- Secure-by-design: only API calls, tight CSP, no backend.
- [Project repo and documentation](https://github.com/risercz/oai-models-speedtest) available for further customization.
