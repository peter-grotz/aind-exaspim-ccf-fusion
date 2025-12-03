"""
Created on Wed Dec 3 14:00:00 2025

@author: Anna Grim
@email: anna.grim@alleninstitute.org

Code for updating SmartSheet after CCF fusion has completed.

"""


def main():
    # Update SmartSheet
    access_token = "9Mx3umDssV5ugK9roAf9EEXQPmZq2ovX7tPyR"
    brain_id = find_brain_id()
    update_smartsheet(brain_id, access_token)


def find_brain_id():
    # Load JSON and extract brain_id
    manifest_json_path = find_manifest_json_path()
    manifest = util.read_json(manifest_json_path)
    uri = manifest['zarr_multiscale']['input_uri']

    # Extract brain ID
    result = re.search(r'exaspim_(\d{6})', uri.lower())
    if not result:
        raise ValueError(f"Could not extract exaSPIM ID from {uri}")
    brain_id = result.group(1)
    return brain_id


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
    client = SmartSheetClient(access_token, sheet_name)
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
