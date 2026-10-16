"""End-to-end setup/update tests against existing project data."""
import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('setup_project', ROOT / 'scripts/project_setup.py')
manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manager)


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / 'application'
        self.project.mkdir()
        self.source = self.base / 'distribution'
        self.source.mkdir()
        for folder in ['skills', '.rule']:
            shutil.copytree(ROOT / folder, self.source / folder,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        shutil.copy2(ROOT / 'catalog.json', self.source / 'catalog.json')
        (self.source / 'docs').mkdir()
        shutil.copy2(ROOT / 'docs/project-intelligence.md', self.source / 'docs/project-intelligence.md')

    def setup(self, **kwargs):
        return manager.setup(self.project, source=self.source, **kwargs)

    def test_initial_setup_installs_eight_and_bootstraps(self):
        result = self.setup()
        self.assertEqual(result['revision'], 0)
        self.assertEqual(len(list((self.project / '.agents/skills').iterdir())), 8)
        self.assertTrue((self.project / 'knowledge.owl').exists())
        self.assertTrue((self.project / '.ontolink/context.json').exists())
        self.assertTrue((self.project / '.agents/docs/project-intelligence.md').is_file())
        self.assertFalse(list(self.project.glob('*.json')))
        before = (self.project / 'knowledge.owl').read_bytes()
        self.setup()
        self.assertEqual(before, (self.project / 'knowledge.owl').read_bytes())
        self.assertEqual((self.project / 'AGENTS.md').read_text().count('<!-- ontolink:start -->'), 1)

    def test_update_preserves_recorded_knowledge_and_adds_commands(self):
        self.setup()
        core = self.project / '.agents/skills/ontolink-skills'
        record = self.project / '.ontolink/records/existing.json'
        record.write_text(json.dumps({'id': 'existing', 'type': 'Requirement', 'title': 'Keep this knowledge'}))
        manager.run_json(core / 'scripts/mediator.py', 'record', '--state', self.project / 'knowledge.owl',
                         '--input', record, '--expected-revision', 0)
        for relative in ['.ontolink/proofs/old.log', '.ontolink/artifacts/old.txt', 'app.py']:
            (self.project / relative).write_text('Existing project bytes: ' + relative)
        artifact = self.project / '.ontolink/artifacts/old.txt'
        proof = self.project / '.ontolink/proofs/old.log'
        content_hash = hashlib.sha256(artifact.read_bytes()).hexdigest()
        records = [
            {'id': 'old-artifact', 'type': 'Artifact', 'kind': 'requirements',
             'path': '.ontolink/artifacts/old.txt', 'contentHash': content_hash, 'status': 'CURRENT'},
            {'id': 'old-proof', 'type': 'Evidence', 'supports': 'old-artifact', 'outcome': 'PASS',
             'proofPath': '.ontolink/proofs/old.log', 'proofHash': hashlib.sha256(proof.read_bytes()).hexdigest(),
             'targetHash': content_hash},
        ]
        for revision, payload in enumerate(records, start=1):
            path = self.project / f'.ontolink/records/fixture-{revision}.json'
            path.write_text(json.dumps(payload))
            manager.run_json(core / 'scripts/mediator.py', 'record', '--state', self.project / 'knowledge.owl',
                             '--input', path, '--expected-revision', revision)
        preserved = {path: path.read_bytes() for path in [self.project / 'knowledge.owl', record,
                    self.project / '.ontolink/proofs/old.log', self.project / '.ontolink/artifacts/old.txt',
                    self.project / 'app.py']}
        command = self.source / 'skills/ontolink-skills/scripts/new_command.py'
        command.write_text('print("New command")\n')
        (self.source / '.rule/new-command.md').write_text('New external command instructions\n')
        result = self.setup()
        self.assertEqual(result['revision'], 3)
        self.assertTrue((core / 'scripts/new_command.py').exists())
        self.assertTrue((self.project / '.rule/new-command.md').exists())
        for path, original in preserved.items():
            self.assertEqual(path.read_bytes(), original)
        self.assertTrue((self.project / result['backup'] / 'knowledge.owl').is_file())

    def test_preserves_unrelated_instructions_skills_and_rule_files(self):
        (self.project / 'AGENTS.md').write_text('# Team rules\nPreserve the approved stack.\n')
        unrelated = self.project / '.agents/skills/unrelated'
        unrelated.mkdir(parents=True)
        (unrelated / 'keep.txt').write_text('Keep unrelated skill')
        (self.project / '.rule').mkdir()
        (self.project / '.rule/company.md').write_text('Company policy')
        self.setup()
        self.assertIn('Preserve the approved stack.', (self.project / 'AGENTS.md').read_text())
        self.assertEqual((unrelated / 'keep.txt').read_text(), 'Keep unrelated skill')
        self.assertEqual((self.project / '.rule/company.md').read_text(), 'Company policy')

    def test_invalid_state_stops_before_replacement(self):
        self.setup()
        installed = self.project / '.agents/skills/ontolink-skills/SKILL.md'
        before = installed.read_bytes()
        (self.project / 'knowledge.owl').write_text('Invalid existing data')
        with self.assertRaises(ValueError):
            self.setup()
        self.assertEqual(installed.read_bytes(), before)
        self.assertEqual((self.project / 'knowledge.owl').read_text(), 'Invalid existing data')

    def test_copy_failure_restores_previous_installation(self):
        self.setup()
        installed = self.project / '.agents/skills/ontolink-skills/SKILL.md'
        before = installed.read_bytes()
        (self.source / 'skills/ontolink-skills/SKILL.md').write_text('Incoming changed instructions')
        original_copy = manager.copy
        copies = 0
        def fail_once(source, target):
            nonlocal copies
            copies += 1
            if copies == 4:
                raise OSError('Synthetic copy failure')
            return original_copy(source, target)
        with patch.object(manager, 'copy', side_effect=fail_once):
            with self.assertRaisesRegex(OSError, 'Synthetic copy failure'):
                self.setup()
        self.assertEqual(installed.read_bytes(), before)
        self.assertFalse((self.project / '.ontolink/context.json').exists())

    def test_custom_state_is_reused_without_second_graph(self):
        self.setup()
        (self.project / 'state').mkdir()
        (self.project / 'knowledge.owl').rename(self.project / 'state/custom.owl')
        before = (self.project / 'state/custom.owl').read_bytes()
        result = self.setup(state_path='state/custom.owl')
        self.assertEqual(result['revision'], 0)
        self.assertEqual((self.project / 'state/custom.owl').read_bytes(), before)
        self.assertFalse((self.project / 'knowledge.owl').exists())
        self.assertTrue((self.project / 'state/.ontolink/context.json').exists())

    def test_symlink_storage_is_rejected(self):
        elsewhere = self.base / 'elsewhere'
        elsewhere.mkdir()
        (self.project / '.ontolink').symlink_to(elsewhere, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.setup()
        self.assertEqual(list(elsewhere.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
