# cursor-plugins

A fork of [cursor/plugins](https://github.com/cursor/plugins) trimmed to one plugin, plus a port
of its portable core to Claude Code.

## What's here

| Directory | For | What it is |
|:--|:--|:--|
| [`pstack/`](pstack/) | Cursor | Lauren Tan's rigorous-engineering plugin: 44 skills, the `poteto-mode` router, and 22 playbooks. Unmodified from upstream. |
| [`rigor/`](rigor/) | Claude Code | pstack's provider-agnostic core, ported. The 21 principles, `unslop`, and six reasoning skills. |

Everything else from the upstream marketplace (the other 12 Cursor plugins and the 20 third-party
integrations) has been removed. Recover any of them from git history, or from
[upstream](https://github.com/cursor/plugins).

## pstack, in Cursor

```
/plugin marketplace add johnjoo1/cursor-plugins
/plugin install pstack
```

Then `/setup-pstack` to choose your models, and `/poteto-mode` at the start of any task that
needs rigor. See [`pstack/README.md`](pstack/README.md) and the
[guide](pstack/docs/guide/README.md).

## rigor, in Claude Code

These are plain skills. No plugin manifest, no install command.

```bash
cp -r rigor/skills/* ~/.claude/skills/
```

The port drops what only works in Cursor (Graphite stacking, bugbot, cloud agents, transcript
mining, the `.mdc` model-config rule) and rewrites the multi-model fan-out for Claude Code's
`Agent` tool. One caveat carries through the whole thing: pstack's review skills derive their
signal from *cross-vendor* model diversity, which Claude subagents cannot provide, so
same-family agreement is weaker evidence than the original rubric assumes. Each affected skill
says so. See [`rigor/README.md`](rigor/README.md) for the full list of changes, the known
limitations, and the optional cross-vendor reviewer.

## Repository structure

```
.
├── .cursor-plugin/
│   └── marketplace.json    # Cursor marketplace manifest (lists pstack)
├── pstack/
│   └── .cursor-plugin/
│       └── plugin.json     # per-plugin manifest
├── rigor/
│   └── skills/             # Claude Code skills, copied to ~/.claude/skills/
├── schemas/                # JSON schemas for the manifests
└── scripts/
    └── validate-plugins.mjs  # run by CI on manifest changes
```

`rigor/` is deliberately absent from `marketplace.json`. It is not a Cursor plugin, so the
validator does not inspect it.

## License

MIT. `pstack/` and `rigor/` each carry their own LICENSE with Lauren Tan's copyright.
