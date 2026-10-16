# Mandatory Ontology-First Workflow

Before research, opening arbitrary Markdown/spec files, or editing code, read and follow .ontolinkRule/ONTOLOGY-FIRST.md. The first project action is to query the canonical project ontology:

    python .agents/skills/ontolink-skills/scripts/mediator.py context --state knowledge.owl

If knowledge.owl is absent, bootstrap it through the installed OntoLink mediator and then run context. Read only packet-listed artifacts and the selected phase skill. Never hand-edit ontology state; use mediator record with the observed expected revision. Enforce strict phase order and require current PASS evidence with exact SHA-256 hashes before marking a task DONE.
