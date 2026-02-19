import os
import platform
import subprocess
import datetime
import soundfile as sf

from basejenerator.artifacts.base_artifact import BaseArtifact


class WavArtifact(BaseArtifact):
    """
    
    Attributes:
        data (str): The gTTS "model" object.
        item_extras (dict): any additional metadata related to this artifact
    """

    def __init__(self, data, item_extras):
        self.data = data 
        self.item_extras = item_extras
        self.extension = ".wav"
        self.system = platform.system()
        self.linux_players = [
            ["mpv", "--no-terminal"],
            ["mpg123", "--quiet"],

        ]
        self.player_funcs = {
            "Windows": self._play_on_windows,
            "Darwin": self._play_on_mac,
            "Linux": self._play_on_linux
        }


    def save(self, path):
        """
        """
        if "chunk_index" in self.item_extras:
            extension = f"_{str(self.item_extras['chunk_index'])}{self.extension}"
        else:
            extension = self.extension

        self.path = f'{path}{extension}'
        sf.write(self.path, self.data.data, 24000)


    def _play_on_windows(self, path):
        os.startfile(path)


    def _play_on_mac(self, path):
        subprocess.run(['afplay', path])


    def _play_on_linux(self, path):
        for player_command in self.linux_players:
            player_command.append(path)
            try:
                subprocess.run(player_command, check=True)
                break
            except FileNotFoundError:
                continue


    def play(self, path=None):
        """
        """
        if not path:
            path = self.data["config"]["path"]
        self.save(path)

        player = self.player_funcs[self.system]
        try:
            player(self.path)
        except Exception as e:
            print(f"Error playing audio: {e}")
