# OpenAI Models Speedtest

A self-contained browser benchmark for OpenAI Responses API streaming calls. Open it locally, or use the published demo at:

<https://rdslw.github.io/risercz/oai-models-speedtest/demo.html>

## How it works

1. Add an API key, select models/modes, choose attempts and a total budget. The key is stored only in browser `localStorage` and is sent only as an Authorization header to `https://api.openai.com`.
2. Every attempt sends the same bounded prompt to `POST /v1/responses` with `stream: true` and `max_output_tokens: 64`.
3. Normal tests send `service_tier: "auto"`; FAST tests send `service_tier: "priority"`. If priority processing or a model is unavailable, that attempt is shown as a failure and the benchmark continues—no model is substituted.
4. Attempts are shuffled across model/mode pairs before running, to reduce a fixed warm-up or time-of-day ordering advantage. HTTP 429 responses are retried up to twice with exponential backoff; failed retries do not create a completed measurement or add spend.

## Measurements

- **TTFT** starts immediately before browser `fetch()` and stops at the first `response.output_text.delta` stream event. It includes browser scheduling, network transit, API queueing, and model time to first visible text.
- **Total latency** ends after the streamed response body completes.
- **Tokens/sec** is reported as returned output tokens divided by time from first text delta to stream completion. If usage is absent, the tool uses a clearly best-effort character-count fallback only for display/cost continuity.
- **Cost** uses the usage fields returned in the terminal response (`input_tokens` and `output_tokens`) multiplied by the editable per-million-token prices for the selected mode. The tool preflights a conservative short-prompt/64-output-token estimate and stops before an attempt that would cross the total cap. It also keeps partial results if the cap is reached.

## Pricing and model caveats

The UI makes pricing deliberately editable: price sheets and priority-processing availability change. The prefilled values are planning estimates rather than a source of billing truth. This environment returned HTTP 403 when fetching OpenAI's pricing page directly, so the values could not be automatically verified during this investigation. Verify current prices and model availability in OpenAI documentation before relying on a result for a cost decision.

The requested `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna` names are passed through exactly as entered. This project did not find a live API key to smoke-test them, and does not silently replace them if the API reports an unknown model. The live results table will surface those failures alongside successful rows.

## Running

There is no build step or backend. Serve this folder with any static server (or open the HTML directly; the OpenAI endpoint must allow your browser origin):

```sh
python3 -m http.server 8000 --directory oai-models-speedtest
```

Then browse to `http://localhost:8000/demo.html`.
