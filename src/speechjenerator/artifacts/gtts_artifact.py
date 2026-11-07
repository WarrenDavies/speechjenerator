import os
import platform
import subprocess

import sounddevice as sd
import soundfile as sf

from basejenerator.artifacts.base_artifact import BaseArtifact

class GTTSArtifact(BaseArtifact):
    """
    Holds a gTTS "model" object. This is more like a promise to create an audio file.
    Due to how gTTS works, the Google Translate API is not called until `.save()`
    is called.

    Attributes:
        data (str): The gTTS "model" object.
        item_extras (dict): any additional metadata related to this artifact
    """

    def __init__(self, data, item_extras):
        self.data = data 
        self.item_extras = item_extras
        self.extension = ".mp3"
        self.system = platform.system()
        self.linux_mp3_players = [
            ["mpg123", "--quiet"],
            ["mpv", "--no-terminal"],
        ]
        self.player_funcs = {
            "Windows": self._play_on_windows,
            "Darwin": self._play_on_mac,
            "Linux": self._play_on_linux
        }

    def save(self, path):
        """
        Called Google Translate API, gets the audio as WAV, and saves to disk.
        """
        self.data.save(path)


    def _play_on_windows(self, path):
        os.startfile(path)

    def _play_on_mac(self, path):
        subprocess.run(['afplay', path])

    def _play_on_linux(self, path):
        for player_command in self.linux_mp3_players:
            player_command.append(path)
            try:
                subprocess.run(player_command, check=True)
                break
            except FileNotFoundError:
                continue

    def play(self, path=None):
        """
        Calls Google Translate API, gets the audio as mp3, saves to disk,
        and plays the audio on the system in which speechjenerator is running
        using .
        """
        if not path:
            path = self.data["config"]["path"]
        self.save(path)

        mp3_player = self.player_funcs[self.system]
        try:
            mp3_player(path)
        except Exception as e:
            print(f"Error playing audio: {e}")