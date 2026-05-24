<a id="registry"></a>

# Registry

Figure registry storage, queries, and locking.

<a id="module-eikon.registry._registry"></a>

<a id="registry-class"></a>

## Registry Class

Registry class — CRUD operations on the figure registry.

The [`Registry`](#eikon.registry._registry.Registry) provides a high-level API for managing figure
entries: registering, querying, removing, and persisting to YAML.

<a id="eikon.registry._registry.Registry"></a>

### *class* eikon.registry._registry.Registry(path)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

In-memory figure registry backed by a YAML manifest.

* **Parameters:**
  **path** (*Path*) – Path to the YAML manifest file.

<a id="eikon.registry._registry.Registry.load"></a>

#### load()

Load entries from the manifest file.

If the file does not exist, the registry starts empty.

<a id="eikon.registry._registry.Registry.save"></a>

#### save()

Persist current entries to the manifest file.

<a id="eikon.registry._registry.Registry.register"></a>

#### register(name, \*, tags=(), group='', metadata=None, on_conflict='update', spec_path=None)

Register a figure in the registry.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name (unique identifier).
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Organizational tags.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Grouping key (e.g. `"manuscript-1"`).
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]* *,* *optional*) – Arbitrary metadata fields.
  * **on_conflict** ( *{"update"* *,*  *"fail"* *,*  *"skip"}*) – How to handle duplicate names. `"update"` replaces the existing
    entry, `"fail"` raises `RegistryError`, and `"skip"` keeps
    the existing entry.
  * **spec_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *optional*) – Path to the figure specification YAML file.
* **Raises:**
  [**RegistryError**](types.md#eikon.exceptions.RegistryError) – If `on_conflict="fail"` and the name already exists.

<a id="eikon.registry._registry.Registry.get"></a>

#### get(name)

Get a registry entry by name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name.
* **Returns:**
  The entry data.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]
* **Raises:**
  [**RegistryError**](types.md#eikon.exceptions.RegistryError) – If the name is not registered.

<a id="eikon.registry._registry.Registry.remove"></a>

#### remove(name)

Remove a figure from the registry.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name.
* **Raises:**
  [**RegistryError**](types.md#eikon.exceptions.RegistryError) – If the name is not registered.

<a id="eikon.registry._registry.Registry.list_all"></a>

#### list_all()

Return a sorted list of all registered figure names.

<a id="eikon.registry._registry.Registry.query"></a>

#### query(\*, tags=(), group='', match_all_tags=False)

Query the registry with optional tag and group filters.

* **Parameters:**
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Tags to match.  Empty = no tag filter.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Group to match.  Empty = no group filter.
  * **match_all_tags** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True`, entries must have **all** tags.
* **Returns:**
  Matching entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="module-eikon.registry._index"></a>

<a id="registry-index"></a>

## Registry Index

YAML manifest I/O for the figure registry.

The manifest is a YAML file (default `eikon-registry.yaml`) that
persists registry entries across sessions.  Each entry stores the
figure name, tags, group, and the timestamp of last registration.

<a id="eikon.registry._index.load_manifest"></a>

### eikon.registry._index.load_manifest(path)

Load the registry manifest from a YAML file.

* **Parameters:**
  **path** (*Path*) – Path to the manifest file.
* **Returns:**
  Mapping of figure names to their registry entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]
* **Raises:**
  [**RegistryError**](types.md#eikon.exceptions.RegistryError) – If the file exists but is not a valid YAML mapping.

<a id="eikon.registry._index.save_manifest"></a>

### eikon.registry._index.save_manifest(path, entries)

Save the registry manifest to a YAML file.

* **Parameters:**
  * **path** (*Path*) – Path to the manifest file.
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Mapping of figure names to their registry entries.

<a id="module-eikon.registry._query"></a>

<a id="registry-queries"></a>

## Registry Queries

Query and filter logic for registry entries.

Provides functions to filter registry entries by tags, group,
or arbitrary predicates.

<a id="eikon.registry._query.filter_by_tags"></a>

### eikon.registry._query.filter_by_tags(entries, tags, \*, match_all=False)

Filter entries that have any (or all) of the given tags.

* **Parameters:**
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Registry entries to filter.
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Tags to match against.
  * **match_all** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True`, an entry must have **all** tags.
    If `False` (default), an entry must have **any** tag.
* **Returns:**
  Filtered entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="eikon.registry._query.filter_by_group"></a>

### eikon.registry._query.filter_by_group(entries, group)

Filter entries belonging to a specific group.

* **Parameters:**
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Registry entries to filter.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Group name to match.
* **Returns:**
  Filtered entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="eikon.registry._query.filter_entries"></a>

### eikon.registry._query.filter_entries(entries, \*, tags=(), group='', match_all_tags=False)

Apply tag and group filters in sequence.

* **Parameters:**
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Registry entries to filter.
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Tags to match.  Empty = no tag filter.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Group name.  Empty = no group filter.
  * **match_all_tags** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether tag matching requires all tags.
* **Returns:**
  Filtered entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="module-eikon.registry._locking"></a>

<a id="registry-locking"></a>

## Registry Locking

Advisory file locking for concurrent registry access.

Provides a context manager that acquires an exclusive lock on the
registry manifest file, preventing partial reads or lost writes when
multiple processes access the same manifest concurrently.

Uses `fcntl.flock` (Unix/macOS) when available, with a no-op
fallback on platforms that lack `fcntl` (e.g. Windows).

<a id="eikon.registry._locking.registry_lock"></a>

### eikon.registry._locking.registry_lock(path, \*, timeout=5.0)

Acquire an exclusive advisory lock on a file.

* **Parameters:**
  * **path** (*Path*) – Path to the file to lock.  A `.lock` sibling file is used.
  * **timeout** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Maximum seconds to wait for the lock.  Defaults to 5.
* **Yields:**
  *None* – Control while the lock is held.
* **Raises:**
  [**RegistryError**](types.md#eikon.exceptions.RegistryError) – If the lock cannot be acquired within *timeout*.
