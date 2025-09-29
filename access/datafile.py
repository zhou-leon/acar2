from pathlib import Path
access_path = Path(__file__).parent.absolute()
DATA_PATH = access_path.parent.joinpath('data')

VEHICLES = DATA_PATH.joinpath('vehicles.xml').as_posix()
EVENT_SUBTYPES = DATA_PATH.joinpath('event-subtypes.xml').as_posix()
TEST = DATA_PATH.joinpath('test.xml').as_posix()
