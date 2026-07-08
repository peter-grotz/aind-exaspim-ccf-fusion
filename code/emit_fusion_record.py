#!/usr/bin/env python3
"""Emit the CCF fusion process record.

Writes a v2 DataProcess document (*_data_process.json) describing the CCF channel
fusion to /results only. It is not published to S3; the upload capsule merges it
into the root processing.json.

The flat-field brain mask is fused and recorded separately by the
aind-exaspim-mask-fusion capsule (Rhapso).

Usage: python emit_fusion_record.py [START_ISO]
"""
import os
import sys
from datetime import datetime, timezone

from aind_process_record import make_data_process, write_data_process


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> None:
    start = sys.argv[1] if len(sys.argv) > 1 else _now()
    end = _now()

    parameters = {
        "input_xml": "tile_alignment/ch_ccf_xmls/bigstitcher_split_affine_ch_ccf.xml",
        "main_class": "net.preibisch.bigstitcher.spark.SparkAffineFusion",
        "block_scale": "4,4,4",
        "data_type": "UINT16",
        "storage_format": "ZARR",
    }

    data_process = make_data_process(
        process_type="Image tile fusing",
        name="CCF channel fusion",
        start=start,
        end=end,
        code_url="https://codeocean.allenneuraldynamics.org/capsule/1941809/tree",
        code_name="aind-exaspim-ccf-fusion",
        code_version=os.environ.get("CODE_VERSION", "0.0.0"),
        run_script="/code/run",
        language="Java",
        experimenters=["Peter Grotz"],
        parameters=parameters,
        output_path="fusion/fused_ccf_ch.zarr",
        notes=("Fuses the CCF-alignment channel. The flat-field brain mask is fused "
               "separately by the aind-exaspim-mask-fusion capsule."),
    )

    # Write to /results only; the upload capsule merges it into the root
    # processing.json. Not published to S3.
    local = write_data_process(data_process, "/results/fusion")
    print(f"wrote {local} (results-only; not published to S3)")


if __name__ == "__main__":
    main()
