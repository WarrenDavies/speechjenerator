import time
import datetime 

from kokoro import KPipeline

from basejenerator.generator_output import GeneratorOutput

from speechjenerator.artifacts.wav_artifact import WavArtifact
from speechjenerator.registry import register_model
from speechjenerator.core.base_speech_generator import BaseSpeechGenerator

@register_model("kokoro")
class Kokoro(BaseSpeechGenerator):
    """
    Concrete implementation of BaseClass for Kokoro.

    """

    def __init__(self, config):
        """
        Initializes the generator.

        Args:
            config (dict): Configuration dictionary. Must include standard BaseClass
                           keys plus model-specific keys.
        """
        super().__init__(config)
        self.model = None


    def load(self):
        """
        Loads Kokoro pipeline.
        """
        pipeline = KPipeline(
            lang_code=self.config["lang"],
            device=self.device,
        )

        self.model = pipeline


    def prepare(self):
        """
        """
        pass

    
    def warmup(self):
        self.generate_impl({
            "text": "Do or do not. There is no try."
        })


    def generate_impl(self, config = None):
        """
        """
        inf_config = self.config.copy()
        if config:
            inf_config.update(config)

        artifacts = []
        for i, (gs, ps, audio) in enumerate(
            self.model(
                text=inf_config["text"], 
                voice=inf_config["voice"]
            )
        ):
            artifacts.append(
                WavArtifact(
                    data=audio,
                    item_extras={
                        "text": gs,
                        "phonemes": ps,
                        "chunk_index": i
                    }
                )
            )
    
        return GeneratorOutput(artifacts)


    def get_params_schema(self):
        class ParamsSchema(BaseModel):
            text: str = ""
            lang: str = ""

        return ParamsSchema