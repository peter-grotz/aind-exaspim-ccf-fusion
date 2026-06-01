#!/usr/bin/env python3
"""Bare-minimum metadata for the CCF fusion capsule.

Emits a lightweight process_record.json (schema-agnostic) describing the CCF
channel fusion (and the mask fusion done with the same transforms). The upload
capsule converts records -> validated v2 Processing. Because fusion writes to
S3 (not through the nextflow channel to upload), the record is also copied to
the asset's S3 fusion/ folder so the upload builder can pick it up.

Usage: python emit_fusion_record.py [START_ISO]
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

from aind_process_record import make_record, write_records


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> None:
    start = sys.argv[1] if len(sys.argv) > 1 else _now()
    end = _now()

    # provenance from the manifest
    manifest = next((os.path.join("../data", f) for f in os.listdir("../data")
                     if f.endswith(".json")), None)
    input_uri = ""
    if manifest:
        try:
            input_uri = str(json.load(open(manifest)).get("zarr_multiscale", {}).get("input_uri", ""))
        except Exception:
            pass
    base = input_uri.split("/fusion/")[0] if "/fusion/" in input_uri else ""

    record = make_record(
        process_type="Image tile fusing",
        name="CCF channel fusion",
        start=start,
        end=end,
        code_url="https://codeocean.allenneuraldynamics.org/capsule/1941809/tree",
        code_name="aind-exaspim-ccf-fusion",
        code_version=os.environ.get("CODE_VERSION", "0.0.0"),
        run_script="/code/run",
        language="Java",
        parameters={
            "input_xml": "tile_alignment/ch_ccf_xmls/bigstitcher_split_affine_ch_ccf.xml",
            "main_class": "net.preibisch.bigstitcher.spark.SparkAffineFusion",
            "block_scale": "4,4,4",
            "data_type": "UINT16",
            "storage_format": "ZARR",
            "mask_fused": True,
            "mask_output": "fusion/fused_mask_ch.zarr",
        },
        output_path="fusion/fused_ccf_ch.zarr",
        notes=("Fuses the CCF-alignment channel; also fuses the flat-field mask "
               "with identical transforms (fused_mask_ch.zarr, registration-only "
               "intermediate)."),
    )

    local = write_records([record], "/results/fusion")
    print(f"wrote {local}")

    # bridge to the upload capsule: copy the record into the asset's S3 fusion/ folder
    if base:
        dest = f"{base}/fusion/process_record.json"
        subprocess.run(["aws", "s3", "cp", local, dest], check=False)
        print(f"copied record to {dest}")


if __name__ == "__main__":
    main()
