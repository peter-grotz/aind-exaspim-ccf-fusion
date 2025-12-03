"""
Created on Wed Dec 3 14:00:00 2025

@author: Anna Grim
@email: anna.grim@alleninstitute.org

Code for updating SmartSheet that CCF fusion has completed.

"""


def main():
    # Update SmartSheet
    access_token = "9Mx3umDssV5ugK9roAf9EEXQPmZq2ovX7tPyR"
    brain_id = find_brain_id(dataset_path)
    update_smartsheet(brain_id, access_token)