
# :::::::::::::: Dependencies :::::::::::::::::

import datetime, glob, json, os, subprocess, vosk

# Subprocess -> It is needed to use FFmpeg since it is the native tool of vosk. We need to sample the audio from
# audio sources such as .mp3, .wav, .mp4, .mkv, ... and FFmpeg does so in a compatible format (s16le).
# Datetime ---> For debugging pourposes
# Vosk -> it is the most relevant open source project to convert speech into text. The quality may not always be
# on point, it depends on the language and model used. I did all the testing process using spanish language, with
# the model 'vosk-model-es-0.42' (the smaller one's quality is way too inferior). By just downloading and 
# defining the route to another model, one can use this script for other languages supported by vosk. 

vosk.SetLogLevel(-1) # Disables LOG output.

class Speech2Text():
    def __init__(self, model: str, sample_rate: int = 16000, chunk_size: int = 5000, verbose : bool = True):
        '''
            This class offers methods based on Vosk that allow to read audio files to then return their scripts.

            Parameters
            ------------------
            model_path -> path (absolute or relative) to the vosk model used to make the transcription.
            sample_rate -> measure (Hz) used to sample audio sources.
            chunk_size -> approximate length in time for each chunk. Since the function does return the whole transcription
            in a list, the chunk_size does not really matter from a logical perspective. The quality and execution time 
            seem roughly the same with the few variations that I tried, I would not spend much time fine-tunning this parameter.
            verbose -> will print some useful information (such as execution time, current process...)
        '''
        self.model = vosk.Model(model)
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.verbose = verbose

    def transcribe_file(self, filename : str) -> list[str]:
        '''
            Takes the filename of a file which contains audio (mkv, mp4, mp3, wav...) and returns the transcription,
            segmented in different chunks.
            
            Parameters
            -------------
            filename -> path to the file that will be analyzed by the function.
            self.verbose -> If set to true, will print the execution time by the end of the analysis.
        '''
        rec = vosk.KaldiRecognizer(self.model, self.sample_rate)
        rec.SetWords(True)
        transcription = []

        ffmpeg_command = ["ffmpeg", "-nostdin", "-loglevel", "quiet", "-i", filename, "-ar", str(self.sample_rate), "-ac", "1", "-f", "s16le", "-"]

        with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, shell=True) as process:
            start_time = datetime.datetime.now()
            
            while True:
                data = process.stdout.read(self.chunk_size)
                if len(data) == 0: # There is no more audio to process
                    break
                
                if rec.AcceptWaveform(data):
                    transcription.append(json.loads(rec.Result())['text']) # Process the current chunk
            transcription.append(json.loads(rec.FinalResult())['text']) # Final part of the audio
        
        if self.verbose:
            print(f"For audio in {filename}, time spent: {datetime.datetime.now() - start_time}.")
        return transcription
    
    def transcribe_folder(self, foldername : str, ext : list[str] | None = None, reach_subfolders : bool = False) -> list[dict]:
        '''
            This function performs the transcription of all audio sources found within the given folder path.
            Returns a list of dicts following this structure:
            {
                "Filename": filename of the audiofile,
                "Script": [chunk1, chunk2, ...] # list[str] containing the transcript of the audiofile.
            }
            
            Parameters
            -------------
            foldername -> path to the folder to analyze.
            
            ext -> extension of files to transcribe. 'mp3' would make the transcriber to only walk thorugh .mp3 files, ignoring all else.
            If a list is given, it will transcribe all files matching those extensions.
            If nothing is given, then all files within the folder will be transcribed.
            It does not matter if an extension is declared here but no matching file is found.
            
            reach_subfolders -> if set to True, will reach all audio files which match the extension both in the root and sub folders.
        '''
        if not ext:
            ext = ['*']
            
        L = []
        for extension in ext:
            if reach_subfolders:
                Lista_ficheros = [y for x in os.walk(foldername) for y in glob.glob(os.path.join(x[0], '*.' + extension))]
            else:
                Lista_ficheros = [f for f in glob.glob(foldername + "/*." + extension)]
                
            for i in Lista_ficheros:
                if self.verbose:
                    print(i)
                L.append({'Filename': i, 'Script': self.transcribe_file(i)})
            
        return L



# :::::::::::::: Example of usage :::::::::::::::::
if __name__ == '__main__':
    import pprint

    extension = ['mkv']
    transcriber = Speech2Text(model_path="vosk-model-es-0.42")
    transcription = transcriber.transcribe_folder(foldername=r"test", ext=extension, reach_subfolders=True)
    pprint.pprint(transcription[0])

    print("::::::::::::::::::::::::::::::::::::::::::::::::::")

    transcription = transcriber.transcribe_file(filename=r"test/video.mkv")
    pprint.pprint(transcription)
    
