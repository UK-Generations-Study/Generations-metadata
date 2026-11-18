# Biomarker assays

Hormone and biomarker assay results.

**Placeholder: no released schema yet.**

When a release adds this data, put the released dataset folder here exactly as the release export produces it
(its `common/` folder and one folder per table), so its `$ref` links keep working.
Table schema files are named like `<Name>.schema.json`.
Then add the dataset to `ro-crate-metadata.json` and run `python tools/build_docs.py`.
