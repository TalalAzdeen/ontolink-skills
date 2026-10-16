# Mandatory Ontology-First Rule

Before researching, inspecting arbitrary Markdown/specification files, or editing code, follow .ontolinkRule/ONTOLOGY-FIRST.md.

First action in the target project: run the mediator context command against root knowledge.owl. If the ontology is missing, bootstrap it through the installed OntoLink mediator and then query context. Use the returned packet to select the single eligible task and read only the artifacts/contracts it lists. Never edit knowledge.owl manually; all state writes require the mediator and the expected revision. Enforce phase order and require current PASS evidence with exact SHA-256 hashes before marking tasks DONE.

This rule applies to every AI agent and every new session/task in this repository, subject to higher-priority platform and safety instructions.
