# Video-Summarizer
This is a small project with the goal to make an AI based program able to pass speech into text and summarize it, extracting all the important information needed to quickly understand what the content is about.
This project uses **only open source and local** AI tools (Vosk and Ollama). This way, personal or confidential videos can be summarized without having to upload to any website, also allowing for customization in both the output format and the arquitecture used to achieve results (prompting and used models).

## Requirements
All python modules needed and versions are listed in the **requirements.txt** file in this repository. 
However, there are three external tools that need to be downloaded and set-up.

### Vosk model

To be able to make the transcription, it is needed to download a model [from Vosk website](https://alphacephei.com/vosk/models) and unzip it. Then by using the argument '--m' you can specify the path to load the model.
It currently defaults to the large spanish model (vosk-model-es-0.42) if unzipped in the root folder of the project.

I recommend using large models instead of smaller ones if possible, from my experience these lead to much better results even if it takes longer to analyze audios.

### Ollama setup

The AI used is Llama 3.1. To set up ollama, simply go to [Ollama's website](https://ollama.com/download) and download according to your operative system. Once installed, you need to download specific models. 
To download the model used in this project, simply open the command line and type:
<table><tr><td>ollama pull llama3.1</td></tr></table>

In *main.py* it will automatically create a derivated model from this base one, setting the temperature to 0 to avoid inconsistencies. Of course, it is possible to change the base model and try different alternatives offered by ollama.


### FFmpeg setup

This tool is used to separate audio from video files, and sample at the desired frequency. After downloading the tool from [FFmpeg's website](https://ffmpeg.org/download.html), simply unzip it and add a environment variable (named Path) to the bin folder inside the unzipped file ([this article may help with more step-by-step guidance](https://es.wikihow.com/instalar-FFmpeg-en-Windows)) and it is ready to go.

## Customization

In this project I give a simple docx template, and the output format (in *doc_gen.py*) is rather simple as well. One can customize it any way they want - I would suggest using [python-docx documentation](https://python-docx.readthedocs.io/en/latest/user/quickstart.html) when working with output format, since it is very clear and straightforward.

If you only are interested in tuning smaller details, simply modify the template's styles and adjust them any way you want.

When it comes to the decisions I made for the prompting part, I made an article (in spanish) about it [in Linkedin](https://www.linkedin.com/in/carlos-gonzalez-parrado-730887229/). Long story short, be careful when asking the AI to 'produce a summary' as if the transcription is too broken it will reject the prompt.