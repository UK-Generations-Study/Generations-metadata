# Generations Study metadata

Metadata for analysts using data releases from the **Breast Cancer Now Generations Study** (BGS, also known as GS).
It describes the study, the data resources it holds, and the structure of each released table: its variables,
data types and allowed values.

> All tables described here are **pseudonymised releases**. Variables that identify participants are removed
> before release, so they never appear in this metadata.

## The three levels

| Level | Answers | Where | How to read it |
|---|---|---|---|
| **Study-level metadata** | What is the Generations Study? Who runs it, who is in it, how to get access? | [`study-level-metadata/`](study-level-metadata/) | [Study at a glance](study-level-metadata/README.md) |
| **Resource-level metadata** | What data exist (questionnaire rounds, linked data, samples, images…) and how do they relate? | [`ro-crate-metadata.json`](ro-crate-metadata.json), [`resource-level-metadata/`](resource-level-metadata/) | [Resources overview](resource-level-metadata/README.md) |
| **Structural metadata** | What exactly is in each released table: variables, labels, types, codes, missing values, constraints? | [`structural-metadata/`](structural-metadata/) | [Schema Explorer](#viewing-the-schemas-in-schema-explorer) |

## Repository layout

```
Generations-metadata/
│
├── README.md
│   Overview of the repository, the metadata model and how to use it
│
├── LICENSE
│   CC BY 4.0: metadata and documentation
│
├── LICENSE-CODE
│   MIT: scripts in tools/
│
├── CHANGELOG.md
│   Record of changes to the repository
│
├── VERSIONS.json
│   Version of every released table schema (generated automatically)
│
├── ro-crate-metadata.json
│   Resource graph describing how the study's resources link together
│   (initially a placeholder)
│
├── release-notes/
│   One page describing each data release
│
├── study-level-metadata/
│   │
│   ├── README.md
│   │   Human-readable description of the study-level metadata
│   │
│   └── study.json
│       Machine-readable description of the Generations Study as a whole
│
├── resource-level-metadata/
│   │
│   └── README.md
│       Human-readable overview of the resources, their relationships
│       and the terminology used to describe them
│
├── structural-metadata/
│   │
│   ├── README.md
│   │   Explains the structural metadata, schema organisation,
│   │   naming/versioning conventions and how to use the schemas
│   │
│   └── schemas/
│       │   JSON Schemas describing released data tables, including
│       │   variables, data types, constraints and allowed values
│       │
│       ├── questionnaires/
│       │   ├── R0/
│       │   ├── R1/
│       │   ├── R2/
│       │   ├── R3/
│       │   ├── R4/
│       │   └── R5/
│       │
│       ├── derived/
│       ├── administration/
│       ├── linkage/
│       ├── biospecimens/
│       ├── biomarker_assays/
│       ├── pathology/
│       ├── imaging/
│       ├── mammograms/
│       ├── accelerometry/
│       └── genomics/
│
├── guides/
│   Practical guides for analysts using Generations data
│
└── tools/
    Scripts that validate the metadata, generate VERSIONS.json
    and generate human-readable pages
```

Questionnaire rounds are named **R0** (baseline) to **R5** (fifth follow-up). R1 is also known as TwoHalfQ.

## Viewing the schemas in Schema Explorer

[Schema Explorer](https://jeyabbalas.github.io/schema-explorer/) shows each table's variables, descriptions,
data types, valid values and constraints in a browsable, searchable form
(source and documentation: [github.com/jeyabbalas/schema-explorer](https://github.com/jeyabbalas/schema-explorer)).

It runs entirely in your browser and reads schemas **from your own computer only**. It cannot open a GitHub link,
so you first get a local copy, then give it the folder:

1. **Get a local copy of this repository.** Either:
   - click **Code → Download ZIP** at the top of this page and unzip it, or
   - clone it: `git clone <this repository's URL>`.
2. **Open Schema Explorer**: <https://jeyabbalas.github.io/schema-explorer/>.
3. **Load the schemas**: drag the folder `structural-metadata/schemas/` onto the page,
   or use the folder picker. To look at one dataset only, load just that dataset's folder.
   - Always load a **folder**, not single files. Schemas point to shared files (for example missing-value codes in
     `common/defs.json`) by relative path, and those links only resolve when the whole folder is loaded.
4. **Browse**: each source folder (for example `linkage`, `questionnaires`) appears as one card, with each of its
   released tables listed inside by title. A table shows its variables with *Variable*, *Description*,
   *Data type*, *Format*, *Valid values* (codes, plus special codes such as missing values) and *Constraints*.
   The **Metadata** button shows the table's own details (title, version, data version), the search box at the top
   searches across everything loaded, and each card can be exported to Excel.

Notes:
- Schemas you load stay in your browser's storage on your computer. Nothing is uploaded.
- To see a newer version, update your local copy (download again or `git pull`) and load the folder again.
- To match the metadata to the data you hold, use the copy tagged with your data release (see below).
- Folders that only contain a `README.md` are placeholders for data that have not been released yet. The explorer
  skips non-schema files and reports them as "files ignored". This is expected.

## Study-level and resource-level metadata

These levels are JSON-LD documents built on [schema.org](https://schema.org), not table schemas, so Schema Explorer
does not display them. Read them through their generated pages instead, which GitHub shows as formatted text:

- [Study at a glance](study-level-metadata/README.md), generated from the study record
  [`study.json`](study-level-metadata/study.json).
- [Resources overview](resource-level-metadata/README.md), generated from [`ro-crate-metadata.json`](ro-crate-metadata.json).
  The graph is an [RO-Crate 1.1](https://www.researchobject.org/ro-crate/1.1/) document. It is a **placeholder**
  until its content is agreed.

Where schema.org has no suitable term, a file defines its own Generations-specific terms inside itself. Each
generated page lists them in a **Terms** section.

## Versions and data releases

| What changes | Where it is recorded |
|---|---|
| A **data release** | A Git tag on this repository (for example `release-2026.1`) and a page in [`release-notes/`](release-notes/) |
| A **table schema** | Its `x-version` (major = variable renamed or removed, minor = variable added, patch = wording fix) and its `x-dataVersion`, both listed in [`VERSIONS.json`](VERSIONS.json) |
| This **repository** | [`CHANGELOG.md`](CHANGELOG.md) |

If you hold data release X, open tag X (the branch/tag selector at the top of this page) to see the metadata that
matches your data.

## Getting access to the data

This repository describes the data. It does not contain any participant data. For access, see the access section of
[Study at a glance](study-level-metadata/README.md#access).

## For maintainers

The readable pages and `VERSIONS.json` are generated. Edit the sources (the study record, `ro-crate-metadata.json`
and the schema files), then run:

```
pip install -r tools/requirements.txt
python tools/build_docs.py      # regenerate the readable pages and VERSIONS.json
python tools/validate.py        # check schemas, links and that generated files are up to date
```

The same check runs automatically on every push (`.github/workflows/validate.yml`).

To add a released dataset:
1. Copy the dataset folder from the release export into the matching folder under `structural-metadata/schemas/`.
2. Add the dataset to `ro-crate-metadata.json` (once the graph's content is agreed).
3. Run `python tools/build_docs.py`, then `python tools/validate.py`.
4. Add a release-notes page and a `CHANGELOG.md` entry.

## Licence

- Metadata and documentation: [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
- Scripts in `tools/`: [MIT](LICENSE-CODE).
