#!/usr/bin/env python3
"""Bare-minimum metadata for the CCF fusion capsule.

Emits a v2 DataProcess document (*_data_process.json) describing the CCF channel
fusion (and the mask fusion done with the same transforms) to /results ONLY.
It is NOT published to S3: it flows to the upload capsule via the pipeline's
/results channel, where aind-metadata-manager merges it into the ROOT
processing.json. The existing fusion/processing.json on S3 is left untouched.

Usage: python emit_fusion_record.py [START_ISO] [MASK_FUSION_STATUS]
  MASK_FUSION_STATUS is the EMR mask job's terminal state (SUCCESS/FAILED/...);
  it is recorded so the processing.json shows whether the flat-field mask was
  actually fused (and thus whether registration ran masked).
"""
import os
import sys
from datetime import datetime, timezone

from aind_process_record import make_data_process, write_data_process


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> None:
    start = sys.argv[1] if len(sys.argv) > 1 else _now()
    # Mask fusion status (EMR terminal state). Recorded so processing.json reflects
    # whether the flat-field mask was actually produced; if not, registration runs
    # unmasked and we do NOT claim a fused_mask_ch.zarr output.
    mask_status = (sys.argv[2] if len(sys.argv) > 2
                   else os.environ.get("MASK_FUSION_STATUS", "UNKNOWN"))
    mask_ok = mask_status.strip().upper() == "SUCCESS"
    end = _now()

    parameters = {
        "input_xml": "tile_alignment/ch_ccf_xmls/bigstitcher_split_affine_ch_ccf.xml",
        "main_class": "net.preibisch.bigstitcher.spark.SparkAffineFusion",
        "block_scale": "4,4,4",
        "data_type": "UINT16",
        "storage_format": "ZARR",
        "mask_fused": mask_ok,
        "mask_fusion_status": mask_status,
    }
    if mask_ok:
        parameters["mask_output"] = "fusion/fused_mask_ch.zarr"
        mask_note = ("also fuses the flat-field mask with identical transforms "
                     "(fused_mask_ch.zarr, a registration-only intermediate).")
    else:
        mask_note = (f"the flat-field mask fusion did NOT succeed "
                     f"(mask_fusion_status={mask_status}); the empty fused_mask_ch.zarr "
                     f"container was removed, so registration runs UNMASKED for this subject.")

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
        notes="Fuses the CCF-alignment channel; " + mask_note,
    )

    # Write the data_process to /results ONLY (NOT to S3). It reaches the upload
    # capsule via the pipeline's /results channel, where it is merged into the
    # ROOT processing.json. We deliberately do not publish it to the S3 asset, and
    # the existing fusion/processing.json on S3 is left untouched.
    local = write_data_process(data_process, "/results/fusion")
    print(f"wrote {local} (results-only; not published to S3)")


if __name__ == "__main__":
    main()
