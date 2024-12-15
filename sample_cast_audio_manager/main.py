# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependencies:
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import asyncio
from sample_cast_audio import SampleCastAudio
import threading                                      

class SampleCastAudioManager:

    """Implements how audio samples are stored and played by the server"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self):
        self.audioStore = {}                     # Store audio instances by an pathname
   
    ####################
    # Instance Methods #
    ####################

    def register(self, filename):
        """Adds instance of SampleCastAudio by filename to audio store"""
        self.audioStore[filename] = SampleCastAudio(filename)

    def unregister(self, filename):
        """Remove instance of SampleCastAudio by filename from audio store"""
        if filename in self.audioStore:
            self.terminateAudioThread(self.audioStore[filename])
            try:
                del self.audioStore[filename]
            except KeyError:
                print(f"Audio for '{filename}' is already removed!")

    def play(self, filename, start=0, end=None):
        """Plays instance of SampleCastAudio by filename"""
        if filename not in self.audioStore:
            self.register(filename)
        self.audioStore[filename].play(start, end)

    def stop(self, filename):
        """Stops instance of SampleCastAudio by filename"""
        if filename in self.audioStore:
            self.audioStore[filename].stop()

    def terminateAudioThread(self, audio):
        audio.stop()
        if audio.thread is not None and audio.thread.is_alive():
            if audio.thread != threading.current_thread():
                audio.thread.join()

    def shutdown(self):
        for audio in self.audioStore.values():
            self.terminateAudioThread(audio)
        print("Audio Manager Stopped")
        
# Example usage
if __name__ == "__main__":

    import time

    try:
        sample1 = "/home/mastergray/Desktop/select-breaks/JBK_160_Brk_Full_Drums_PraySista.wav"
        sample2 = "/home/mastergray/Desktop/select-breaks/JBK_160_Brk_Full_Drums_Yonder.wav"
        sample3 = "/home/mastergray/Desktop/select-breaks/JBK_162_Brk_Full_Drums_FriedHard.wav"
        audioManager = SampleCastAudioManager()
        audioManager.play(sample2, 0)
        time.sleep(1.25)
        audioManager.stop(sample2)
        time.sleep(1)
        audioManager.play(sample2, 0, .75)
        time.sleep(1)
        audioManager.play(sample2, 0, .75)
        time.sleep(1)
        audioManager.play(sample2, 0, -.05)
        time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        audioManager.shutdown()



