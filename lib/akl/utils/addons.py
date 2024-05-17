# -*- coding: utf-8 -*-

# AKL addon utilities

# Copyright (c) chrisism
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

#
# --- Python standard library ---
from __future__ import unicode_literals
from __future__ import division
from __future__ import annotations

import argparse
import json

# AKL libraries
import constants


def argument_parsing_for_addons(addon_name):

    parser = argparse.ArgumentParser(prog=addon_name)
    parser.add_argument('--cmd', help="Command to execute", choices=['launch', 'scan', 'scrape', 'configure'])
    parser.add_argument('--type', help="Plugin type", choices=['LAUNCHER', 'SCANNER', 'SCRAPER'], default=constants.AddonType.LAUNCHER.name)
    parser.add_argument('--server_host', type=str, help="Host")
    parser.add_argument('--server_port', type=int, help="Port")
    parser.add_argument('--source_id', type=str, help="Source ID")
    parser.add_argument('--entity_id', type=str, help="Entity ID")
    parser.add_argument('--entity_type', type=int, help="Entity Type (ROM|ROMCOLLECTION|SOURCE)")
    parser.add_argument('--akl_addon_id', type=str, help="Addon configuration ID")
    parser.add_argument('--settings', type=json.loads, help="Specific run setting")