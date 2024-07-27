import argparse
from audio_processor import Speech2Text



if __name__ == "__main__":
    parser = argparse.ArgumentParser("python main.py")
    parser.add_argument("--f", "--folder", dest='FOLDER', help="Folder to analyze", type=str, default="video")
    args = parser.parse_args()
    
    transcriber = Speech2Text(model_path="vosk-model-es-0.42")
    import pprint
    transcription = transcriber.transcribe_folder(foldername=args.FOLDER)
    pprint.pprint(transcription)
    pass