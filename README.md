# hewe-nlp
## Installing Ollama
This repository uses Ollama to perform the NLP operations. To run your own local model, install ollama from [Github](https://github.com/ollama/ollama) and download the Gemma3 model. To run and chat with Gemma 3:

ollama run gemma3

## Text extraction
We use uv as the package manager. You can create a virtual environment using :

```bash
   ollama run gemma3
```
 and activate using 
 ```bash
source .venv/bin/activate
```
 on Linux/Mac
or
```bash
.\.venv\Scripts\activate 
```
on Windows.

To install the required dependencies, run the following command:
```bash
uv sync
```
Once the dependencies are installed, you can run the text extraction using the following command.
```bash
python main.py
```
