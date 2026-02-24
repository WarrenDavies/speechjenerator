from abc import ABC, abstractmethod
import datetime
import time
import os
import random
import torch
import gc

from basejenerator.base_generator import BaseGenerator


class BaseSpeechGenerator(BaseGenerator):
    """
    Abstract base class for TTS.

    This class handles... 
    
    Subclasses must implement create_pipeline() and run_pipeline()

    Attributes:
        config (dict): Configuration dictionary containing model parameters, paths, and settings.
    """

    def __init__(self, config):
        """
        Initializes the object with a config.

        Args:
            config (dict): A dictionary containing configuration parameters.
                Expected keys include:
                - 
        """
        self.config = config
        self.device = self.set_device()
 

    def set_device(self):
        """
        Sets the computation device based on CUDA availability.

        Sets `self.device` to 'cuda' if available, otherwise defaults to 'cpu'.
        """
        if "device" in self.config:
            return self.config["device"]

        if torch.cuda.is_available():
            return "cuda"
        else:
            return "cpu"


    @abstractmethod
    def load(self):
        """
        Abstract method to initialize the model pipeline.
        
        Subclasses must implement this to load the specific model and tokenizer/pipeline object, assigning it to self.pipe (e.g., a Hugging Face Pipeline object).
        """
        pass


    @abstractmethod
    def prepare(self):
        """
        Reset lifecycle without tearing down the model - e.g., clear cache, etc.
        """
        pass


    @abstractmethod
    def warmup(self):
        """
        Initial inference run to create cache etc., mainly for benchmarking.
        """
        pass


    def generate(self):
        """
        The public API that runs inference.

        Returns:
            GeneratorOutput
        """
        return self.generate_impl()


    @abstractmethod
    def generate_impl(self):
        """
        The public API that runs inference.

        Returns:
            GeneratorOutput        
        """
        pass


    def teardown(self):
        """
        Deletes the pipeline, empties the torch cache, and forces Python's garbage collector to run. Clears the slate to create
        another pipeline.
        """
        if self.model is None:
            print("No pipeline found. You cannot teardown that which was not created.")
            return

        del self.model
        self.model = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        gc.collect()