from speechjenerator import registry

output_path = "./outputs/test.wav"
config = {
    "model": "gtts",

    "text": "Do or do not - there is no try.",
    "lang": "en"

}

speech_generator = registry.get_model_class(config)
speech_generator.load()
output = speech_generator.generate()
speech = output.batch[0]
speech.play(output_path)
