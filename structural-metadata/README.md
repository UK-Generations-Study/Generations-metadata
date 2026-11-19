# Structural metadata

One JSON Schema per released table. Each schema describes the table's structure: its variables, labels,
descriptions, data types, allowed values (codes and their meanings), missing-value codes and constraints.

The schema files are in **[`schemas/`](schemas/)**, grouped by data source.

## How to use the schemas

- **Browse them in Schema Explorer:**
  1. Get a local copy of this repository: **Code → Download ZIP** at the top of the repository page, or `git clone`.
  2. Open **[Schema Explorer](https://jeyabbalas.github.io/schema-explorer/)**.
  3. Drag the `structural-metadata/schemas/` folder (or one dataset's folder) onto the page.

  Full steps, and what you will see: [Viewing the schemas in Schema Explorer](../README.md#viewing-the-schemas-in-schema-explorer).
- **Match them to your data**: use the version of this repository tagged with your data release. Each table's
  version is listed in [`VERSIONS.json`](../VERSIONS.json).
- Guides for loading the data and using the schemas in R and Python will be added to [`guides/`](../guides/).

## Schema organisation

| Folder | Contents |
|---|---|
| [`questionnaires/R0`](schemas/questionnaires/R0/) … [`R5`](schemas/questionnaires/R5/) | Questionnaire rounds: R0 baseline, R1 (TwoHalfQ) to R5 follow-ups |
| [`derived/`](schemas/derived/) | Derived variables |
| [`administration/`](schemas/administration/) | Study administration |
| [`linkage/`](schemas/linkage/) | Linked registry and NHS data |
| [`biospecimens/`](schemas/biospecimens/) | Biobank samples |
| [`biomarker_assays/`](schemas/biomarker_assays/) | Hormone and biomarker assays |
| [`pathology/`](schemas/pathology/) | Tissue and pathology |
| [`imaging/`](schemas/imaging/) | Imaging data other than mammograms |
| [`mammograms/`](schemas/mammograms/) | Mammograms |
| [`accelerometry/`](schemas/accelerometry/) | Accelerometer data |
| [`genomics/`](schemas/genomics/) | Genotyping and sequencing |

A folder holding only a `README.md` is a placeholder: those data have not been released yet.

Each released dataset sits in its source folder exactly as the release export produces it:

```
<source folder>/<Dataset>/
├── common/defs.json                   shared definitions (for example missing-value codes)
└── <Table>/
    ├── <Table>.schema.json            the table: one record per row
    └── categories/*.json              groups of variables, referenced by the table schema
```

Only the `<Table>.schema.json` files are tables. The other files are referenced from them, by relative path.

## Naming conventions

| Item | Convention | Example |
|---|---|---|
| Questionnaire rounds | `R0` (baseline) to `R5` (fifth follow-up) | `questionnaires/R1/` |
| Table schema files | Words capitalised and joined by `_`, ending in `.schema.json` | `R0_Questionnaire.schema.json` |
| Source folders | Lower case, words joined by `_` | `biomarker_assays/` |

## Versioning conventions

Each table schema carries two version fields:

| Field | Meaning | Changes when |
|---|---|---|
| `x-version` | Version of the schema (its structure) | **Major** (2.0.0): a variable renamed or removed, which may break analysis code · **Minor** (1.1.0): a variable added · **Patch** (1.0.1): a wording fix |
| `x-dataVersion` | Version of the data the schema describes | A new data extract |

Both are collected in [`VERSIONS.json`](../VERSIONS.json). Each data release is also a Git tag on this repository,
described in [`release-notes/`](../release-notes/).
