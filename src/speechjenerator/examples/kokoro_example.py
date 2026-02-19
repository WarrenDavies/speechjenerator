from speechjenerator import registry
import datetime


output_path = "./outputs/"
config = {
    "model": "kokoro",

    "text": """Hazlo o no lo hagas.
    Intentar no existe.""",
    "lang": "es",
    "voice": "ef_dora",

}


filename_stem = datetime.datetime.now().strftime(format="%Y-%m-%d_%H-%M-%s")
speech_generator = registry.get_model_class(config)
print("loading model...")
speech_generator.load()
print("warmup run...")
speech_generator.warmup()
print("running inference...")
output = speech_generator.generate()
for chunk in output.batch:
    chunk.play(output_path + filename_stem)
print("tearing down...")    
speech_generator.teardown()
print("done!")