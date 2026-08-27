# Talk track

One section per slide, in deck order. The build script reads this file and puts it
in the presenter drawer (press **N** in the deck).

Format, and it is strict:

- `## <slide number> · <title> — <m:ss>` starts a slide. The number and the duration
  are both parsed; the title is for you, not the deck.
- Every blank-line-separated paragraph is a spoken paragraph, rendered in white.
- A paragraph beginning with `> ` is a presenter cue, rendered in amber under a
  "Watch for" heading. Cues are for you; they are not meant to be said.
- Slides 16-18 are the appendix and are not counted in the running time.

Rebuild after editing: `python3 build.py`

## 1 · Cover — 0:30

Thanks for making the time. Same deck as June — same title, deliberately, because the story hasn't changed. What's changed is how much of it is real.

Twenty-five minutes, and I want to spend a good chunk of it showing you working software rather than slides. I'll start with what we promised you in June and what actually landed — including the two things that didn't.


## 2 · Disclaimers — 0:20

Housekeeping. This is confidential and it's directional — we ship weekly and we re-prioritize on what we hear from you, which is part of why I'm here. Nothing on the roadmap slide is a contractual commitment.


## 3 · Forward-Looking Statements — 0:10

And the legal page. I'll let you read that on your own time.

> Ten seconds. Don't read it aloud.


## 4 · The world is changing — 1:00

The premise hasn't changed since June, so I'll be quick.

Agents are already doing the routine work of a data team. And they don't just report — they act.

Which means they don't wait for clean data. A human who sees something odd stops and asks. An agent takes the number and moves on.

So bad data stops being a slow embarrassment and becomes a fast, silent one, at scale.

And that turns data quality from a reporting problem into an AI infrastructure problem. Every agent you deploy inherits the trustworthiness of the data underneath it.

Hold on to that. I'll come back to it at the end.

> The callback lands on slide 13. Flag it here so it pays off there.


## 5 · What we said in June. What shipped. — 1:35

Before I ask you to believe anything about this quarter, the scorecard on last quarter. Five things were on the June deck. Three shipped.

High-cardinality entity checks — per-segment logic that holds up when an entity has thousands of segments.

Lineage expansion, and it shipped bigger than we promised. We committed to column-level lineage for Snowflake and Databricks. You also have BigQuery, which was not in that commitment, plus an OpenLineage connector — so lineage across sources, not just inside one warehouse.

Global AIDA shipped early. The June deck put it in Q3; it landed ahead of that.

Two didn't ship. Co-Pilot Phase II is in build now, and the scope grew to include table configuration. First Responder is in build now, and it's materially bigger than that June slide described — a triage agent plus the entire incident layer around it. I'd rather show you that in a minute than defend the date.

Three shipped, one early, one past spec. Two grew and are in flight. Those two lead this quarter.

> Say “early” and “past what we promised” out loud — they buy credibility for everything after this.

> If pressed on the First Responder slip: it had to get cheap enough to run on every alert. Dogfooding drove per-run cost down roughly fiftyfold. Technical rooms only.


## 6 · Three products. One platform. — 1:00

Same frame as June: three products, one platform. Seven things this quarter, and this is where they land.

Monitoring and quality gets three — First Responder, Copilot Phase II, and streaming connectors.

Data intelligence gets Autopilot.

And data context gets three: our own MCP server, MCP connectors, and native result tables.

Two things worth flagging before we start. Not all of this is AI — the streaming work has nothing to do with agents. And we're going in that order, ending on data context, because that's where “one platform” stops being an architecture diagram and turns into something you can plug into.

> This is the map. Every slide from here carries its product in the top right corner, so nobody has to hold the structure in their head.


## 7 · First Responder — 5:30

First Responder. The problem isn't that you don't have alerts — it's that a person has to be the first pair of eyes on every one. That's the job we're taking away.

It judges first: is this real, how bad is it, where does it rank against the runbooks you've defined. It runs an initial investigation before it decides anything.

Then it investigates properly — traces root cause using lineage, check history and live queries, and cross-references issues you've already resolved.

Then it acts. Ignore it, if it's noise or a false positive. Escalate with the whole investigation attached, so the human starts where the agent finished. Or open the ServiceNow or Jira ticket itself.

! DEMO — 4 min. Take one real failed check through the agent end to end: the alert, the agent's reasoning, the investigation it ran, and the incident it produced. Let them read the agent's actual write-up on screen. Do not narrate every field.

What's new since June is that all of it lands inside an incident. Twenty checks failing across six tables over three days because of one upstream problem is one incident, not twenty alerts — grouped using lineage and your documentation. Noise gets silenced and auto-resolved. Everything else gets routed to the right person.

> If asked about acting on the fix — re-run the pipeline, open a PR — hold it until slide 13, which is what makes it possible.


## 8 · You stay in control of the agent — 1:20

The question you should all be asking is what happens when it's wrong. Three answers.

