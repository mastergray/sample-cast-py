# Dependencies:
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio
import asyncio
import threading
import wave


class SampleCastAudio:

    """Implements how to handle audio for playback"""

    ###############
    # CONSTRUCTOR #
    ###############

    def __init__(self, audioFilePath):
        try:
            # Set file path:
            self.audioFilePath = audioFilePath
              
            # Initialze and set audio:
            self.audio = AudioSegment.from_file(audioFilePath)  # Load audio
            self.audio = self.audio.set_sample_width(2) # Force sample width to "2" since simpeaudio seems to only support 16-bit PCM

            # To track active playback instance:
            self.playback = None 
        
        except Exception as err:
             raise ValueError(f"Error loading audio file '{audioFilePath}': {err}")


    ####################
    # Instance Methods #
    ####################

    def play(self, start=0, end=None, gain=0, callback=None):
        """Plays stored audio"""
        
        # Always ensure audio is stopped before trying to play:
        self.stop()

        # Set and convert range of play duration
        start_ms = start * 1000 
        end_ms = len(self.audio) if end is None else end * 1000

        # Adjust volume with gain if given:
        adjustedAudio = self.audio.apply_gain(gain)

        # Slice the audio segment
        audioDuration = adjustedAudio[start_ms:end_ms]

        # Start playback:
        self.playback = _play_with_simpleaudio(audioDuration)

        # Define the function that will be executed in a new thread
        def play_with_callback():
            self.playback.wait_done()  # Wait until playback is finished (this will block the thread)
            if callback:
                callback()

        # Create and start a new thread for playback 
        self.thread = threading.Thread(target=play_with_callback)
        self.thread.start()

    def stop(self, callback=None):
        """Stops stored audio"""
        if self.playback is not None:
            self.playback.stop()
            self.playback = None
            if callback:
                callback()

    #################
    # Magic Methods #
    #################

    def __repr__(self):
        """Returns info about instance"""
        status = "Stopped" if self.playback is None else "Is Playing"
        return str({"audioFile":self.audioFilePath,"status":status})
    
    ##################
    # Static Methods #
    ##################

    @staticmethod
    def getAudioInfo(audioPath):
        """Extract audio properties from a WAV file using wave."""
        with wave.open(audioPath, "rb") as wav_file:
            return {
                "channels": wav_file.getnchannels(),
                "sample_width": wav_file.getsampwidth(),
                "frame_rate": wav_file.getframerate(),
                "duration": wav_file.getnframes() / wav_file.getframerate(),
            }


    # Example usage
if __name__ == "__main__":

    import time

    filename = "/home/mastergray/Desktop/select-breaks/JBK_160_Brk_Full_Drums_PraySista.wav"
    audio = SampleCastAudio(filename)
    audio.play(gain=5)
    time.sleep(1)
    audio.stop()
    audio.play(start=.25, gain=-1)
    print("done.")    