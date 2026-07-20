# OpenAI Models Speedtest

A self-contained browser benchmark for OpenAI Responses API streaming calls. Open it locally, or use the published demo at:

<https://rdslw.github.io/risercz/oai-models-speedtest/demo.html>

## Run setup

1. Enter an OpenAI API key. Use **Save key to browser** if you want to retain it in browser `localStorage`; the clear saved/available state confirms what is stored. The key is only sent in the Authorization header to `https://api.openai.com` when a run begins.
2. Select 1–20 tries per model/mode, a total budget, an approximate generated input size (10K–100K tokens), and requested output target (2K–20K tokens). The page does not expose an editable prompt: it generates repeated one-thousand-token lorem-ipsum blocks and instructs the model to produce numbered, invented field-guide entries until the requested output target is reached. Hover the ⓘ marker to preview those critical output instructions. The API receives twice the requested output target as `max_output_tokens` to leave completion headroom.
3. Review each row’s expected maximum cost and the total. The Run button is disabled, and expected-cost cells turn red, when the selected rows’ maximum cost is above the budget.
4. Runs shuffle the model/mode attempts. Normal mode uses `service_tier: "auto"`; FAST uses `service_tier: "priority"`. Unavailable models/tier combinations are recorded as failures—nothing is substituted.

## Prices

The twelve default rows retain the requested six model names. Normal-mode input/output prices are taken from the current [`data/openai.json` in Simon Willison’s llm-prices repository](https://github.com/simonw/llm-prices/blob/main/data/openai.json), retrieved during this update: `gpt-5.6-sol` $5/$30, `gpt-5.6-terra` $2.50/$15, `gpt-5.6-luna` $1/$6, `gpt-5.4` $2.50/$15, `gpt-5.4-mini` $0.75/$4.50, and `gpt-5.4-nano` $0.20/$1.25 per million input/output tokens. FAST rows use the published priority-processing 2× rate. All displayed rates are editable because model availability and pricing can change.

Expected maximum cost is `tries × (selected input tokens × input price + twice the requested output target × output price) / 1,000,000`, reflecting the API output cap and budget guard. Actual cost uses returned `input_tokens` and `output_tokens`. The preflight uses the maximum requested output, so it is deliberately conservative; the in-run budget guard also stops before a further estimated attempt would exceed the cap.

## Measurements

- **TTFT** starts immediately before browser `fetch()` and ends at the first `response.output_text.delta`; it includes browser, network, queue, and model-first-text time.
- **Total latency** ends when the response stream closes.
- **Tokens/sec** is returned output tokens divided by the time from first text delta to stream completion. If a terminal usage event is unavailable, the page uses a character-count fallback.
- HTTP 429 responses retry up to twice with exponential backoff. Retry timers are reset for every attempt, avoiding backoff time in the subsequent measurement.

## Content Security Policy

The page includes a CSP before its inline script. It permits connections only to `https://api.openai.com`, disables plugin objects, form submissions, and base-URL changes, and authorizes the exact embedded script with a SHA-256 hash. This is not circular: the hash covers the script contents, not the HTML document or CSP meta tag. Regenerate the hash whenever the script changes; otherwise browsers will block the changed script. Inline styles remain permitted because the standalone page includes CSS and bounded result-bar widths.

## Running

There is no build step or backend:

```sh
python3 -m http.server 8000 --directory oai-models-speedtest
```

Then browse to `http://localhost:8000/demo.html`.
