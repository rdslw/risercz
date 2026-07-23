# OpenAI Models Speedtest

A self-contained browser benchmark for OpenAI Responses API streaming calls. Open it locally, or use the published demo at:

<https://rdslw.github.io/risercz/oai-models-speedtest/demo.html>

## Run setup

1. Enter an OpenAI API key. Use **Save key to browser** if you want to retain it in browser `localStorage`; the clear saved/available state confirms what is stored. The key is only sent in the Authorization header to `https://api.openai.com` when a run begins.
2. Select 1–5 tries per model/mode, a total budget, an approximate generated input size (10K–100K tokens), and requested output tokens (2K–20K). The input prompt uses repeated one-thousand-token lorem-ipsum blocks; hover its ⓘ marker to see the leading instruction. The output contract is mechanically checkable: it requires exact numbered 1,000-word lowercase diceware blocks, one word per line, and one precisely formatted counter line after each 100 words. The request disables reasoning with `reasoning: {"effort": "none"}` so output capacity is directed to visible text. Hover the output ⓘ marker to preview it. The API receives twice the selected requested output value as `max_output_tokens`. Every benchmark request also starts with a unique five-word sentence to avoid reusing a cacheable leading prompt prefix.
3. Review each row’s expected maximum cost, total cost, and total sequential time in minutes. The Run button is disabled, and expected-cost cells turn red, when the selected rows’ maximum cost is above the budget.
4. Runs shuffle the model/mode attempts. Normal mode uses `service_tier: "auto"`; FAST uses `service_tier: "priority"`. Unavailable models/tier combinations are recorded as failures—nothing is substituted.

## Prices

The twelve default rows retain the requested six model names. Normal-mode input/output prices are taken from the current [`data/openai.json` in Simon Willison’s llm-prices repository](https://github.com/simonw/llm-prices/blob/main/data/openai.json), retrieved during this update: `gpt-5.6-sol` $5/$30, `gpt-5.6-terra` $2.50/$15, `gpt-5.6-luna` $1/$6, `gpt-5.4` $2.50/$15, `gpt-5.4-mini` $0.75/$4.50, and `gpt-5.4-nano` $0.20/$1.25 per million input/output tokens. FAST rows use the published priority-processing 2× rate. All displayed rates are editable because model availability and pricing can change.

Expected maximum cost is `tries × (selected input tokens × input price + (2 × requested output tokens) × output price) / 1,000,000`, reflecting the API output cap and budget guard. Each table row’s **Naive time bound** is `tries × (0.5 × input tokens / 5,000 tokens/second + requested output tokens / 100 tokens/second)`. Its ⓘ marker exposes the same equation. This is a coarse sequential planning bound, not a latency prediction. Actual cost uses returned `input_tokens` and `output_tokens`. The preflight uses the maximum requested output, so it is deliberately conservative; the in-run budget guard also stops before a further estimated attempt would exceed the cap.

## Measurements

- **TTFT** starts immediately before browser `fetch()` and ends at the first `response.output_text.delta`; it includes browser, network, queue, and model-first-text time.
- **Total latency** ends when the response stream closes.
- **Tokens/sec** is returned output tokens divided by the time from first text delta to stream completion. If a terminal usage event is unavailable, the page uses a character-count fallback. The result table’s input/output-token columns are medians of API-reported usage, not selected workload estimates. Before a run, the page first counts one generated lorem block with the official Responses input-token-count endpoint, scales the number of blocks toward the selected input-token target, then counts the exact calibrated prompt for each selected model. If a streamed terminal response reports zero/missing input tokens, that counted value is used for displayed input usage and cost instead of incorrectly treating the request as output-only.
- HTTP 429 responses retry up to twice with exponential backoff. Retry timers are reset for every attempt, avoiding backoff time in the subsequent measurement.

## Results clipboard

Use **Copy results to clipboard** above the results card to copy a Markdown table of the completed aggregate results, including aggregate visible-output, cached-token, and short-completion metrics. The Detailed results table retains one row per completed attempt, including total, reasoning, and visible output tokens. Use **Copy debug to clipboard** to copy redacted API diagnostics: stream event types, terminal usage, response metadata, and errors (never model output text). Both buttons remain disabled until the relevant data exists. A green confirmation is shown for two seconds after a successful copy.

## Content Security Policy

The page includes a CSP before its inline script. It permits connections only to `https://api.openai.com`, disables plugin objects, form submissions, and base-URL changes, and authorizes the exact embedded script with a SHA-256 hash. This is not circular: the hash covers the script contents, not the HTML document or CSP meta tag. Regenerate the hash whenever the script changes; otherwise browsers will block the changed script. Inline styles remain permitted because the standalone page includes CSS and bounded result-bar widths.

## Running

There is no build step or backend:

```sh
python3 -m http.server 8000 --directory oai-models-speedtest
```

Then browse to `http://localhost:8000/demo.html`.
