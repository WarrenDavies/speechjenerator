from speechjenerator import registry

output_path = "./outputs/test.wav"
config = {
    "model": "gtts",

    "text": "Hazlo o no lo hagas. Intentar no existe.",
    "lang": "es"

}

speech_generator = registry.get_model_class(config)
speech_generator.load()
print(speech_generator.config)
output = speech_generator.generate()
speech = output.batch[0]
speech.play(output_path)
