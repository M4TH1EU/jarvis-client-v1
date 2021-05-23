import os
import tempfile
import wave

import pyaudio

filename = tempfile.gettempdir() + '\\recorded_song.wav'


def record(record_for_seconds):
    """
    Record the mic for a given amount of seconds

    :param record_for_seconds: the amount of second to record
    """
    # Record in chunks of 1024 samples
    chunk = 1024

    # 16 bits per sample
    sample_format = pyaudio.paInt16
    chanels = 2

    # Record at 44400 samples per second
    smpl_rt = 44400
    seconds = record_for_seconds

    # Delete the existing file
    if os.path.exists(filename):
        os.remove(filename)

    # Create an interface to PortAudio
    pa = pyaudio.PyAudio()

    stream = pa.open(format=sample_format, channels=chanels,
                     rate=smpl_rt, input=True,
                     frames_per_buffer=chunk)

    print('Recording...')

    # Initialize array taht be used for storing frames
    frames = []

    # Store data in chunks for 8 seconds
    for i in range(0, int(smpl_rt / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate - PortAudio interface
    pa.terminate()

    print('Done.')

    # Save the recorded data in a .wav format
    sf = wave.open(filename, 'wb')
    sf.setnchannels(chanels)
    sf.setsampwidth(pa.get_sample_size(sample_format))
    sf.setframerate(smpl_rt)
    sf.writeframes(b''.join(frames))
    sf.close()