You can see what it silenced. A daily or weekly digest of every alert suppressed or re-routed, and in-app filtering by what the agent did. The failure mode we worry about most is an agent that gets too good at quieting things down — this is how you catch that before it costs you.

You can override anything. Status, resolution, grouping. The rule we hold ourselves to: anything the agent can do to an incident, a human or an API call can undo.

And it learns from the override. You comment with feedback, that becomes memory, the correction goes into the runbook. You are not having the same argument with it every week.

Incidents also carry live links into Jira, ServiceNow and Linear. This has to work inside your incident process, not beside it.

> Enterprise and regulated buyers block here. Don't rush it even if you're running long.


## 9 · Copilot — 1:45

Copilot is the assistant surface across the product, and a fair amount of it is already live. So let me split this one: what you can do today, and what lands this quarter.

Today, you can ask questions of your data in plain language and get answers that use everything Anomalo knows about it — not just the table, but the documentation, the lineage, the history.

You can create custom data quality checks by describing them, instead of writing the SQL or filling in a form.

And on any visualization or any check result, you can ask it to explain, dig deeper, investigate. That's usually where people actually start.

What lands this quarter is the part that scales. And it's worth saying why, because some version of this sentence has been said to me by nearly every platform lead I've met: rolling out monitoring across ten thousand tables isn't a feature, it's a project, and we don't have the people for it. That's fair.

So — table configuration through AIDA. Describe how a table should be watched, which segments matter, what to ignore, how fresh it needs to be, and AIDA configures it. And bulk check creation and cloning, across many tables in one instruction.

Copilot gets coverage on. First Responder keeps it quiet. Two halves of the same job — and those two on the right are June's Co-Pilot Phase II landing.

> The ten-thousand-tables line is spoken, not on the slide. Quotes land better said than read — and if someone in the room has said it to you personally, use their words instead.

> If anyone asks why conversational analytics appears here when slide 6 files it under Data Intelligence: AIDA is one assistant, and Data Intelligence is the capability it delivers. Copilot is the surface. Don't volunteer the distinction.


## 10 · Streaming connectors — 1:10

One more in monitoring, and this one has nothing to do with AI.

Right now your detection floor is your load frequency. Data that arrives as a stream is only monitorable once it lands somewhere we can query. Hourly loads mean you can't know in under an hour. Overnight loads mean you find out tomorrow — and by then it's been read.

This quarter we connect straight to the source: Kafka, Kinesis, Pub/Sub. Checks evaluated against the stream, over windows you define. And when one fails it raises the same incident and goes to the same First Responder.

I'm flagging that this isn't an agent feature on purpose. It's infrastructure — and it's what decides whether the agents have anything current to look at.

> The “not everything is an agent” line is doing real work. A roadmap that's seven-for-seven AI reads as bandwagon; this one item makes the other six more credible.


## 11 · Autopilot: reporting nobody has to write — 4:50

Into data intelligence. Autopilot.

Rather than walk you through the configuration, let me tell you what it gets you.

Monday's report is already written. Every domain owner opens a written summary instead of a dashboard — what broke last week, what changed, what deserves a look — in prose, by the agent. Nobody assembled it, and more to the point, nobody had to remember to.

It's timed to your data, not the clock. The analysis of last night's load exists because the load finished, not because it turned eight. When the pipeline runs late, the report waits. Anyone who has opened a scheduled report that confidently described data which hadn't landed yet knows why that matters.

And this is the one that changes the arithmetic: one definition, every domain. You set the job up once and it fans out — a report per domain, per table, per data product, each written about its own data. That's coverage you'd otherwise staff with an analyst per team.

! DEMO — 3 min. Show one Autopilot-generated report, in full, on screen. This slide makes three claims and offers no evidence for any of them; the report is the evidence. If there is only time for one demo in the whole deck, make it this one.

It also lands June's data intelligence promise, in June's own words: formatted recurring reports through conversation, iterate on templates with the agent, publish as HTML or slides. Conversational analytics and Global AIDA already shipped. That leaves natural-language dashboards as the one piece still to come.

> The slide is deliberately thin. Three headlines and a line each — the detail above is yours to say, not theirs to read. If you find yourself reading the slide aloud, you've lost the room.

> If someone asks how you set one up, the four-step definition is appendix A2. Don't volunteer it — the configuration surface is the least interesting thing about this product.


## 12 · Anomalo speaks agent. In both directions. — 1:10

Data context. And this is the slide I'd most want you to remember.

Everything so far lives inside Anomalo. This one is about the boundary.

One protocol — MCP — implemented in both directions.

Going right, we're a server. Your agents, whether that's Claude, Cursor or something you built internally, query Anomalo directly. They can ask whether the data is good before they use it.

Going left, we're a client. Anomalo reads your systems: Confluence, your catalog, GitHub, your ticketing.

