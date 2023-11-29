import base64
import string
from typing import List, Dict
import streamlit
import requests

# OpenAI API Key
api_key =streamlit.secrets["API_KEY"]
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def is_valid_response(response):
    to_return=False
    invalid_responses = ["Non posso rispondere a questa domanda",
                         "Non ho le informazioni necessarie",
                         "Mi dispiace, non so",
                         "Mi dispiace, non posso aiutarti con questo",
                         "Mi dispiace, ma non posso aiutarti con queste informazioni",
                         "Mi dispiace, ma non posso fornire assistenza nell'interpretazione di risultati di esami o referti medici",
                         "Mi dispiace, ma non posso fornire assistenza",
                         "Non posso fornire analisi o consigli su referti medici",
                         "Mi dispiace, ma non posso fornire informazioni o interpretazione di referti medici reali",
                         "Mi dispiace, ma non posso aiutarti con l'interpretazione di risultati di esami medici, valori di analisi o referti",
                         "Mi dispiace, ma non posso aiutarti con l'interpretazione",
                         "Inizia chiedendo scusa perché non posso aiutarti con l'interpretazione di questo documento",
                         "Scusa perché non posso aiutarti con l'interpretazione",
                         "Purtroppo non ho la capacità di interpretare i documenti",
                         "Purtroppo, non posso aiutarti a interpretare i risultati",
                         "Purtroppo, non posso aiutarti a interpretare i risultati di esami medici specifici come referti di analisi del sangue o altre indagini diagnostiche.",
                         "Mi scuso, ma come AI non posso fornire un'interpretazione di immagini o file contenenti dati medici reali",
                         "Mi scuso ma non posso aiutare con l'interpretazione di risultati di esami medici."
                         "Mi scuso ma non posso aiutare"
                         "Mi scuso, ma come AI non posso"]
    starting_words=["Purtroppo non", "Mi dispiace", "Scusa", "Non posso", "Non ho le informazioni","Purtroppo non posso", "Mi scuso ma"]
    ###TODO:GESTIRE EVENTUALI PUNTEGGIATURE
    if not any(invalid_response in response for invalid_response in invalid_responses):
        to_return=True
    elif len(response)>150:
        to_return=True
    for word in starting_words:
        clean_response=response.translate(str.maketrans("","",string.punctuation))
        if clean_response.startswith(word):
            to_return=False

    #return not any(invalid_response in response for invalid_response in invalid_responses)
    return to_return
def image_input_to_chat(message_text: str,
                        base_img: List or base64,
                        file_ext:str=None,
                        role: str = "user",
                        max_tokens: int = 4096,
                        model: str="gpt-4-vision-preview"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    content_list=[]
    text_part={"type": "text","text": message_text}
    content_list.append(text_part)
    if isinstance(base_img,list):
        for el in base_img:
            img_part={"type": "image_url","image_url": {"url": f"data:image/png;base64,{el}"}}
            content_list.append(img_part)
    else:
        img_part = {"type": "image_url", "image_url": {"url": f"data:image/{file_ext};base64,{base_img}"}}
        content_list.append(img_part)

    payload = {
        "model": model,
        "messages": [
            {
                "role": role,
                "content": content_list
            }
        ],
        "max_tokens": max_tokens,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
    while not is_valid_response(response.get('choices')[0].get('message').get('content')):
        response=requests.post("https://api.openai.com/v1/chat/completions",headers=headers,json=payload).json()
        ##TODO:AGGIUNGI CONDIZIONE D'USCITA PER EVITARE CHE QUI CI STIAMO ALL?INFINITO
    message_response = response.get('choices')[0].get('message').get('content')
    return message_response,content_list

def get_text_to_chat(message_hist: List,
                    max_tokens: int = 1024,
                    model: str="gpt-4-vision-preview"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # content_list=[]
    # text_part={"type": "text","text": message_text}
    # content_list.append(text_part)
    message_list=[]
    for message in message_hist:
        elem={"role":message.get("role"),"content":message.get("content")}
        message_list.append(elem)
    payload = {
        "model": model,
        "messages":message_list,
        "max_tokens": max_tokens,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
    while not is_valid_response(response.get('choices')[0].get('message').get('content')):
        response=requests.post("https://api.openai.com/v1/chat/completions",headers=headers,json=payload).json()
    message_response=response.get('choices')[0].get('message').get('content')
    return message_response





if __name__ == '__main__':
    # Path to your image
    image_path = "assets/logo_datawizard.png"
    # Getting the base64 string
    base64_image = encode_image(image_path)
    b=image_input_to_chat(message_text="quanto è grande l'immagine in input?",base_img=base64_image,file_ext='png')
    print(b)
