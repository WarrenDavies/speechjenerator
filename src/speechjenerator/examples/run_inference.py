from speechjenerator.models import registry

config = {
    # model
    "model": "",
    "model_path": "",
    # hardware/system

    # model parama
}



speech_generator = registry.get_model_class(config)
speech_generator.load()
output = text_generator.generate()
response = output.batch[0].data
