# Variable-level metadata

One JSON Schema per released table. Each schema lists the table's variables with their labels, descriptions, data
types, valid values (codes and their meanings), missing-value codes and constraints.

The schema files are in **[`schemas/`](schemas/)**, grouped by source. Open this folder in
[Schema Explorer](../README.md#viewing-the-schemas-in-schema-explorer) to browse them.

## Source folders

| Folder | Contents |
|---|---|
| [`questionnaires/R0`](schemas/questionnaires/R0/) … [`R5`](schemas/questionnaires/R5/) | Questionnaire rounds: R0 baseline, R1 (TwoHalfQ) to R5 follow-ups |
| [`derived/`](schemas/derived/) | Derived variables |
| [`administration/`](schemas/administration/) | Study administration |
| [`linkage/`](schemas/linkage/) | Linked registry and NHS data |
| [`biospecimens/`](schemas/biospecimens/) | Biobank samples |
| [`biomarker_assays/`](schemas/biomarker_assays/) | Hormone and biomarker assays |
| [`pathology/`](schemas/pathology/) | Tissue and pathology |
| [`imaging/`](schemas/imaging/) | Mammograms |
| [`accelerometry/`](schemas/accelerometry/) | Accelerometer data |
| [`genomics/`](schemas/genomics/) | Genotyping and sequencing |

A folder holding only a `README.md` is a placeholder: those data have not been released yet.

## How a released dataset is laid out

Each dataset sits in its source folder exactly as the release export produces it:

```
<source folder>/<Dataset>/
├── common/defs.json                   shared definitions (for example missing-value codes)
└── <Table>/
    ├── <Table>.schema.json            the table: one record per row
    └── categories/*.json              groups of variables, referenced by the table schema
```

Only the `<Table>.schema.json` files are tables. The other files are referenced from them.
