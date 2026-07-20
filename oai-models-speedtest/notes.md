# Working notes

- Created investigation folder and began by inspecting repository guidance.
- Retrieved the Simon Willison reference HTML from GitHub and reused its core palette, card, control, spinner, and table conventions.
- Direct curl requests to OpenAI documentation and pricing endpoints returned HTTP 403 in this environment; no API key was available for live smoke tests. The demo therefore includes editable price defaults and browser-side mock validation.
- Implemented a standalone Responses API streaming benchmark: shuffled attempts, `service_tier: "priority"` fast mode, first text-delta TTFT, terminal usage-based costs, cap preflight, 429 backoff, partial results, and editable rates.
- Explicitly preserved all requested model names. Because no API key was available, models were not substituted or treated as confirmed available.
- Checked the embedded script with `node --check`. An initial jsdom load lacked a browser origin, so I reran it with a localhost URL: the UI rendered 12 selected base-set model/mode rows and a results placeholder.
- A static-server smoke test could not be retained by this execution environment after the shell exited, so a browser screenshot was not available here.
