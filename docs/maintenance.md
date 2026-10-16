# Maintenance audit and migration

Scope: all tracked files in the distribution were reviewed. `skills/` is the
protected source: no procedures, references, assets, fixtures or metadata in
that directory are changed by this maintenance revision.

## Findings and changes outside skills

| Finding | Action |
| --- | --- |
| Operational rules were duplicated across overview and host instructions | Keep the English README for readers and the canonical operational policy in `.rule/ONTOLOGY-FIRST.md`. |
| Five host files duplicated policy and assumed `.agents/skills` | Keep short discovery pointers; resolve the real installed coordinator path. |
| Legacy `.ontolinkRule/` directory | Rename to `.rule/`; update every external reference. |
| Loose record JSON and generated text had no shared placement rule | Require the fixed `.ontolink/records`, `proofs`, `artifacts` paths. |
| Update refresh depended on manual follow-through | Add the external `.rule/ontolink.py` adapter: record, receipt, validate, context and existing-index refresh. |
| README linked missing `SOURCES.md` | Link the existing bundled `assets/sources.json`; do not create another attribution copy. |
| Optional intelligence tests absent from the main check | Include them and adapter regression tests in `scripts/check.py`. |
| No repository automation | Run maintenance checks on pull requests and pushes through GitHub Actions. |
| Lifecycle mentioned unrelated department/browser operations | Remove that tangential paragraph outside the skills. |

## File classification

| Files | Relation to skills | Decision |
| --- | --- | --- |
| `skills/*/SKILL.md`, `agents/openai.yaml`, phase references | Installable workflow and host metadata | Preserve unchanged. |
| Coordinator scripts, assets, examples and tests inside `skills/` | Runtime, vocabulary, constraints, fixtures and verification | Preserve unchanged. |
| `.rule/` | Shared project integration policy and adapter | Retain outside `skills/`. |
| `AGENTS.md`, `GEMINI.md`, `.cursor/`, `.clinerules`, `.github/copilot-instructions.md` | Host discovery integration | Retain small pointers; do not delete host directories. |
| `README.md`, `docs/`, `catalog.json` | Distribution documentation and catalogue | Retain with distinct responsibilities. |
| `scripts/`, `requirements-dev.txt`, `.github/workflows/` | Repository maintenance and regression verification | Retain outside installed skill packages. |
| `.gitignore` | Repository hygiene | Retain; ignore regenerable context/index and Python caches only. |
| `.ontolinkRule/` | Superseded integration directory | Removed by rename, with migration instructions in the canonical rule. |

No tracked file was demonstrated to be wholly unrelated to distributing,
executing or verifying these skills. Support files outside `skills/` are not
unrelated merely because they are not installable skills. Only redundant prose,
a tangential lifecycle passage and the superseded directory are removed.

## Protected findings and compatibility limits

Phase SKILL.md files and contracts repeat shared bootstrap/evidence wording.
They are intentionally left unchanged under the requested scope. Host rules
supply the new paths without changing the coordinator's payload schema, phase
order, revision guard, evidence rules or canonical-state location.

The coordinator still documents a legacy `record.json` example and its direct
mediator CLI accepts an arbitrary input path. External callers must apply the
new canonical policy or use the adapter; there is no claim that the unchanged
mediator globally enforces the new directory convention. The adapter checks
record-input placement; generated proof/artifact placement is an agent rule.

The optional source indexer has its original traversal and heuristic limitations
and is opt-in. The external adapter refreshes it when enabled; it does not
change its parser, scan policy or generate new canonical facts. A failed index
refresh is reported, and a stale cached packet is removed.

## Safe deletion and update procedure

Follow the canonical rule's migration section. Compare local customizations
before replacing `.rule`; preserve existing host instructions. Verify new
pointers before removing the old `.ontolinkRule` directory. Do not delete all of
`.ontolink`, rewrite registered proof bytes, remove active locks, move application
files, or modify installed skill internals. Preserve original evidence and
receipts; remove only demonstrably regenerable context/index caches.

Run `python scripts/check.py` after each distribution update. Automated CI
checks the repository; each target project still needs `start` after installation
or update to validate its own state. Nothing silently downloads or applies a
remote revision.

## Distribution setup, safe updates and documentation discovery

`project_setup.py` copies all catalogued packages and external rules into an
existing application project. It preserves canonical graph bytes and durable
records/proofs/artifacts, validates incoming compatibility, backs up replaced
paths and merges managed host blocks. Failure restores replaced package/rule
paths; it does not migrate or reset graph data. Tests cover an existing project
with a registered artifact and proof, plus a newly added command.

The English README explains the workflow, installation and updates, with the
approved project-ontology image and the detailed ontology update-cycle diagram. `sitemap.xml` covers
all eight skill entries, their Markdown references and public documentation.
The sitemap is a repository discovery file; Google submission and indexing of a
separately hosted site require that site's real URLs and ownership configuration.
