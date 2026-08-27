# Anomalo roadmap deck

Customer and prospect roadmap briefing. 15 slides, about 25 minutes, plus 3 appendix
slides. Self-contained HTML — open `Anomalo-Roadmap.html` in a browser, no server needed.

**Arrow keys** or click the left/right edges to navigate. **N** opens the presenter
script. **Esc** closes it. `Cmd/Ctrl+P` prints to PDF at 16:9.

## Working on the talk track

Everything you'd want to edit is in **`talk-track.md`** — one section per slide, plain
prose. Edit it, then:

```
python3 build.py
```

That regenerates `Anomalo-Roadmap.html`. Reload the browser. No dependencies.

The build fails loudly if the track and the slides disagree — a slide with no script,
or a script for a slide that doesn't exist. It also prints the running time, so you can
see immediately what a rewrite costs you.

Durations in the headings are estimates at roughly 140 words per minute, not measured.
Treat them as a budget, not a stopwatch.

## Files

| | |
| --- | --- |
| `talk-track.md` | The spoken script. **Start here.** |
| `slides.html` | Slide markup and CSS. Contains a `/*__FONTS__*/` marker the build fills in. |
| `build.py` | `slides.html` + `talk-track.md` + `fonts.css` → `Anomalo-Roadmap.html` |
| `Anomalo-Roadmap.html` | Built output, committed so it can be opened or shared directly. |
| `fonts.css` | Archivo, IBM Plex Sans and IBM Plex Mono as base64 woff2. |
| `fonts.py` | Regenerates `fonts.css` from Google Fonts. Only needed if the typefaces change. |
| `qa.py` | Screenshots every slide and reports overflow, clipping and out-of-bounds elements. Needs `playwright`. |

Fonts are embedded rather than linked so the deck can't lose its typography mid-talk on
bad conference wifi. That's most of the file size.

## Before this is presented

- **Dates are placeholders.** Sep / Oct / Nov 2026 on the roadmap slide are invented.
- **Streaming connectors has no Linear project**, so its November date is the softest
  number in the deck.
- **Confirm the customer-facing names** for Autopilot and First Responder. Both were
  renamed internally as recently as 19 Aug 2026.
- **Table status refresh is not in the deck yet.** Prototype PR is
  `datagravity-ai/dquality#36330`. It needs a product section, a date, and a decision
  on whether it earns a slide or only a roadmap line.

## Structure

Anchored on the three products, which is the same frame customers saw in the June deck.
Every content slide carries its product in the top-right corner, so the anchor is
referenced throughout rather than shown once and abandoned.

Sections run **Monitoring and Quality → Data Intelligence → Data Context**, unnumbered.
That order opens on alert fatigue (the most widely felt pain, and a continuation of
June's deep-dive) and closes on the two-way MCP story, which is the strategic payoff.

| Section | This quarter |
| --- | --- |
| Data Monitoring and Quality | First Responder + Incidents · Copilot Phase II · Streaming connectors |
| Data Intelligence | Autopilot |
| Data Context | Anomalo MCP · MCP Connectors · Native result tables |

Slide 5 is the load-bearing one: what June promised against what shipped. Three shipped
(one early, one past spec), two grew in scope and carried over. Everything after it is
easier to believe because of it.

Native result tables has no slide of its own — it appears on the anchor, on the roadmap
with a date, and in one line on slide 13. Full detail is appendix A3.

Appendix slides A1–A3 hold material cut for time: the agent's context-and-instructions
detail, Autopilot's data-aware triggers, and native result tables. They are numbered
separately and excluded from the running time.
