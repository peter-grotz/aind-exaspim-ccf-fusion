"""Marks a brain's row in SmartSheet as CCF-fused after fusion completes."""

from aind_exaspim_dataset_utils.smartsheet_util import SmartSheetClient
from datetime import datetime

import json
import os
import re


class PaginatedSmartSheetClient(SmartSheetClient):
    # list_sheets() returns only the first 100 sheets by default;
    # include_all=True returns every sheet so the name lookup is reliable.
    def find_sheet_id(self):
        response = self.client.Sheets.list_sheets(include_all=True)
        for sheet in response.data:
            if sheet.name == self.sheet_name:
                return sheet.id
        raise Exception(f"Sheet Not Found - sheet_name={self.sheet_name}")


def main():
    # Read the API token from the SMARTSHEET_TOKEN env var; skip the update if unset.
    access_token = os.environ.get("SMARTSHEET_TOKEN")
    if not access_token:
        print("SMARTSHEET_TOKEN not set; skipping SmartSheet update.")
        return
    brain_id = find_brain_id()
    update_smartsheet(brain_id, access_token)


def find_brain_id():
    # Load JSON and extract brain_id
    manifest_json_path = find_manifest_json_path()
    manifest = read_json(manifest_json_path)
    uri = manifest['zarr_multiscale']['input_uri']

    # Extract brain ID
    # Prefix-agnostic: asset names dropped the "exaSPIM_" prefix when aind-data-schema
    # went to v2 (v2 removed data_description.platform), so anchor on the acquisition
    # datestamp that follows the subject id rather than requiring the platform prefix.
    result = re.search(r'(?<!\d)(\d{6})_\d{4}-\d{2}-\d{2}', uri)
    if not result:
        raise ValueError(f"Could not extract subject id from {uri}")
    return result.group(1)


def read_json(path):
    with open(path, "r") as file:
        return json.load(file)


def find_manifest_json_path():
    # Find all json paths
    data_dir = os.path.abspath("../data")
    json_paths = [p for p in os.listdir(data_dir) if p.endswith(".json")]

    # Get manifest path
    filenames = [p for p in json_paths if "manifest" in p.lower()]
    assert len(filenames) == 1, f"JSONs Found: {filenames}"
    manifest_json_path = os.path.join(data_dir, filenames[0])
    return manifest_json_path


def update_smartsheet(brain_id, access_token):
    # Initialize client
    sheet_name = "ExM Dataset Summary"
    client = PaginatedSmartSheetClient(access_token, sheet_name)
    column_map = {col.title: col.id for col in client.sheet.columns}

    # Update SmartSheet
    updated_row = client.client.models.Row()
    updated_row.id = client.find_row_id(brain_id)
    updated_row.cells.append({
        'column_id': column_map.get('CCF Fused'),
        'value': True,
        'strict': False
    })
    updated_row.cells.append({
        'column_id': column_map.get('CCF Fused Date'),
        'value': datetime.today().strftime("%m/%d/%Y"),
        'strict': False
    })

    # Send row update
    client.client.Sheets.update_rows(client.sheet_id, [updated_row])


if __name__ == "__main__":
    main()
