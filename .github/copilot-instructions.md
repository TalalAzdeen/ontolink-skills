# Mandatory Ontology-First Workflow

Before research, opening arbitrary Markdown/spec files, or editing code, follow .ontolinkRule/ONTOLOGY-FIRST.md. First run from the target project root:

    python .agents/skills/ontolink-skills/scripts/mediator.py context --state knowledge.owl

If knowledge.owl is absent, bootstrap it through the installed OntoLink mediator and then run context. Use the returned packet to select the eligible task and read only the listed artifacts/contracts. Never hand-edit knowledge.owl; use mediator record with the observed --expected-revision. Enforce strict phase order and require current PASS evidence with exact SHA-256 hashes before DONE.
