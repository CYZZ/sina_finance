import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from Stategy.mygrid import MyGrid

MyGrid.get_rolling_rate()