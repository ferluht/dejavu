import json

from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
from dejavu.logic.recognizer.microphone_recognizer import MicrophoneRecognizer
import pandas as pd

import sys
import tqdm

# load config from a JSON file (or anything outputting a python dictionary)
config = {
    "database": {
        "host": "localhost",
        "user": "postgres",
        "password": "password",
        "database": "dejavu"
    },
    "database_type": "postgres"
}

if __name__ == '__main__':

    root = sys.argv[1]
    filelist = pd.read_csv(sys.argv[2], sep=',', header=None)
    chunk_size = int(sys.argv[3])
    filenames = []

    pbar = tqdm(total=filelist.shape[0])

    for index, row in filelist.iterrows():

        filename = row.values[-1].split('/')[-1]
        filename = os.join(root, filename)

        try:
            data = scipy.io.wavfile.read(filename)
            filenames.append(filename)
        except Exception as e:
            pass
        
        if len(filenames) >= chunk_size:
            djv = Dejavu(config)
            djv.fingerprint_filelist(filenames)
            pbar.update(1)
            filenames = []

    # # Recognize audio from a file
    # results = djv.recognize(FileRecognizer, "mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")
    # print(f"From file we recognized: {results}\n")

    # # Or use a recognizer without the shortcut, in anyway you would like
    # recognizer = FileRecognizer(djv)
    # results = recognizer.recognize_file("mp3/Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")
    # print(f"No shortcut, we recognized: {results}\n")
