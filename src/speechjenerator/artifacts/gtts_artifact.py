import sounddevice as sd
import soundfile as sf

from basejenerator.artifacts.base_artifact import BaseArtifact

class GTTSArtifact(BaseArtifact):
    """
    Holds a gTTS object. This is more like a promise to create an audio file.
    Due to how gTTS works, the Google Translate API is not called until `.save()`
    is called.

    Attributes:
        data (str): The gTTS object.
        item_extras (dict): any additional metadata related to this artifact
    """

    def __init__(self, data, item_extras):
        self.data = data 
        self.item_extras = item_extras
        self.extension = ".wav"


    def save(self, path):
        """
        Called Google Translate API, gets the audio as WAV, and saves to disk.
        """
        self.data.save(path)


    def play(self, path=None):
        """
        Called Google Translate API, gets the audio as WAV, and saves to disk.
        """
        if not path:
            path = self.data["config"]["path"]
        self.save(path)
        data, fs = sf.read(path, dtype='float32')
        sd.play(data, fs)
        sd.wait()
