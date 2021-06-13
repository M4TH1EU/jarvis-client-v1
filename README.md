<img src="https://i.imgur.com/uuWWP39.png" />

# jarvis-client

Jarvis is a simple IA for home automation with voice commands written in Python. Mainly based on HomeAssistant API, the
more devices you have on HomeAssistant, the more you will be able to teach to Jarvis.

**This is only the client-side of Jarvis, you can download the server [here](https://github.com/M4TH1EU/jarvis-server)
.**

### Languages

It only supports **french** for now, but with some changes you should be able to use english or another language.

### Compatiblity

The client should too **but**, the client manage the STT & TTS part and I did not found any cool voice on Linux *(for
french voices at least)* I only found out that Windows is the only one that has good french voices *(Mathieu from IVONA2
p.ex)*.

The server can run on anything that runs Python 3+  

### Installation

If not already installed, you will need Python 3.9, you can install it with theses commands.
```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3.9 python3.9-dev python3.9-distutils
```

To install the TTS engine (Larynx) you must download 3 deb files from their [GitHub](https://github.com/rhasspy/larynx/releases/latest).  
A list of the available voices and languages with samples is available [here](https://rhasspy.github.io/larynx/).  

Download theses files according to your language :
- larynx-tts-lang-xx-xx_V.V.V_all.deb *(e.g larynx-tts-lang-fr-fr_0.4.0_all.deb)*
- larynx-tts-voice-xx-xx-name-engine-tts_V.V.V_all.deb *(e.g larynx-tts-voice-fr-fr-tom-glow-tts_0.4.0_all.deb)*
- larynx-tts_V.V.V_amd64.deb **(or arm64 / armhf)** *(e.g larynx-tts_0.4.0_amd64.deb)*

Then do the following commands (replace the filenames by yours)
```shell
sudo apt install libatlas3-base libopenblas-base # install some requirements for larynx
sudo dpkg -i larynx-tts_0.4.0_amd64.deb 
sudo dpkg -i larynx-tts-lang-fr-fr_0.4.0_all.deb
sudo dpkg -i larynx-tts-voice-fr-fr-tom-glow-tts_0.4.0_all.deb
larynx "Bonjour monsieur" --voice tom-glow_tts --quality high --output-dir wavs --denoiser-strength 0.001  # try it out
```
