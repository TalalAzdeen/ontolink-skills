# Quickstart

1. Install the coordinator and seven phase skills. Resolve engineering adapters separately.
2. Initialize one state at the real project root. Never overwrite an existing state to clear blockers.
3. Query `context`; read only the returned `workflow_skill` and relevant source excerpts.
4. Perform the phase work and create real artifacts and proof files under that root.
5. Hash each artifact and proof file with SHA-256. Register the artifact, then evidence supporting its exact current content hash.
6. Record required outcomes with the observed revision. Query again after a handoff.

```sh
python skills/ontolink-skills/scripts/mediator.py record   --state /path/to/project/knowledge.owl --input /path/to/project/record.json --expected-revision 0
python skills/ontolink-skills/scripts/mediator.py context   --state /path/to/project/knowledge.owl --task task-build --budget 4000
python skills/ontolink-skills/scripts/mediator.py validate   --state /path/to/project/knowledge.owl
```

Read the coordinator's [record contract](../skills/ontolink-skills/references/record-contract.md) for exact field names and allowed values. `project` is the project relationship ID. `belongsTo` is generated automatically for project records. State writes use an exclusive lock, compare the expected revision, and replace the file atomically. On conflict, reread rather than forcing the write.

The example project is synthetic initialization data with seven incomplete phase tasks. The JSON signal examples are illustrations, not real assessments or claims about an application. Preserve unknown uncertainty values by omitting `value`.

Use a task-focused query to inspect blocked work. If no task is ready, resolve the reported blocker or dependency instead of advancing a phase. Recording a recommendation does not execute it. Recording a message does not transmit it.
