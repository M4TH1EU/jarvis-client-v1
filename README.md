<img src="https://i.imgur.com/uuWWP39.png" />

# jarvis-client

Jarvis is a simple IA for home automation with voice commands written in Python. Mainly based on HomeAssistant API, the
more devices you have on HomeAssistant, the more you will be able to teach to Jarvis.

**This is only the client-side of Jarvis, you can download the server [here](https://github.com/M4TH1EU/jarvis-server)
.**

## Languages

It only supports **french** for now, but with some changes you should be able to use english or another language.

## Compatiblity

The client should too **but**, the client manage the STT & TTS part and I did not found any cool voice on Linux *(for
french voices at least)* I only found out that Windows is the only one that has good french voices *(Mathieu from IVONA2
p.ex)*.

The server can run on anything that runs Python 3+  

## Installation

If not already installed, you will need Python 3.9, you can install it with theses commands.
```shell
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3.9 python3.9-dev python3.9-distutils
```

### Larynx TTS
Pre-built Debian packages are [available for download](https://github.com/rhasspy/larynx/releases/tag/v0.4.0).

There are three different kinds of packages, so you can install exactly what you want and no more:

* `larynx-tts_<VERSION>_<ARCH>.deb`
    * Base Larynx code and dependencies (always required)
    * `ARCH` is one of `amd64` (most desktops, laptops), `armhf` (32-bit Raspberry Pi), `arm64` (64-bit Raspberry Pi)
* `larynx-tts-lang-<LANG>_<VERSION>_all.deb`
    * Language-specific data files (at least one required)
    * See [above](#docker-installation) for a list of languages
* `larynx-tts-voice-<VOICE>_<VERSION>_all.deb`
    * Voice-specific model files (at least one required)
    * See [samples](#samples) to decide which voice(s) to choose
    
As an example, let's say you want to use the "harvard-glow_tts" voice for English on an `amd64` laptop for Larynx version 0.4.0.
You would need to download these files:

1. [`larynx-tts_0.4.0_amd64.deb`](https://github.com/rhasspy/larynx/releases/download/v0.4.0/larynx-tts_0.4.0_amd64.deb)
2. [`larynx-tts-lang-en-us_0.4.0_all.deb`](https://github.com/rhasspy/larynx/releases/download/v0.4.0/larynx-tts-lang-en-us_0.4.0_all.deb)
3. [`larynx-tts-voice-en-us-harvard-glow-tts_0.4.0_all.deb`](https://github.com/rhasspy/larynx/releases/download/v0.4.0/larynx-tts-voice-en-us-harvard-glow-tts_0.4.0_all.deb)

Once downloaded, you can install the packages all at once with:

```sh
sudo apt install \
  ./larynx-tts_0.4.0_amd64.deb \
  ./larynx-tts-lang-en-us_0.4.0_all.deb \
  ./larynx-tts-voice-en-us-harvard-glow-tts_0.4.0_all.deb \
  sox
```