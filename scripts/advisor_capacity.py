"""İzole Colab giriş noktası."""
import os
import sys
from pathlib import Path
os.environ['MPLBACKEND']='Agg'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from yenibot.experiment.advisor_capacity import main
if __name__=='__main__':main()
