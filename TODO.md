# TODO

Items are grouped by the condition that opens them.

## Needs of the project repositories

- [x] **Read the settings from `config/tools/`.** The [rule on project repositories](https://github.com/esther-poniatowski/geonexus/blob/main/docs/rules/project-repositories.md) places the settings of tools in `config/tools/`, so that tool files do not crowd the root of a project. Eikon searches `eikon.yaml` upward from the root of the project, and offers no option for its path. It must also find `config/tools/eikon.yaml`, or take the path of its file as an option. Done on 2026-11-10: `locate_config` finds the file in `config/tools/` or at a root, and the file in `config/tools/` takes precedence, as the [command-line conventions](https://github.com/esther-poniatowski/keystone/blob/main/docs/internals/cli-conventions.md) require.

## Defects

- [ ] **Repair the circular import of the command line.** `import eikon.cli` fails: `eikon.cli.commands` imports `get_project_root` from itself while it initializes, so `tests/test_eikon/test_cli.py` fails at collection and `python -m eikon --help` fails (`test_main.py::TestMainEntry::test_module_invocation_help`).
- [ ] **Repair `test_merge_layout`.** `tests/test_eikon/test_spec/test_override.py::TestMergeSpecOverride::test_merge_layout` fails on the code of 2026-11-10, before and after the search in `config/tools/`.
