# Bel-TTS project
## Introduction
In this project I use a fork from [Coqui-TTS](https://github.com/coqui-ai/TTS/tree/main) 
framework to train a TTS model for the Belarusian language.

Everything you need to know about the framework and how to use it to train and generate speech is written in the [documentation](https://tts.readthedocs.io/en/latest/index.html). Here I will only describe the steps I took to train the model.
## Installation
If you are only interested in [synthesizing speech](https://tts.readthedocs.io/en/latest/inference.html) with the released 🐸TTS models, installing from PyPI is the easiest option.

```bash
pip install TTS
```

If you plan to code or train models, clone 🐸TTS and install it locally.

```bash
git clone https://github.com/coqui-ai/TTS
pip install -e .[all,dev,notebooks]  # Select the relevant extras
```
You could also install this fork of 🐸TTS from GitHub:
```bash
git clone https://github.com/jhlfrfufyfn/diplom-bel-tts
pip install -e .[all,dev,notebooks]  # Select the relevant extras
```


If you are on Ubuntu (Debian), you can also run following commands for installation.

```bash
$ make system-deps  # intended to be used on Ubuntu (Debian). Let us know if you have a different OS.
$ make install
```

If you are on Windows, 👑@GuyPaddock wrote installation instructions [here](https://stackoverflow.com/questions/66726331/how-can-i-run-mozilla-tts-coqui-tts-training-with-cuda-on-a-windows-system).

## Training
To train a model, you need to:
### 1. Prepare a dataset
In this project I use [CommonVoice](https://commonvoice.mozilla.org/en/datasets) dataset. Download the latest Belarusian dataset.

Downloaded dataset contains some .tsv files with metadata and a folder with audio files. 

Now you need to choose a speaker, who recorded enough data to train the model (at least 10 hours). For this purpose I wrote a script in ```/notebooks/jhlfrfufyfn/choose_speaker.ipynb```.
Is is a bit messy there, but you will surely get the idea.

After you have chosen a speaker, I recommend manually listen to some of his/her recordings to find bad quality ones and remove them from the dataset. 

There are some good notebooks for dataset analysis in ```/notebooks/dataset_analysis``` folder. You can use them to find bad quality recordings, check the distribution of the data, etc, tune the audio parameters for the speaker's voice, etc.

#### Phonemizing the dataset
It is a really good idea to phonemize the dataset before training. It will help the model to learn better because it will not have to learn the pronunciation of the words, which can be very different from the spelling.

To phonemize the dataset I used a phomenizer that was kindly given to me by [BNKorpus](https://bnkorpus.info/fanetyka.html) project. It is written in Java, so I wrapped it in Spring, deployed it on my server, and used it via API (```POST fonemizer.nikuchin.fun/processText```). It takes some text as an input, converts it into IPA format, than it maps IPA multisymbol phonemes to single symbols and returns the result as a response.

Keep in mind, that if you phonemized the training data, you would also need to phonemize the inference data.
### 2. Decide what model to use
There are several models available in the framework.
I used GlowTTS for text-to-spec model and HifiGAN for vocoder because they take the least time to train and give good results.

### 3. Generate scale_stats file
It is a good idea to generate scale_stats file before training. It will help the model to learn better. To generate it, you need to run the following command:
```bash
python TTS/bin/compute_statistics.py --config_path TTS/tts/configs/config.json --out_path scale_stats.npy
```
or something like that. You can find more information in the documentation.

### 4. Create a config
Default config files are located in ```TTS/tts/configs```. You can use them as a template for your own config. You can find parameters that I overwrote during training in training files, located in ```recipes/jhlfrfufyfn/```.

### 5. Train the model

### 6. Monitor the training progress
During training, you can monitor the progress of the model by running the following command:
```
tensorboard --logdir PATH_TO_LOGS
```
This will start a TensorBoard server, which you can access in your web browser at http://localhost:6006. TensorBoard provides visualizations and metrics to help you analyze the training process.

### 7. Inference
After the model is trained, you can synthesize speech with either the command line or with Python, (see ```/recipes/jhlfrfufyfn/generate.py``` for the inspiration, note that it is not connected to the phonemizer and doesn't work for my last trained model).
