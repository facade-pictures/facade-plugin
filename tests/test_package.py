import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from facade_plugin import asset_root, generate_plugins


class PackageTests(unittest.TestCase):
    def test_self_contained_assets_without_checkout_or_backend_imports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            module = root / 'facade_plugin'
            module.mkdir()
            shutil.copy2(asset_root() / 'LICENSE', module / 'LICENSE')
            shutil.copy2(asset_root() / 'facade_plugin/__init__.py', module / '__init__.py')
            for name in ('skills', 'hosts', 'docs'):
                shutil.copytree(asset_root() / name, module / name)
            executable = root / "runtime with ' quote/facade-editor"
            executable.parent.mkdir()
            executable.write_text('#!/bin/sh\nprintf \'%s\\n\' "$@"\n')
            executable.chmod(0o755)
            code = '''import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from facade_plugin import asset_root, generate_plugins
assert asset_root() == Path(sys.argv[1]) / 'facade_plugin'
generate_plugins(Path(sys.argv[2]), Path(sys.argv[3]), version='9.8.7')
assert not any(name.startswith('facade_processing') for name in sys.modules)
'''
            subprocess.run([sys.executable, '-I', '-c', code, str(root), str(executable), str(root / 'packages')],
                           check=True, capture_output=True, text=True)
            for host in ('codex', 'cursor', 'claude'):
                package = root / 'packages' / host
                self.assertEqual((package / 'LICENSE').read_bytes(), (asset_root() / 'LICENSE').read_bytes())
                manifest = json.loads((package / f'.{host}-plugin/plugin.json').read_text())
                self.assertEqual(manifest['license'], 'MIT')
                self.assertTrue((package / 'skills/facade-setup/SKILL.md').is_file())
                self.assertTrue((package / 'docs/installation.md').is_file())
                self.assertEqual((package / 'skills/facade-photo-editor/host.md').read_bytes(),
                                 (asset_root() / 'hosts' / f'{host}.md').read_bytes())
                config = json.loads((package / '.mcp.json').read_text())
                self.assertEqual(config['mcpServers']['facade']['command'], str(executable))
            launcher = root / 'packages/codex/bin/facade-editor'
            response = subprocess.run([str(launcher), 'mcp'], cwd=root, capture_output=True, text=True, check=True)
            self.assertEqual(response.stdout, 'mcp\n')

    def test_does_not_overwrite_existing_package_directory(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            executable = root / 'runtime'
            executable.write_text('#!/bin/sh\nexit 0\n')
            executable.chmod(0o755)
            output = root / 'packages'
            generate_plugins(executable, output, version='9.8.7')
            with self.assertRaises(FileExistsError):
                generate_plugins(executable, output, version='9.8.7')


if __name__ == '__main__':
    unittest.main()
