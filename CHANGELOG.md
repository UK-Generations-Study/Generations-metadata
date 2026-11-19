# Changelog

Changes to this repository. Changes to the data themselves are described in [`release-notes/`](release-notes/).

## Unreleased

- Renamed `variable-level-metadata/` to `structural-metadata/`; its README now covers schema organisation,
  naming and versioning conventions and how to use the schemas.
- Added a `mammograms/` placeholder folder beside `imaging/`.
- Renamed the study record to `study-level-metadata/study.json` and converted it from the HDR UK Gateway v4 format
  to JSON-LD (schema.org). Every value is kept; fields with no schema.org term use Generations-specific terms
  defined inside the file.
- Removed `resource-level-metadata/terms.md`. Generations-specific terms are now defined inside each JSON-LD file and
  listed in a Terms section of its generated page.
- Repository renamed to Generations-metadata.
- Repository structure created: study-level, resource-level and structural metadata folders.
- Study record added (HDR UK Gateway v4 metadata).
- Resource graph (`ro-crate-metadata.json`) added as a placeholder.
- Placeholder folders for every round and data source.
- Scripts to generate the study and resource pages and `VERSIONS.json`, and to check the metadata; the check runs
  automatically on every push.
- Licences: CC BY 4.0 (metadata and documentation), MIT (scripts).
