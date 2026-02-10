# Figure Registry

The figure registry tracks and organizes figures across a project. Entries are persisted in a YAML manifest file (`eikon-registry.yaml` by default), making the registry version-controllable and human-readable.

## Registering figures

### From the CLI

```bash
eikon registry add fig1 --tag neural --tag overview --group manuscript-1
eikon registry add fig2 --tag behavioral --group manuscript-1 --spec-path specs/fig2.yaml
```

### From Python

```python
import eikon

reg = eikon.load_registry()
reg.register(
    "fig1",
    tags=("neural", "overview"),
    group="manuscript-1",
    spec_path="specs/fig1.yaml",
)
reg.save()  # Persist to disk
```

## Querying the registry

### List all figures

```bash
eikon registry list
```

```python
reg = eikon.load_registry()
print(reg.list_all())  # ["fig1", "fig2", ...]
```

### Filter by tags

```bash
# Figures with ANY of these tags
eikon registry list --tag neural --tag behavioral

# Figures with ALL of these tags (CLI batch command)
eikon batch --tag neural --tag overview --match-all
```

```python
results = reg.query(tags=("neural",))
# {"fig1": {"tags": ["neural", "overview"], ...}}

# Require all tags
results = reg.query(tags=("neural", "overview"), match_all_tags=True)
```

### Filter by group

```bash
eikon registry list --group manuscript-1
```

```python
results = reg.query(group="manuscript-1")
```

## Viewing and removing entries

```bash
# Show details for a figure
eikon registry show fig1

# Remove a figure
eikon registry remove fig1
```

```python
entry = reg.get("fig1")
# {"tags": ["neural"], "group": "manuscript-1", "spec_path": "...", ...}

reg.remove("fig1")
reg.save()
```

## Conflict handling

When registering a figure whose name already exists:

```python
reg.register("fig1", on_conflict="update")   # Default: replace entry
reg.register("fig1", on_conflict="skip")     # Keep existing entry
reg.register("fig1", on_conflict="fail")     # Raise RegistryError
```

## Registry manifest format

The manifest file is a YAML file managed by eikon:

```yaml
fig1:
  tags: [neural, overview]
  group: manuscript-1
  metadata: {}
  spec_path: specs/fig1.yaml
  registered_at: "2026-02-10T14:30:00+00:00"
fig2:
  tags: [behavioral]
  group: manuscript-1
  metadata: {}
  spec_path: ""
  registered_at: "2026-02-10T14:31:00+00:00"
```

## Rendering from the registry

The `render()` function can resolve figures by registry name:

```python
handle = eikon.render("fig1", formats=("pdf",))
```

This looks up the registry entry, finds the associated `spec_path`, and renders the figure. If no registry entry is found, it falls back to looking for `specs/fig1.yaml`.

From the CLI:

```bash
eikon render-registry fig1 --format pdf
```

See the {doc}`/api/registry` for the complete API reference.
