# aind-exaspim-ccf-fusion

Fuses the **CCF-alignment channel** (and, with identical transforms, the
flat-field **brain mask**) from BigStitcher-stitched tiles into OME-Zarr, using
BigStitcher-Spark on **AWS EMR Serverless**. Part of the exaSPIM
CCF-registration + soma-reg pipeline (Code Ocean pipeline `9578158`).

## Run it standalone

```bash
cd code && ./run
```

`run` is a bash script — it reads the manifest, derives the BigStitcher XML,
submits the CCF + mask fusion jobs to EMR Serverless, polls them, then writes a
metadata record.

## Inputs (must be present in `../data/`)
- `exaspim_manifest1.json` — manifest whose `zarr_multiscale.input_uri` points at
  the processed asset. The tile XML is read from
  `<asset>/tile_alignment/ch_ccf_xmls/bigstitcher_split_affine_ch_ccf.xml`, and
  tiles + mask tiles from `<asset>/flatfield_correction/...` on S3.
- **AWS credentials** with EMR Serverless + S3 access (the fusion runs on EMR
  under `aind-emr-role`).

## Environment variables (all optional)
- `OUTPUT_PREFIX` — if set (e.g. `s3://aind-scratch-data/exaspim_processing_test`),
  fused outputs go to `<OUTPUT_PREFIX>/<asset>/fusion/`; if unset, alongside the
  input asset (production).
- `CODE_VERSION` — stamped into the emitted metadata record.
- `SMARTSHEET_TOKEN` — if set, updates the tracking sheet; **leave unset for test
  runs** so production SmartSheet isn't touched.

## Outputs
- `<out>/fusion/fused_ccf_ch.zarr` and `<out>/fusion/fused_mask_ch.zarr` (S3).
- `/results/fusion/ccf_channel_fusion_data_process.json` — metadata record the
  upload capsule aggregates into the asset's `processing.json`.

## Notes
- The CCF fusion is **required**; if it fails the script exits non-zero. The mask
  fusion is optional (registration runs unmasked if it's missing).
- It does **not** publish the metadata record to S3 — that flows to the upload
  capsule via the pipeline's `/results`.
