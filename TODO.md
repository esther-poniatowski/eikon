# TODO

Items are grouped by the condition that opens them.

## Needs of the project repositories

- [x] **Read the configuration file from `config/tools/`.** The [rule on project repositories](https://github.com/esther-poniatowski/geonexus/blob/main/docs/rules/project-repositories.md) places the configuration files of tools in `config/tools/`, so that tool files do not crowd the root of a project. Done on 2026-11-10: `locate_config` finds `eikon.yml` in `config/tools/` or at a root, both files being an error, and `--config` names another file, as the [command-line conventions](https://github.com/esther-poniatowski/keystone/blob/main/docs/internals/cli-conventions.md) require.

- [ ] **Rename the option of the export formats.** The [command-line conventions](https://github.com/esther-poniatowski/keystone/blob/main/docs/internals/cli-conventions.md) reserve `--format` for the format of a report, whereas `render`, `batch` and `render-registry` use `--format`, `-f` for the formats of the exported figure. A domain name such as `--export-format` must replace it, together with every consumer that calls it.
- [ ] **Review the remaining exit statuses.** The conventions reserve status 2 for a usage or configuration error. `registry show` and `registry remove` on an unknown name, and `batch` on an absent specs folder, still exit with status 1.

## Defects

- [ ] **Repair `test_merge_layout`.** `tests/test_eikon/test_spec/test_override.py::TestMergeSpecOverride::test_merge_layout` fails on the code of 2026-11-10, before and after the search in `config/tools/`.
