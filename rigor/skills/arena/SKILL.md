---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
---
<!-- Adapted from pstack/skills/arena (pstack by Lauren Tan, MIT). Modified for Claude Code: see rigor/README.md. -->
# Arena

Fan out N parallel attempts at the same task. Read every candidate end to end. Pick the strongest as the base. Graft the best ideas from the others into it. Verify the synthesized result.

## Start

Open a todolist with one entry per phase before launching anything. The arena runs autonomously and the list keeps phases from silently disappearing.

1. Frame
2. Fan out
3. Cross-judge
4. Pick
5. Graft
6. Verify

## Phase A: Frame

The N candidates will receive the same prompt, so the prompt is the contract. Get it right before spawning anything.

1. State the artifact each candidate is producing.
2. Derive the rubric. State what success looks like for *this* task, then turn it into 3-6 concrete gradeable criteria. Concrete: `Adds a --dry-run flag that skips writes`. Vague: `code is correct`. The rubric is the picker's tool in Phase D; candidates only see the task.
3. Pick the runners.

   <!-- RUNNERS: edit this block to change the roster. See rigor/README.md for the cross-vendor opt-in. -->

   Default to four: two on `opus`, two on `sonnet`. Give each a different *starting bias* so they explore rather than converge (for a design: one minimal-surface, one extensible, one that optimizes the caller's ergonomics, one that redesigns from first principles). Spawn more when the arena covers multiple design directions. Same tier N times is fine when the work is generation-bound rather than judgment-sensitive.

   Every runner is a Claude model, so the candidates are correlated in a way the original cross-vendor version was not. That does not break the arena, but it changes how you read convergence. See Phase E.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`). N candidates writing to the same path is shared mutable state and fails the the **separate-before-serializing-shared-state** principle skill test.

## Phase B: Fan out

Spawn all N runners in one message with the `Agent` tool, `subagent_type: "general-purpose"` and `run_in_background: true`, each with the task, the path to the shared grounding, its own output path, its starting bias, and instructions to produce both the artifact and a short rationale.

The rationale is mandatory. Without it, the parent cannot tell whether a candidate's structure is principled or accidental, which makes Phase E grafting unreliable. Each rationale names the alternatives the candidate considered and what it rejected.

If a candidate fails to produce output, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all Phase B candidates complete, spawn one read-only judge (`subagent_type: "Explore"`). Use a cross-vendor judge when one is configured; it is the only arm not sharing the runners' priors and is worth the most here. Otherwise use a different Claude tier from the runners' majority, and treat the judge as a second opinion rather than an independent check. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with the parent's reading in Phase D, not with the candidates themselves. Spawning while candidates are still writing means the judge sees partial or empty outputs and reports them as dropouts.

## Phase D: Pick a base

Read every candidate end to end before picking. Skimming N candidates surfaces only the candidate whose surface looks most familiar.

Score each candidate against the rubric criterion by criterion, not on holistic feel. Compare against the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base on which candidate a future maintainer can extend most easily without breaking invariants. Prefer the cleaner boundary or smaller surface area when two feel tied, per the Laziness Protocol.

Record the pick and the reason in a short synthesis note alongside the base artifact, including the cross-judge's verdict.

## Phase E: Graft

Walk each losing candidate once more and identify what is worth porting into the base. The signal is usually one or two things per candidate, not most of it.

Fold each graft in by hand, per the **redesign-from-first-principles** principle skill. Don't paste mechanically. The result has to remain coherent under one mental model.

Record what was grafted, from which candidate, and what was rejected and why. The rejection notes are the highest-signal part of the record. Future readers learn from what you considered and dropped, not just what you kept.

When N candidates converge on the same shape, note it in the record. **Do not read same-family convergence as proof the shape is right.** Four Claude runners agreeing may reflect shared training priors rather than a correct answer, and the failure mode here is worse than in review: convergence tempts you to ship the consensus unexamined. Convergence buys you one thing only, that no runner found a better shape under its bias. It does not license skipping Phase F, and it does not mean no graft was available. Re-read at least the two most different rationales for a rejected idea worth folding in. If a cross-vendor runner or judge took part and *also* converged, that is genuinely strong; say so explicitly, and say the opposite when it is absent. When N candidates wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

The synthesized artifact has to hold up under the same scrutiny as any other output, per the **prove-it-works** principle skill. The arena does not earn you a pass.

If verification surfaces a problem the arena did not catch, either Phase A was wrong (re-frame and re-run) or one candidate caught it and you missed the graft (go back to Phase E). Don't paper over.

## Outputs

One synthesized artifact. One short synthesis note alongside, naming the base, the grafts (with source candidate), the rejections, the dropouts if any, and the verification result.
