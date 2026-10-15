"""Entry point for a pinned interpreter invoked with -I."""
import os
import sys
from pathlib import Path

# Must run before importing yenibot.experiment and its plotting dependencies.
os.environ['MPLBACKEND'] = 'Agg'

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from yenibot.experiment.advisor_workspace import main

if __name__ == '__main__':
    main()
