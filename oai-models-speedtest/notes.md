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
