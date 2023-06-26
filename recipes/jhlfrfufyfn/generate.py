# this file attempts to generate a part of an audiobook
from TTS.utils.synthesizer import Synthesizer

path_to_files = '/home/jhlfrfufyfn/dev/diplom/tts-files/'
path_to_model = path_to_files + 'best_model_102713.pth'
path_to_config = path_to_files + 'glow-config.json'
path_to_vocoder = path_to_files + 'best_model_215301.pth'
path_to_vocoder_config = path_to_files + 'vocoder-config.json'
path_to_scale_stats = path_to_files + 'scale_stats.npy'
path_to_output = path_to_files + '../book-example/output/'
path_to_text = path_to_files + '../book-example/ipa0.txt'

synthesizer = Synthesizer(
    path_to_model,
    path_to_config,
    None,
    None,
    path_to_vocoder,
    path_to_vocoder_config,
    None,
    None,
    None,
    None,
    False
)

# read text from file
with open(path_to_text, 'r') as file:
    text = file.read().replace('\n', '')

# generate speech
speech = synthesizer.tts(text)

# save speech to file
with open(path_to_output + 'charnyshevich-zascenak-malinauka-0.wav', 'wb') as file:
     synthesizer.save_wav(speech, file)