Both arrows are on one slide because they're the same capability pointed in two directions. The same protocol that lets you consume Anomalo lets Anomalo consume you. That's the moment three products stop being three things that share a login and start being one platform plugged into your stack.

> Slow down. This lands here, after four concrete products, because by now the question in the room is “how does any of this know anything about my company?”


## 13 · What that unlocks — 1:55

Concretely, in both directions.

Ours to you: quality status on demand, so an agent can ask whether a dataset is healthy before it trains on it or reports on it. Documentation and lineage, callable. And Global AIDA, domain-scoped — worth saying that one isn't a promise, it's a capability that shipped this quarter, now reachable outside the product.

Yours to us: wikis, for the business definitions nobody put in the warehouse. Catalogs, whatever you already treat as the source of truth. Code, so the agent can read the transformation that broke instead of only the symptom. Ticketing, so incidents live in the process your team already runs.

Native result tables belong in this section too. Anomalo's own check results and incidents become queryable, so our agents and yours can look them up exactly the way they'd look up a catalog. No S3 pipeline required.

And the payoff. Every agent in this deck gets better the day the left-hand side exists. Documentation written from your wiki instead of from column names. Triage that cites your runbook because it read your runbook. And remember how we opened — agents don't wait for clean data. This is the mechanism that fixes that: not a dashboard someone checks first, but a question your agent asks automatically, every time.

> If someone asks about the agent opening a PR to fix the code: it becomes reachable once the left-hand side exists. Say it's a direction, not a date.

> Full native-result-tables detail is in the appendix if anyone wants the before-and-after.


## 14 · Roadmap — the next 90 days — 1:10

Dates. Two caveats first. These are targets, not commitments — we ship weekly and we re-prioritize. And two items are carried over from June, First Responder and Copilot Phase II. They're marked as such. I'd rather flag that myself than have you find it.

Monitoring and quality: First Responder and Copilot in September, streaming connectors in November.

Data intelligence: Autopilot in October. And natural-language dashboards the quarter after — that's the last outstanding piece of the June vision.

Data context: Anomalo MCP in October, MCP connectors and native result tables in November.

The most useful thing you can do for me in the next few minutes is tell me which of these you'd want first, and which one you'd trade away. That ordering is not locked.

> REPLACE THE DATES before presenting — Sep/Oct/Nov 2026 are placeholders.

> The closing ask is the point of the slide. Don't skip it to save a minute.


## 15 · One platform. Three products. — 0:40

To land it.

One platform, three products — same as June. What's different is that it's starting to drive. It handles the alert before you do. It does the standing work you delegated. And it connects to everything else you run.

Every priority on that roadmap slide moved because a customer pushed on it. So the feedback genuinely matters, on the big initiatives and the small annoyances alike.

What haven't I covered?

> End on the question. The answer is worth more than anything else you'll get in the room.


## 16 · APPENDIX · It follows your runbooks — 1:10

[Appendix — pull up if someone asks how the agent knows what matters at their company.]

On the context side: documentation at the domain and table level, the data itself, column-level lineage, everything AIDA has already learned about your environment, and every incident you've previously resolved along with how.

On the instruction side: you define agents, plural, applied per notification channel — so the team paged about revenue tables can have different judgment than the team watching marketing data. You can override at the individual check. And you control the incident vocabulary: your own statuses, types and tags.

The tension we're managing is flexibility versus clarity. Enough control to encode how your team actually works, without a configuration surface nobody wants to own.

> This was in the main deck at 37 minutes. It's the best objection-handler you have for “it won't know what matters to us.”


## 17 · APPENDIX · How an Autopilot job is defined — 1:05

[Appendix — pull up if someone asks how a job is set up, or conflates Autopilot with scheduling.]

Four things define a job: what the agent looks at, which tables or checks or domains are in scope, whether you want one report or one per item, and what sets it off.

The trigger is the part worth dwelling on. Run when all the tables are fresh, or run per table the moment that table is fresh. A cron job fires at nine whether the pipeline landed or not.

On placement: First Responder answers failures nobody asked for, which is why it sits in monitoring and quality. Autopilot produces analysis you commissioned, which is why it sits in data intelligence.

> If someone pushes on the freshness trigger: the check that noticed is monitoring. What Autopilot adds is the written analysis on top of it.


## 18 · APPENDIX · Anomalo's own data, without the pipeline — 1:05

[Appendix — pull up if anyone asks about the batch exporter or querying their own quality history.]

Today, if you want to query your own quality history, we export results to your object store and then you build a pipeline into your warehouse and model the tables yourself. Several of you have told me that's more work than it should be. You're right.

This quarter those become native tables inside Anomalo. Check results, incidents, metadata — queryable on day one, no S3 hookup, no pipeline, no modelling.

And the reason it sits in data context rather than reporting: First Responder, Autopilot and AIDA all read it the same way they'd read a data catalog. It's a lookup source, not a dashboard.

> Least glamorous item this quarter, one of the most requested. It has no main-deck slide by design.
