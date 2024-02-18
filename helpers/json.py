"""
********************************************************************************
* SPDX-License-Identifier: MIT
* SPDX-FileType: OTHER
* SPDX-FileCopyrightText: (c) 2024, OpenGateware authors and contributors
********************************************************************************
*
* JSON Helpers
* Copyright (c) 2024, Marcus Andrade <marcus@opengateware.org>
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the "Software"), to deal
* in the Software without restriction, including without limitation the rights
* to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
* copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
* OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
* SOFTWARE.
********************************************************************************
"""

import json
import os
from datetime import date


def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {json_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_json_file(json_path, data, debug=False):
    if debug:
        print("JSON content being saved to", json_path)
        print(json.dumps(data, indent=4))
    try:
        with open(json_path, 'w') as file:
            json.dump(data, file, indent=4)
            return True
    except FileNotFoundError:
        print(f"File not found: {json_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {json_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def read_gateware_json():
    workspace = os.getenv('GITHUB_WORKSPACE')
    json_path = os.path.join(workspace, "gateware.json")
    if not os.path.exists(json_path):
        print(f"Error: {json_path} does not exist.")
        return

    return read_json_file(json_path)


def update_apf_core_json(config):
    stage_folder = config['release']['folders']['stage_folder']
    core_folder = f"{config['author']}.{config['name']}"
    version = os.getenv('GITHUB_REF').split('/')[-1]

    print("Updating core.json...")
    # Read the existing JSON file
    json_path = os.path.join(stage_folder, "Cores", core_folder, "core.json")
    data = read_json_file(json_path)

    # Update the version and release date
    current_date = date.today().strftime("%Y-%m-%d")

    if 'core' in data and 'metadata' in data['core']:
        data['core']['metadata']['version'] = version
        data['core']['metadata']['date_release'] = current_date
    else:
        print("Error: JSON structure is not as expected.")
        return

    # Write the updated JSON back to the file
    save_json_file(json_path, data, True)
