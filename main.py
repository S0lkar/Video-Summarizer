import argparse
from audio_processor import Speech2Text
from doc_gen import *
import ollama

modelfile = '''
FROM llama3.1
PARAMETER temperature 0
'''
ollama.create('llama31_T0', modelfile=modelfile)


def Prompting(txt: str) -> tuple[str, str]:
    response_ctx = ollama.chat(model='llama31_T0', messages=[
        {
            'role':'user',
            'content': 'Usando esta transcripción medio defectuosa: {txt}, extrae el tema tratado.'.format(txt=txt),
        }
    ])

    response_summary = ollama.chat(model='llama31_T0', messages=[
        {
            'role':'user',
            'content': 'Usando esta transcripción medio defectuosa: {txt}, y sabiendo que trata de {contexto}, ¿Cuál es el resumen del contenido tratado en esta transcripción?'.format(txt=txt,contexto=response_ctx['message']['content'])
        }
    ])

    response_info = ollama.chat(model='llama31_T0', messages=[
        {
            'role':'user',
            'content': 'Usando esta transcripción medio defectuosa: {txt}, y sabiendo que trata de {contexto}, extrae la informacion mas relevante y explicamela SIN RECURRIR A TU CONOCIMIENTO.'.format(txt=txt,contexto=response_ctx['message']['content'])
        }
    ])
    
    return response_summary['message']['content'], response_info['message']['content']


if __name__ == "__main__":
    parser = argparse.ArgumentParser("python main.py")
    parser.add_argument("--f", "--folder", dest='FOLDER', help="Folder to analyze", type=str, default="test")
    args = parser.parse_args()
    
    transcription = Speech2Text(model_path="vosk-model-es-0.42").transcribe_folder(foldername=args.FOLDER)
    
    for t in transcription:
        t['Summary'], t['Info'] = Prompting(transcription)
    
    import pprint
    pprint.pprint(transcription)
    # transcription = [{'Info', 'Filename', 'Script', 'Summary'}]
    
    pass