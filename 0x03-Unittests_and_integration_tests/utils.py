#!/usr/bin/env python3
"""Utils module with access_nested_map"""
def access_nested_map(nested_map, path):
    for key in path:
        nested_map = nested_map[key]
    return nested_map
