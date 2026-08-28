# rigor

The provider-agnostic core of [pstack](https://github.com/cursor/plugins/tree/main/pstack),
adapted to run on Claude Code.

pstack is Lauren Tan's ([poteto](https://x.com/poteto)) rigorous-engineering plugin for Cursor:
44 skills, a router called `poteto-mode`, and 22 playbooks. Much of it is engineering judgment
that has nothing to do with Cursor. The rest is wired to Cursor's Task API, Graphite, bugbot, and
a multi-vendor model roster.

This directory is the first part, ported. Credit for the substance goes upstream; the mistakes in
the translation are mine.

## Install

These are plain Claude Code skills. There is no plugin manifest and no install command.

```bash
cp -r rigor/skills/* ~/.claude/skills/
```

`~/.claude/skills/` makes them available in every project; a project's `.claude/skills/` scopes
them to that repo. Claude Code watches both directories, so they appear without a restart.

If you later want to share these with a team, drop a `.claude-plugin/plugin.json` into the folder
and it loads as a plugin in place. Nothing needs restructuring.

## What's here

**`rigor-mode`.** The router, and the thing that makes the rest fire. Carries an inline index of
all 21 principles with their trigger conditions, plus routing rules for the other skills, the
autonomy posture, and the reply and comment style rules. Invoke `/rigor-mode` at the start of a
task that needs care. Rebuilt from pstack's `poteto-mode`, minus its 22 playbooks and the ten
routes to skills this port does not include.

**The principles** (21 skills, `principle-*`). Laziness Protocol, Model the Domain, Type System
Discipline, Boundary Discipline, Minimize Reader Load, Prove It Works, Fix Root Causes, Sequence
Verifiable Units, Build the Lever, and the rest. Each states when it applies, why, and a
falsifiable test question. All carry `disable-model-invocation: true`, so they load when cited or
invoked by name rather than on every turn. Copied verbatim.

**`unslop`.** Thirty-one numbered AI-writing tells with a fix for each. Copied verbatim.

**`epistemics`.** Grades every claim as Direct, Supported, Inferred, Speculative, or Unknown, and
polices the phrasing each tier licenses. Promoted from a reference file inside pstack's `why`
skill into a skill of its own, with an output contract added so it stands alone.

**`blast-radius`.** What a change breaks somewhere else. Carries the evidence ladder: *you said
so → you pointed at the line → you showed the bad case can't happen → you ran it → you reproduced
it in the app*. Get each safety fact as far down as is cheap, then say where it stopped.

**`interrogate`.** Adversarial review by several reviewers, triaged into Act on / Consider /
Noted / Dismissed. Ships pstack's rubric, code-quality lens, and lead-judgment framework, which
between them are the best material in the plugin.

**`arena`.** N parallel candidates at one task, cross-judged, best base picked, strongest ideas
from the losers grafted in.

**`architect`.** Design before implementing: ground, sketch, agree, implement, scrap. Calls
`arena` for the parallel exploration. Ships the design red flags (shallow module, information
leakage, temporal decomposition, pass-through method) and a rationale template.

**`decision-log`.** An append-only TSV trail for long or unattended runs, one row per decision,
evidence as a pointer rather than prose. Was `show-me-your-work` upstream.

## How the principles load

Two tiers, inherited from pstack. `rigor-mode` carries a ~39-line **index** naming all 21
principles and the condition each applies to; that is always in context once the mode is invoked.
The **leaves** are 487 lines total and load only for the principles you actually apply. Roughly
12x compression, so you always know which principle is relevant without paying for all of them.

The forcing function is a rule, not a mechanism: a citation must name the decision it changed. A
principle named in a reply with no choice behind it means the leaf was never read.

Every leaf carries `disable-model-invocation: true`, so nothing auto-fires. Without `/rigor-mode`
citing them, the principles sit inert — that is by design, and it is why the router exists.

## The caveat that matters

pstack's review skills rest on **decorrelated error**. `interrogate` says the adversarial signal
comes from model diversity, *not assigned personas*. `show-me-your-work` requires a reviewer on a
different model family because "self-review is not a substitute; the point is fresh eyes you
cannot bring yourself."

Claude Code's `Agent` tool takes Claude models only. So every reviewer here is a Claude model, and
their errors correlate. Distinct lenses (correctness, structure, security) are the compensation,
and pstack explicitly calls personas the weaker mechanism.

This is stated inside each affected skill rather than buried here, because an agent reading
`interrogate` mid-task needs to know it. The short version:

- Same-family agreement is **moderate** evidence, not high confidence.
- A lone dissent is worth more than its count suggests, because correlated reviewers
  under-produce disagreement.
- Consensus never replaces tracing the path yourself.

**`arena` Phase E is the sharpest case.** Upstream it reads: when candidates converge, that is a
strong signal, ship the consensus shape. Across vendors that holds. Across four Claude runners,
convergence may only reflect shared priors — and unlike a review, where correlation just inflates
a verdict, here it can make you *ship* the wrong thing unexamined. The ported Phase E says
convergence does not license skipping the graft or the verification.

## Cross-vendor reviewer (optional)

Because Claude Code subagents can't be another vendor's model, a genuinely decorrelated reviewer
has to be a tool call rather than a subagent. Two ways:

**MCP (preferred).** Run an MCP server exposing an "ask Gemini" tool. The skill calls it as a
tool, the key lives in MCP config, and nothing shells out from markdown.

**Script.** `skills/_shared/ask-vendor.sh` reads a prompt on stdin and returns a completion. It
needs `GEMINI_API_KEY` in the environment (`GEMINI_MODEL` optional, defaults to
`gemini-2.5-pro`). It exits 2 when no key is set, which is the "when present" test the review
skills perform — a non-zero exit means fall back to same-family and state the caveat.

```bash
echo "$PROMPT" | rigor/skills/_shared/ask-vendor.sh
```

Never commit a key.

Note this works only where the network allows it. Claude Code on the web routes through a proxy
whose policy is set per environment; as of writing, `generativelanguage.googleapis.com` is
reachable from that sandbox while `api.openai.com` and `openrouter.ai` are not. Local sessions
have no such restriction. The unconfigured fallback and every failure path were tested; the
configured path was not, because no key was available.

## Known limitations

**A cross-vendor reviewer is one-shot, not agentic.** Both paths above return a single completion
over whatever prompt you supply. Claude-side reviewers are subagents that read, grep, and explore
before forming an opinion. A one-shot reviewer cannot. The cost is uneven, so it's worth knowing
per skill rather than as a general warning:

| Skill | What its reviewer needs | Impact |
| :-- | :-- | :-- |
| `interrogate` | the diff, the rubric, the intent | **Low.** The diff *is* the context. Near parity. |
| `decision-log` | the trail plus the artifacts it cites | **Low.** Finite text that pastes cleanly. Its best use, since judgment review is exactly where decorrelation pays. |
| `architect` | grounding, then a design sketch | **Medium.** Claude must ground first and pass it in; the candidate is then producible from a prompt. |
| `blast-radius` | to go and find what grep won't show | **High.** Its stated job is "the breakage grep won't show you." A model that sees only what you pasted cannot do that job. |

So: enable it freely for `interrogate` and `decision-log`, pass grounding explicitly for
`architect`, and treat a cross-vendor arm on `blast-radius` as a weak signal that must not be
weighed against the agentic arms or stand in for a rung-4 proof.

Worth revisiting if an *agentic* cross-vendor path appears — an MCP server that can itself read
the codebase, rather than a bare completion endpoint. That would close the gap for
`blast-radius` and `architect` and make the whole decorrelation story work as pstack intended.

## Deliberately not ported

`swarm` (Cursor cloud agents), `why`'s source orchestration (needs Linear/Slack/Sentry MCP
fan-out; its epistemics reference is here, its investigators are not), `reflect` and `recall`
(both read Cursor transcript paths), `setup-pstack` (writes a Cursor `.mdc` rule), `how`,
`figure-it-out`, the `automations/benny/` subtree, and the shipping / autopilot / babysit
playbooks (Graphite and bugbot). pstack's 22 playbooks are not ported; they assume Graphite stacking and
bugbot. `rigor-mode` replaces `poteto-mode` as the router, without them.

`architect` Phase A upstream delegates grounding to `how`. Since `how` isn't here, the ported
version states the grounding requirement in prose instead.

## Changes made in porting

1. Model slugs became roles and Claude tiers. No dated model IDs anywhere.
2. Cursor's `Task` became the `Agent` tool; `readonly: true` became `subagent_type: "Explore"`.
3. The `~/.cursor/rules/pstack-models.mdc` lookup was dropped. Each skill carries its roster in
   one marked block, so changing it is a local edit.
4. Cross-plugin dependencies (`deslop`, `create-skill`, `bugbot`, `control-ui`, `control-cli`)
   were repointed or dropped.
5. Transcript mining was removed, not repointed.
6. Cursor-only frontmatter (`mode`, `icon`, `color`, `reminder`) was dropped.
   `disable-model-invocation` was kept; Claude Code supports it and it means the same thing.
7. The correlation caveats above were added.

Every modified file carries a comment naming its upstream source. The 21 principles, `unslop`,
and the reference files under `interrogate/` are unmodified.

## License

MIT, carrying pstack's copyright. See `LICENSE`.
