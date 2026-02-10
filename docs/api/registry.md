# eikon.registry

Figure registry: CRUD operations, YAML persistence, and query filtering.

For usage examples, see the {doc}`Registry guide </guide/registry>`.

## Classes

### Registry

```
eikon.registry.Registry(path: Path)
```

In-memory figure registry backed by a YAML manifest file.

| Attribute | Type | Description |
|-----------|------|-------------|
| `path` | `Path` | Path to the YAML manifest file |

**Methods:**

#### load

```
Registry.load() -> None
```

Load entries from the manifest file. If the file does not exist, the registry starts empty.

#### save

```
Registry.save() -> None
```

Persist current entries to the manifest file.

#### register

```
Registry.register(name: str, *, tags=(), group="", metadata=None,
                  on_conflict="update", spec_path=None) -> None
```

Register a figure in the registry.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | *(required)* | Figure name (unique identifier) |
| `tags` | `tuple[str, ...]` | `()` | Organizational tags |
| `group` | `str` | `""` | Grouping key |
| `metadata` | `dict[str, str] \| None` | `None` | Arbitrary metadata |
| `on_conflict` | `"update" \| "fail" \| "skip"` | `"update"` | Duplicate handling |
| `spec_path` | `str \| None` | `None` | Path to spec YAML file |

**Raises:** `RegistryError` if `on_conflict="fail"` and name exists.

#### get

```
Registry.get(name: str) -> dict[str, Any]
```

Get a registry entry by name.

**Raises:** `RegistryError` if the name is not registered.

#### remove

```
Registry.remove(name: str) -> None
```

Remove a figure from the registry.

**Raises:** `RegistryError` if the name is not registered.

#### list_all

```
Registry.list_all() -> list[str]
```

Return a sorted list of all registered figure names.

#### query

```
Registry.query(*, tags=(), group="", match_all_tags=False) -> dict[str, dict[str, Any]]
```

Query the registry with optional tag and group filters.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tags` | `tuple[str, ...]` | `()` | Tags to match (empty = no filter) |
| `group` | `str` | `""` | Group to match (empty = no filter) |
| `match_all_tags` | `bool` | `False` | Require all tags to match |

#### Special methods

```
len(registry)          # Number of entries
"fig1" in registry     # Membership test
```

## Functions

### filter_by_tags

```
eikon.registry.filter_by_tags(entries: dict[str, dict[str, Any]],
                              tags: tuple[str, ...],
                              *, match_all=False) -> dict[str, dict[str, Any]]
```

Filter registry entries by tags.

---

### filter_by_group

```
eikon.registry.filter_by_group(entries: dict[str, dict[str, Any]],
                               group: str) -> dict[str, dict[str, Any]]
```

Filter registry entries by group name.

---

### filter_entries

```
eikon.registry.filter_entries(entries: dict[str, dict[str, Any]], *,
                              tags=(), group="",
                              match_all_tags=False) -> dict[str, dict[str, Any]]
```

Combined tag and group filter.
