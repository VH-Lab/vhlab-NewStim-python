"""Tests for the MATLAB -> Python bridge contract files.

Each ``vhlab_newstim`` package carries a ``vhlab_newstim_matlab_python_bridge.yaml``
recording where every module came from in vhlab-NewStim-matlab, and what was
decided about the parts that will never be ported. These tests keep the files
and the code in step: a new module without a bridge entry, a bridge entry
pointing at a file that no longer exists, or a status outside the vocabulary
fails here.

What these tests cannot check is that every MATLAB file still has an entry --
vhlab-NewStim-matlab is not checked out in CI. That half is manual, and is done
when ``matlab_last_sync_hash`` is bumped. See PORTING_INSTRUCTIONS.
"""

import os

import pytest
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRIDGE_NAME = 'vhlab_newstim_matlab_python_bridge.yaml'
PACKAGE_ROOT = os.path.join('src', 'vhlab_newstim')
ROOT_BRIDGE = os.path.join(REPO_ROOT, PACKAGE_ROOT, BRIDGE_NAME)

# Packages that carry a function-level bridge file. Add a package here in the
# same commit that gives it one; test_root_bridge_lists_every_package checks
# this list against the top-level file's `subpackages`.
FUNCTION_PACKAGES = (
    'src/vhlab_newstim/display',
    'src/vhlab_newstim/scripts',
    'src/vhlab_newstim/stimuli',
)

VALID_TYPES = ('function', 'class', 'method')

# A status that names a Python implementation must have one; every other status
# must not, or "not ported" and "ported" become indistinguishable.
STATUSES_WITH_PYTHON = ('ported', 'does_not_exist')


def load(path):
    with open(path, 'r') as handle:
        return yaml.safe_load(handle)


def bridge_files():
    """Every bridge file in the repository, as absolute paths."""
    found = []
    for dirpath, _dirnames, filenames in os.walk(os.path.join(REPO_ROOT, PACKAGE_ROOT)):
        if BRIDGE_NAME in filenames:
            found.append(os.path.join(dirpath, BRIDGE_NAME))
    return sorted(found)


def python_modules(package_path):
    """Every non-__init__ module in a package, repo-relative, recursively."""
    modules = []
    for dirpath, _dirnames, filenames in os.walk(os.path.join(REPO_ROOT, package_path)):
        for name in sorted(filenames):
            if name.endswith('.py') and name != '__init__.py':
                full = os.path.join(dirpath, name)
                modules.append(os.path.relpath(full, REPO_ROOT))
    return sorted(modules)


def function_entries(path):
    """(entry, label) for every function entry in one bridge file."""
    for entry in load(path).get('functions', []):
        yield entry, '%s: %s' % (os.path.relpath(path, REPO_ROOT),
                                 entry.get('matlab_path') or entry.get('name'))


@pytest.fixture(scope='module')
def vocabulary():
    return set(load(ROOT_BRIDGE)['status_vocabulary'].keys())


def test_every_package_has_a_bridge_file():
    for package in FUNCTION_PACKAGES:
        path = os.path.join(REPO_ROOT, package, BRIDGE_NAME)
        assert os.path.isfile(path), 'missing bridge file for package ' + package
    assert os.path.isfile(ROOT_BRIDGE), 'missing top-level bridge file ' + ROOT_BRIDGE


def test_bridge_files_parse():
    paths = bridge_files()
    assert paths, 'no bridge files found under ' + PACKAGE_ROOT
    for path in paths:
        data = load(path)
        assert isinstance(data, dict), path + ' is not a mapping'
        assert 'project_metadata' in data, path
        metadata = data['project_metadata']
        for key in ('bridge_version', 'matlab_repository', 'matlab_last_sync_hash',
                    'python_package', 'naming_policy', 'indexing_policy'):
            assert key in metadata, '%s: project_metadata.%s' % (path, key)


def test_status_values_are_from_the_vocabulary(vocabulary):
    for path in bridge_files():
        data = load(path)
        entries = (list(data.get('functions', []))
                   + list(data.get('coverage_areas', []))
                   + list(data.get('downstream_requirements', [])))
        for entry in entries:
            label = entry.get('name') or entry.get('matlab_path')
            assert 'status' in entry, '%s: %s has no status' % (path, label)
            assert entry['status'] in vocabulary, (
                '%s: %s has unknown status %r' % (path, label, entry['status']))


