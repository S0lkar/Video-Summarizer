import argparse
from audio_processor import *
from doc_gen import *
import ollama

modelfile = '''
FROM llama3.1
PARAMETER temperature 0
'''
ollama.create('llama31_T0', modelfile=modelfile)

Prompts = {
    'ES': [
        'Usando esta transcripción inexacta: "{txt}", extrae el tema tratado.',
        'Usando esta transcripción inexacta: "{txt}", y sabiendo que trata de {contexto}, ¿Cuál es el resumen del contenido tratado en esta transcripción?',
        'Usando esta transcripción inexacta: "{txt}", y sabiendo que trata de {contexto}, extrae la informacion mas relevante y explicamela SIN RECURRIR A TU CONOCIMIENTO.'
    ],
    'EN': [
        'Using this inaccurate transcription: "{txt}", extract the topic discussed.',
        'Using this inaccurate transcription: "{txt}", knowing that the context is {contexto}, what is the summary of the content covered in this transcript?',
        'Using this inaccurate transcription: "{txt}", knowing that the context is {contexto}, extract the most relevant information and explain it to me WITHOUT RESOURCING TO YOUR KNOWLEDGE.'
    ]
}


Titles = {
    'ES': [
        'Resumen de ',
        'Contenido Relevante',
        'Script original'
    ],
    'EN': [
        'Summary of ',
        'Relevant Content',
        'Original Script'
    ]
}


def Prompting(txt: str, lang : str | None = None) -> tuple[str, str]:
    if not lang:
        lang = 'ES' # Defaults to spanish
        
        
    response_ctx = ollama.chat(model='llama31_T0', messages=[{
        'role':'user',
        'content': Prompts[lang][0].format(txt=txt),
    }])

    response_summary = ollama.chat(model='llama31_T0', messages=[{
        'role':'user',
        'content': Prompts[lang][1].format(txt=txt,contexto=response_ctx['message']['content'])
    }])

    response_info = ollama.chat(model='llama31_T0', messages=[{
        'role':'user',
        'content': Prompts[lang][2].format(txt=txt,contexto=response_ctx['message']['content'])
    }])
    
    return response_summary['message']['content'], response_info['message']['content']



if __name__ == "__main__":
    parser = argparse.ArgumentParser("python main.py")
    parser.add_argument("--f", "--folder", dest='FOLDER', help="Folder to analyze", type=str, default="test")
    parser.add_argument('--es', '--expore-sub', dest='EXSUB', action=argparse.BooleanOptionalAction, help='If set, explores subfolders as well.')
    parser.add_argument("--la", "--lang", dest='LANG', help="Language used in generation (ES for Spanish, EN for english).", type=str, default="ES", choices=['ES', 'EN'])
    parser.add_argument('--e','--ext', nargs='+', dest='EXT', help='File extensions taken as audio files. Defaults to take all files within the folder.', default=['*'])
    parser.add_argument('--v', '--verbose', dest='VERB', action=argparse.BooleanOptionalAction, help='If set, prints messages according to the analysis status.')
    
    parser.add_argument("--t", "--template", dest='TEMPLATE', help="Docx template to be used", type=str, default="template.docx")
    parser.add_argument("--m", "--Vosk-model", dest='VMODEL', help="Vosk model to be used", type=str, default="vosk-model-es-0.42")
    args = parser.parse_args()
    
    
    transcription = Speech2Text(args.VMODEL, verbose=args.VERB).transcribe_folder(foldername=args.FOLDER, ext=args.EXT, reach_subfolders=args.EXSUB)
    
    for t in transcription:
        t['Summary'], t['Info'] = Prompting(transcription, args.LANG)
    
    
    docs = []
    cont = 0
    for t in transcription:
        sections = [(Titles[args.LANG][0] + t['Filename'], t['Summary']), (Titles[args.LANG][1], t['Info']), (Titles[args.LANG][2], ' '.join(t['Script']))]
        Gen_docx_template(args.TEMPLATE, 'result/result_{filename}_{cont}.docx'.format(cont=cont, filename=os.path.basename(t['Filename'])), sections)
        cont += 1
        
    
    pass