# Add the path to the parent directory to sys.path:
import sys
import os
modules_dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(modules_dir_path)

# Dependenceis:
from flask import Flask, request, jsonify, Response             # HTTP Server Framework
from flask_cors import CORS                                     # For setting CORS
from sample_cast_audio_manager import SampleCastAudioManager    # For managing audio with
import signal                                                   # For shutting down audio manager when server is stopped

class SampleCastServer:
    
    """Implements server for handling request to play samples with"""

    ###############
    # CONSTRCUTOR #
    ###############

    def __init__(self):

         # Create an instance of the Flask app as a property of the class
        self.app = Flask(__name__)                        
        
        # Create an instance of audio manager to manage audio playback with:
        self.audioManager = SampleCastAudioManager()

        # TODO: Dont accept CORS from EVERYONE:
        CORS(self.app)
        
        # Initalizes routes for Flask server: 
        self.initRoutes()                               
    
    ####################
    # Instance Methods #
    ####################

    def initRoutes(self):

        """Initalizes routes for Flask server"""

        # GET :: / 
        @self.app.route('/', methods=["GET"])
        def get_index():
            return "Yo. Things are Running. Probably. LOLLERZ!!!!1111" 
        
        # POST :: /play
        @self.app.route("/play", methods=["POST"])
        def play_audio():

            """Plays an audio file for given start and stop time"""

            try:

                # Get the JSON data from the request body
                body = request.get_json()
                audioPath = body.get("audioPath")
                start = body.get("start", 0)
                end = body.get("end", None)

                # Convert values:
                start = float(start)
                end = float(end) if end is not None else end

                # Show message:
                print(f"Playing {audioPath}...")
     
                # Play audio:
                self.audioManager.play(audioPath, start, end)

                # Send success message:
                return str(f"Playing {audioPath}"), 200

            except Exception as err:

                print(f"Could Not Play Audio: {err}")
                return str(err), 500
            

        # POST :: /stop
        @self.app.route("/stop", methods=["POST"])
        def stop_audio():

            """Plays an audio file for given start and stop time"""

            try:
                # Get the JSON data from the request body
                body = request.get_json()
                audioPath = body.get("audioPath")

                # Show message:
                print(f"Stopping {audioPath}...")
     
                # Stop audio:
                self.audioManager.stop(audioPath)

                # Send success message:
                return str(f"Stopped {audioPath}"), 200

            except Exception as err:

                print(f"Could Not Stop Audio: {err}")
                return str(err), 500


    def start(self, host="127.0.0.1", port=5000):
        """Starts server"""
        # Set up signal handlers to catch SIGINT (CTRL+C) and SIGTERM
        signal.signal(signal.SIGINT, self.audioManager.shutdown)  # CTRL+C (SIGINT)
        signal.signal(signal.SIGTERM, self.audioManager.shutdown)  # SIGTERM (for other shutdown scenarios)
        self.app.run(host=host, port=port, debug=True)  # Start Server
       
# Example usage
if __name__ == "__main__":

    # Initalize server:
    server = SampleCastServer()

    # Start Server
    server.start(port=5069)

