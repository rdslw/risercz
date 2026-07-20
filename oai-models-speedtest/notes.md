# Working notes

- Created investigation folder and began by inspecting repository guidance.
- Retrieved the Simon Willison reference HTML from GitHub and reused its core palette, card, control, spinner, and table conventions.
- Direct curl requests to OpenAI documentation and pricing endpoints returned HTTP 403 in this environment; no API key was available for live smoke tests. The demo therefore includes editable price defaults and browser-side mock validation.
- Implemented a standalone Responses API streaming benchmark: shuffled attempts, `service_tier: "priority"` fast mode, first text-delta TTFT, terminal usage-based costs, cap preflight, 429 backoff, partial results, and editable rates.
- Explicitly preserved all requested model names. Because no API key was available, models were not substituted or treated as confirmed available.
- Checked the embedded script with `node --check`. An initial jsdom load lacked a browser origin, so I reran it with a localhost URL: the UI rendered 12 selected base-set model/mode rows and a results placeholder.
- A static-server smoke test could not be retained by this execution environment after the shell exited, so a browser screenshot was not available here.

## Follow-up fixes (post-review)

- **Timer-reset bug**: `start`, `first`, `text`, `usage` were captured/initialized before the retry loop, so if retry 0 received a 429 and slept 1–2 s, the subsequent attempt's TTFT and total latency were inflated by the sleep duration. Additionally, a network error mid-stream could leave `first` set from the partial read, poisoning the retry's TTFT. Fixed by moving all four variable assignments inside the loop (beginning of each retry iteration).
- **API key save event**: Changed from `change` (fires on blur) to `input` (fires on every keystroke) so the key is persisted to localStorage immediately, even if the user types it and clicks Run without clicking away first.
- Follow-up: added a hash-based CSP before the inline script. The script hash is generated from the script block only, so it is not circular with the CSP meta element that carries it; the hash must be regenerated when the script changes.
- Updated the setup UI with explicit key saving/status, range sliders for 1–20 tries and generated 10K–100K input/2K–20K output workloads, expected row costs, and a pre-run budget disable guard.
- Retrieved `https://raw.githubusercontent.com/simonw/llm-prices/main/data/openai.json` to set normal-mode defaults for all six requested models. FAST rows use the published 2× priority-processing rate.
- Refined output semantics: the selected requested output is now an explicit generated-output target, while the API `max_output_tokens` is set to twice that target for headroom; expected maximum cost uses that API cap.
- Updated the workload to use repeatable diceware-word output blocks: one 1,000-word, one-word-per-line block per 2K requested output tokens, with deterministic counter-line instructions every 100 words.
- Made prompt-preview markers inline with their labels and added a total sequential-time estimate in minutes beside the expected total cost.
