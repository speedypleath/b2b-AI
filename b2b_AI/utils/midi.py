import os
from pathlib import Path
# pylint: disable="no-name-in-module"
from mido import MidiFile, open_output
from .logging import get_logger

def get_project_root() -> Path:
    return Path(__file__).parent.parent

root = get_project_root()
os.chdir(get_project_root())
logger = get_logger('logs/midi.log')

def play_song(mid: MidiFile) -> None:
    output = open_output('Virtual Port', virtual=True)
    for msg in mid.play():
        output.send(msg)
    output.close()

def in_range(number: float, first: float, last: float) -> bool:
    return first <= number <= last

def next_file(file: str) -> str:
    tree = file.split('/')
    count = int(tree.pop()[:-4])
    count += 1
    return f'{"/".join(tree)}/{count}.mid'

def create_dir_if_not_exists(directory: str) -> None:
    if not os.path.exists(directory):
        logger.info('Directory does not exist')
        os.mkdir(directory)

def normalize_data(directory: str, parent: str) -> None:
    os.chdir(get_project_root())
    os.chdir(parent)
    create_dir_if_not_exists(f'{directory}-8bar')

    files = os.listdir(f'{directory}')
    new_file = f'{directory}-8bar/1.mid'

    for file in files:
        if file.split('.')[-1] != 'mid':
            continue

        mid = MidiFile(f'{directory}/{file}')

        if in_range(mid.length, 3.5, 4.5):
            logger.info('%s: 2 bars in file %s', file, new_file)
            track = mid.tracks[0] + list(filter(lambda msg: not msg.is_meta, mid.tracks[0]))
        elif in_range(mid.length, 14, 18):
            logger.info('%s: 8 bars in file %s', file, new_file)
            filtered_msg = list(filter(lambda msg: not msg.is_meta, mid.tracks[0]))
            meta_msg = list(filter(lambda msg: msg.is_meta, mid.tracks[0]))
            track = meta_msg + filtered_msg[:len(filtered_msg) // 2]
            del mid.tracks[0]
            mid.tracks = []
            mid.tracks.append(track)
            mid.save(new_file)
            new_file = next_file(new_file)
            track = meta_msg + filtered_msg[len(filtered_msg) // 2:]
        elif in_range(mid.length, 7, 9):
            logger.info('%s: 4 bars in file %s', file, new_file)
            track = mid.tracks[0]
        else:
            logger.warning('%s: %d', file, mid.length)
            continue

        with open(new_file, 'wb') as file:
            del mid.tracks[0]
            mid.tracks = []
            mid.tracks.append(track)
            mid.save(new_file)
            new_file = next_file(new_file)
            file.close()
