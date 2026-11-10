# TODO

Items are grouped by the condition that opens them.

## Needs of the project repositories

- [ ] **Read the settings from `config/tools/`.** The [rule on project repositories](https://github.com/esther-poniatowski/geonexus/blob/main/docs/rules/project-repositories.md) places the settings of tools in `config/tools/`, so that tool files do not crowd the root of a project. Eikon searches `eikon.yaml` upward from the root of the project, and offers no option for its path. It must also find `config/tools/eikon.yaml`, or take the path of its file as an option.
