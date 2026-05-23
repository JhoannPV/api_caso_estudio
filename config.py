from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "AirQualityUCI_preparado.csv"

FEATURES = ["PT08.S1(CO)", "PT08.S2(NMHC)", "C6H6(GT)", "NOx(GT)"]

N_CLUSTERS = 2
RANDOM_STATE = 42
