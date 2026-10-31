"""Instruction-contract regressions, not model behavior or photographic quality tests."""
import tempfile
from pathlib import Path
import unittest

from facade_plugin import asset_root, generate_plugins


class VisualAcceptanceTests(unittest.TestCase):
    def test_checkpoint_reaches_every_host_with_bounded_transitions(self):
        root = asset_root()
        relative = Path('skills/facade-photo-editor/references/visual-acceptance.md')
        canonical = (root / relative).read_text()
        rows = [line.split('|')[1:-1] for line in canonical.splitlines()
                if line.startswith('| 1 |') or line.startswith('| 2 |')]
        transitions = {(r[0].strip(), r[1].strip()): r[2].strip() for r in rows}
        self.assertEqual(len(transitions), 6)
        self.assertIn('ONE targeted correction', transitions['1', 'revise'])
        self.assertIn('no acceptance', transitions['2', 'revise'])
        for count in ('1', '2'):
            self.assertIn('finish', transitions[count, 'accept'])
            self.assertIn('no acceptance', transitions[count, 'uncertain/error/missing images'])
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            executable = directory / 'runtime'
            executable.write_text('#!/bin/sh\nexit 0\n')
            executable.chmod(0o755)
            generate_plugins(executable, directory / 'packages', version='test')
            for host in ('codex', 'cursor', 'claude'):
                package = directory / 'packages' / host
                self.assertEqual((package / relative).read_text(), canonical)
                skill = (package / 'skills/facade-photo-editor/SKILL.md').read_text()
                self.assertIn('Only after an accept verdict', skill)
                self.assertIn('(references/visual-acceptance.md)', skill)
                self.assertNotIn('After two unhelpful revisions', skill)

    def test_fixed_baseline_preservation_and_fail_closed_instructions(self):
        text = (asset_root() / 'skills/facade-photo-editor/references/visual-acceptance.md').read_text()
        for rule in ('Keep before fixed through both reviews',
                     'never overwrite, reject or delete it',
                     'also show the saved first_candidate',
                     'newer is not automatically better',
                     'missing images or reviewer errors mean uncertain',
                     'at most TWO substantial issues',
                     'At most ONE corrective',
                     'An accept with unresolved issues or an invalid/missing verdict is uncertain'):
            self.assertIn(rule, text)
