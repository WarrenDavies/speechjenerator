import time
import datetime 

from gtts import gTTS

from basejenerator.generator_output import GeneratorOutput

from speechjenerator.artifacts.gtts_artifact import GTTSArtifact
from speechjenerator.registry import register_model
from speechjenerator.core.base_speech_generator import BaseSpeechGenerator


@register_model("gtts")
class GTTS(BaseSpeechGenerator):
    """
    Concrete implementation of BaseClass for gTTS.

    """

    def __init__(self, config):
        """
        Initializes the gTTS generator.

        Args:
            config (dict): Configuration dictionary. Must include standard BaseClass
                           keys plus model-specific keys.
        """
        super().__init__(config)


    def load(self):
        """
        No-op - gTTS uses a remote API (Google Translate).
        """
        pass


    def prepare(self):
        """
        No-op - gTTS uses a remote API (Google Translate).
        """
        pass


    def generate_impl(self, text=None, lang=None):
        """
        """
        if not text:
            text = self.config["text"]

        if not lang:
            lang = self.config["lang"]

        gtts_obj = gTTS(text=text, lang=lang)

        artifacts = self._quick_wrap([gtts_obj], [{}], GTTSArtifact)

        return GeneratorOutput(artifacts)


    def teardown(self):
        """
        No-op - gTTS uses a remote API (Google Translate).
        """
        pass


    def get_params_schema(self):
        class ParamsSchema(BaseModel):
            text: str = ""
            lang: str = ""

        return ParamsSchema