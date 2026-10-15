"""Compatibility launcher for the read-only final archive notebook."""
from build_advisor_notebooks_v2 import build as build_phase

def build():
    return build_phase("final")

if __name__ == "__main__":
    build()
