# OntoLink Skills

Ontology-mediated project execution from discovery through monitoring. OntoLink
selects the current task, phase contracts, dependencies and evidence through a
persistent project graph instead of loading every skill and the full history.

## Install and first use

Install all eight directories from `skills/` through your agent host's supported
skill mechanism. Keep their names and relative contents intact. Engineering
adapters are external and optional. Python 3.10+ is required for the mediator.

Copy `.rule/` into the **target application root**, merge the applicable host
pointer (`AGENTS.md`, `GEMINI.md`, Cursor, Cline or Copilot), and invoke
`$ontolink-skills` with the project goal. The agent resolves the installed
coordinator and automatically runs:

```sh
python .rule/ontolink.py start --root /path/to/project \
  --skill-root /actual/installed/path/ontolink-skills
```

This creates or reuses `knowledge.owl`, validates it and retrieves context.
Installing or copying files alone does not execute setup. Reuse an explicitly
configured canonical state with `--state`; do not create a second graph.

The complete first-use, update, host, naming and cleanup contract is in
[.rule/ONTOLOGY-FIRST.md](.rule/ONTOLOGY-FIRST.md). Keep that policy in one place;
`AGENTS.md` and `GEMINI.md` are discovery pointers, not policy copies.

## Project files

| Path | Responsibility |
| --- | --- |
| `knowledge.owl` | Canonical operational state; mediator writes only. |
| `.rule/` | Shared project rules and external storage/refresh adapter. |
| `.ontolink/records/` | Generated JSON record payloads and receipts. |
| `.ontolink/proofs/` | Generated verification logs and text proofs. |
| `.ontolink/artifacts/` | Generated requirements, plans and handoff text. |
| `.ontolink/context.json` | Regenerable context packet. |
| `.ontolink/index/project-index.json` | Optional, regenerable code index. |

`.ontolink` is a fixed name in **every** project. Application source/configuration
stays in its native directories. Never delete durable proofs or records with a
cache cleanup. The schema in `skills/ontolink-skills/assets/ontolink.owl` is
separate from each project's state; JSON is not a parallel state authority.

## Workflow

| Order | Skill | Required outcome |
| --- | --- | --- |
| Coordinator | `ontolink-skills` | Canonical knowledge, routing and handoffs |
| 1 | `ontolink-discovery` | Requirements and acceptance criteria |
| 2 | `ontolink-architecture` | Reviewed contracts and architecture |
| 3 | `ontolink-planning` | Dependency-aware execution plan |
| 4 | `ontolink-implementation` | Working implementation |
| 5 | `ontolink-verification` | Current verification evidence |
| 6 | `ontolink-delivery` | Authorized delivery and handoff |
| 7 | `ontolink-monitoring` | Observed health and follow-up work |

Record through `.rule/ontolink.py record` to automatically validate and refresh
context after each successful update. An enabled code index is refreshed too.
See [quickstart](docs/quickstart.md) for commands. Direct mediator calls remain
supported and require explicit validate/context refresh by the caller.

## Reference and maintenance

- [Canonical project rule](.rule/ONTOLOGY-FIRST.md): first use, updates and migration.
- [Knowledge model](docs/knowledge-model.md) and [lifecycle](docs/lifecycle.md).
- [Optional Project Intelligence](docs/project-intelligence.md).
- [Validation and limitations](docs/validation.md).
- [Maintenance audit and file classification](docs/maintenance.md).
- [Skill catalogue](catalog.json) and [standards attribution](skills/ontolink-skills/assets/sources.json).

```sh
python -m pip install -r requirements-dev.txt
python scripts/check.py
```

The runtime is a constrained named-node RDF/XML mediator, not a general OWL
reasoner. Hashes check local provenance; agents must inspect proof meaning.
Selective retrieval aims to reduce repeated context, with no universal measured
token saving. Monitoring runs during active use; background operation requires
separate configuration. Message records do not transmit messages.
