"""Setup-layer tests; they never access GitHub or modify deposited science."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from configure_github import apply_configuration, validate_repository, validate_tag
from apply_github_settings import settings_command
from check_release_assets import check_assets
from check_github_setup import check


class SetupTests(unittest.TestCase):
    def make_fixture(self, folder):
        root = Path(folder)
        for name in ['repository_metadata.json', 'CITATION.cff', 'README.md', '.github/repository-settings.json']:
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        # A unit-test fixture must not inherit the live package's publication state.
        metadata = json.loads((root / 'repository_metadata.json').read_text())
        metadata.update(repository_url=None, public_version=None, publication_status='not_deposited')
        (root / 'repository_metadata.json').write_text(json.dumps(metadata) + '\n')
        (root / 'manuscript').mkdir()
        (root / 'manuscript/main.tex').write_bytes(b'SCIENCE MUST NOT CHANGE\n')
        return root

    def test_actual_setup_structure(self):
        self.assertTrue(check(ROOT)['passed'])

    def test_valid_repository(self):
        self.assertEqual(validate_repository('research-lab/stable-score-mh'), 'research-lab/stable-score-mh')

    def test_rejects_url_instead_of_slug(self):
        with self.assertRaises(ValueError): validate_repository('https://github.com/research-lab/project')

    def test_rejects_owner_placeholder(self):
        with self.assertRaises(ValueError): validate_repository('YOUR-USERNAME/stable-score-mh')

    def test_rejects_shell_characters(self):
        with self.assertRaises(ValueError): validate_repository('person/repo;echo')

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError): validate_repository('../repo')

    def test_tag_accepts_normal_version(self):
        self.assertEqual(validate_tag('v1.0.0'), 'v1.0.0')

    def test_tag_rejects_option(self):
        with self.assertRaises(ValueError): validate_tag('--delete')

    def test_tag_rejects_shell(self):
        with self.assertRaises(ValueError): validate_tag('v1;echo x')

    def test_tag_rejects_relative_path(self):
        with self.assertRaises(ValueError): validate_tag('../v1')

    def test_configuration_no_science_or_authorship_change(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            before = (r / 'manuscript/main.tex').read_bytes()
            authors = json.loads((r / 'repository_metadata.json').read_text())['manuscript_authors']
            apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0')
            meta = json.loads((r / 'repository_metadata.json').read_text())
            self.assertEqual(meta['manuscript_authors'], authors)
            self.assertEqual(meta['publication_status'], 'not_deposited')
            self.assertEqual((r / 'manuscript/main.tex').read_bytes(), before)
            self.assertFalse((r / '.github/CODEOWNERS').exists())

    def test_unverified_status_is_not_promoted_to_public(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            p = r / 'repository_metadata.json'
            metadata = json.loads(p.read_text())
            metadata['publication_status'] = 'unverified'
            p.write_text(json.dumps(metadata))
            apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0')
            self.assertEqual(json.loads(p.read_text())['publication_status'], 'unverified')

    def test_configuration_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0')
            before = {p.relative_to(r): p.read_bytes() for p in r.rglob('*') if p.is_file()}
            apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0')
            self.assertEqual(before, {p.relative_to(r): p.read_bytes() for p in r.rglob('*') if p.is_file()})

    def test_explicit_maintainer_only(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0', 'confirmed-user')
            self.assertIn('* @confirmed-user', (r / '.github/CODEOWNERS').read_text())

    def test_invalid_maintainer_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            before = (r / 'repository_metadata.json').read_bytes()
            with self.assertRaises(ValueError):
                apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0', '@not-valid')
            self.assertEqual((r / 'repository_metadata.json').read_bytes(), before)

    def test_no_repoint_of_public_repository(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            p = r / 'repository_metadata.json'
            m = json.loads(p.read_text()); m.update(publication_status='public', repository_url='https://github.com/old-owner/old-repo')
            p.write_text(json.dumps(m))
            with self.assertRaises(ValueError): apply_configuration(r, 'research-lab/stable-score-mh', 'v1.0.0')

    def test_no_unverified_public_tag_change(self):
        with tempfile.TemporaryDirectory() as td:
            r = self.make_fixture(td)
            p = r / 'repository_metadata.json'
            m = json.loads(p.read_text())
            m.update(publication_status='public', repository_url='https://github.com/research-lab/stable-score-mh', public_version='v1.0.0')
            p.write_text(json.dumps(m))
            with self.assertRaises(ValueError):
                apply_configuration(r, 'research-lab/stable-score-mh', 'v2.0.0')

    def test_settings_plan_never_changes_visibility(self):
        s = json.loads((ROOT / '.github/repository-settings.json').read_text())
        s['repository'] = 'research-lab/stable-score-mh'
        cmd = settings_command(s)
        self.assertNotIn('--visibility', cmd)
        self.assertNotIn('--enable-advanced-security', cmd)
        self.assertIn('--enable-wiki=false', cmd)

    def test_unconfigured_settings_fail(self):
        s = json.loads((ROOT / '.github/repository-settings.json').read_text()); s['repository'] = None
        with self.assertRaises(ValueError): settings_command(s)

    def test_settings_rejects_nonboolean(self):
        s = json.loads((ROOT / '.github/repository-settings.json').read_text())
        s.update(repository='research-lab/stable-score-mh', enable_wiki='false')
        with self.assertRaises(ValueError): settings_command(s)

    def test_asset_checker_accepts_exact_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td); a = r / 'a.zip'; a.write_bytes(b'exact bytes')
            (r / 'RELEASE_ASSETS.json').write_text(json.dumps({'assets': [{'filename': 'a.zip', 'bytes': a.stat().st_size, 'sha256': hashlib.sha256(a.read_bytes()).hexdigest()}]}))
            self.assertEqual(check_assets(r, r, True)['matched'], ['a.zip'])

    def test_asset_checker_rejects_corruption(self):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td); (r / 'a.zip').write_bytes(b'wrong')
            (r / 'RELEASE_ASSETS.json').write_text(json.dumps({'assets': [{'filename': 'a.zip', 'bytes': 5, 'sha256': '0' * 64}]}))
            with self.assertRaises(ValueError): check_assets(r, r, True)

    def test_missing_assets_are_not_claimed_available(self):
        with tempfile.TemporaryDirectory() as td:
            r = Path(td)
            (r / 'RELEASE_ASSETS.json').write_text(json.dumps({'assets': [{'filename': 'absent.zip', 'bytes': 5, 'sha256': '0' * 64}]}))
            with self.assertRaises(ValueError): check_assets(r, r, True)


if __name__ == '__main__':
    unittest.main()