def test_function_entries_are_well_formed():
    for path in bridge_files():
        for entry, label in function_entries(path):
            assert entry.get('name'), path + ': entry with no name'
            assert entry.get('type') in VALID_TYPES, (
                '%s has bad type %r' % (label, entry.get('type')))
            assert entry.get('decision_log'), '%s has no decision_log' % label
            if entry['status'] in STATUSES_WITH_PYTHON:
                assert entry.get('python_path'), (
                    '%s is %s but has no python_path' % (label, entry['status']))
            else:
                assert entry.get('python_path') is None, (
                    '%s is %s but names a python_path' % (label, entry['status']))
            if entry['status'] != 'does_not_exist':
                assert entry.get('matlab_path'), '%s has no matlab_path' % label
                assert entry.get('matlab_last_sync_hash'), (
                    '%s has no matlab_last_sync_hash' % label)


def test_ported_entries_type_both_sides():
    """A ported entry is the contract; both sides of every argument are typed."""
    for path in bridge_files():
        for entry, label in function_entries(path):
            if entry['status'] != 'ported':
                continue
            for key in ('input_arguments', 'output_arguments'):
                assert key in entry, '%s is ported but has no %s' % (label, key)
                for argument in entry[key] or []:
                    assert argument.get('name'), '%s: %s entry with no name' % (label, key)
                    for side in ('type_matlab', 'type_python'):
                        assert argument.get(side), (
                            '%s: %s %s has no %s'
                            % (label, key, argument.get('name'), side))


def test_matlab_paths_are_unique_and_in_the_right_folder():
    """matlab_path is the key; the same method name recurs across many classes."""
    for path in bridge_files():
        folder = load(path)['project_metadata'].get('matlab_package_path')
        seen = set()
        for entry, label in function_entries(path):
            matlab_path = entry.get('matlab_path')
            if matlab_path is None:
                continue
            assert matlab_path not in seen, '%s is listed twice' % label
            seen.add(matlab_path)
            if folder:
                assert matlab_path.startswith(folder + '/'), (
                    '%s is not under %s' % (label, folder))


def test_python_paths_exist():
    for path in bridge_files():
        data = load(path)
        entries = data.get('functions', []) + data.get('subpackages', [])
        for entry in entries:
            label = entry.get('name') or entry.get('python_package')
            for key in ('python_path', 'bridge_file'):
                value = entry.get(key)
                if not value:
                    continue
                assert os.path.exists(os.path.join(REPO_ROOT, value)), (
                    '%s: %s -> %s does not exist' % (path, label, value))


def test_every_module_is_covered_by_a_bridge_entry():
    for package in FUNCTION_PACKAGES:
        data = load(os.path.join(REPO_ROOT, package, BRIDGE_NAME))
        covered = {entry['python_path'] for entry in data.get('functions', [])
                   if entry.get('python_path')}
        for module in python_modules(package):
            assert module in covered, (
                '%s has no entry in %s/%s' % (module, package, BRIDGE_NAME))


def test_root_bridge_lists_every_package():
    data = load(ROOT_BRIDGE)
    listed = {entry['python_path'] for entry in data['subpackages']}
    assert listed == set(FUNCTION_PACKAGES)
    for entry in data['subpackages']:
        assert entry.get('matlab_path'), entry['python_package'] + ' has no matlab_path'


def test_coverage_areas_account_for_every_matlab_file():
    """Every .m file in vhlab-NewStim-matlab is accounted for by exactly one area."""
    data = load(ROOT_BRIDGE)
    areas = data['coverage_areas']
    for area in areas:
        assert isinstance(area.get('matlab_file_count'), int), (
            '%s has no integer matlab_file_count' % area.get('matlab_path'))
        assert area.get('decision_log'), (
            '%s has no decision_log' % area.get('matlab_path'))
    total = sum(area['matlab_file_count'] for area in areas)
    assert total == data['project_metadata']['matlab_file_count'], (
        'coverage_areas sum to %d but matlab_file_count is %d'
        % (total, data['project_metadata']['matlab_file_count']))


def test_downstream_requirements_are_well_formed():
    for entry in load(ROOT_BRIDGE).get('downstream_requirements', []):
        assert entry.get('requested_by'), 'downstream requirement with no requested_by'
        assert entry.get('matlab_function'), (
            '%s names no matlab_function' % entry['requested_by'])
        assert entry.get('decision_log'), (
            '%s has no decision_log' % entry['requested_by'])
