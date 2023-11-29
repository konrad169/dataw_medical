import base64
import os
import os
os.path.abspath(os.getcwd())
import streamlit as st

from converter_utils import extract_docx, pdf_to_base64_images
from form_utils import dict_messages_button, get_question_chat
from open_ai_utils import image_input_to_chat, get_text_to_chat
from output_files import create_pdf_with_logo_and_text

path = os.path.dirname(__file__)
logo_name = path + "/assets/logo_datawizard.png"
path=str(os.path.abspath(os.getcwd()))+"/"
# Trick to preserve the state of your widgets across pages
for k, v in st.session_state.items():
    st.session_state[k] = v

def download_pdf(text,pdf_path):
    create_pdf_with_logo_and_text(logo_path=f"{path}assets/DataWizard.png",text=text,output_path=pdf_path)
    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    st.download_button(
        label="Scarica PDF",
        data=pdf_bytes,
        file_name="output.pdf",
        mime='application/pdf',
        on_click=handle_download)
# def select_and_confirm(key=int):
#     # Inizializza lo stato della sessione se non esiste
#     if "selected_value" not in st.session_state:
#         st.session_state["selected_value"] = None
#
#     # Mostra la select box solo se non è stato ancora selezionato un valore
#     if st.session_state["selected_value"] is None:
#         place_h=st.empty()
#         #button_h=st.empty()
#         options = ["Opzione 1", "Opzione 2", "Opzione 3",  "Risposta prompt"]
#         selected_option = place_h.selectbox("Scegli un'opzione", options,key=key,index=None, placeholder="Scegli una risposta...")
#         st.session_state.created_selection=True
#
#         # Se l'utente ha selezionato un'opzione, mostra il bottone di conferma
#         #if st.button("Conferma",key=key_but):
#         st.session_state["selected_value"] = selected_option
#
#             #s.empty()
#         st.session_state.created_selection=None
#         if selected_option:
#             place_h.empty()
#     # Se è stato selezionato un valore, ritorna il valore e nasconde la select box e il bottone
#     if st.session_state["selected_value"] is not None:
#         to_return=st.session_state.selected_value
#         st.session_state.selected_value=None
#         return to_return
def select_and_confirm():
    if (st.session_state.show_messages):
        options =get_question_chat(genre)
        selected_option = st.selectbox("Scegli un'opzione", options, key="selected_value")
        confirmed = st.button("Conferma selezione", on_click=handle_confirm, args=[selected_option])
        if confirmed:
            #show_chat_messages()
            # st.session_state.messages.append({"role": "assistant", "content": confirmed})
            with st.spinner("Stiamo analizzando la tua richiesta. Attendere prego..."):
                response = get_text_to_chat(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response})
            show_chat_messages()
            return response
    else:
        show_chat_messages()
        if st.session_state.selected_value == "Domanda Prompt":
            chat = st.empty()
            if prompt := chat.chat_input("Come desideri approfondire?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                chat.empty()
                with st.chat_message("user"):
                    st.markdown(prompt, unsafe_allow_html=True)
                with st.spinner('Stiamo analizzando la tua richiesta. Attendere prego..'):
                    response = get_text_to_chat(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response, unsafe_allow_html=True)
                st.session_state.show_messages = True
                select_and_confirm()
        else:
            if not st.session_state.closed_cycle:
                final_message = "Mi fai un riassunto della conversazione e in cui mi spieghi tutto quello che mi hai detto, soffermandoti sui punti salienti e dettagliando le soluzioni che mi hai proposto. Voglio questo riassunto in italiano e fatto per fare un pdf."
                st.session_state.messages.append({"role": "user", "content": final_message})
                # with st.chat_message("user"):
                #     st.markdown(final_message, unsafe_allow_html=True)

                with st.spinner('Stiamo preparando un riassunto della conversazione. Attendere la comparsa del bottone di Download..'):
                    response = get_text_to_chat(st.session_state.messages)

                with st.chat_message("assistant"):
                    st.markdown(response, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response})
                download_pdf(response,f"{path}temp/output_generated.pdf")
            else:
                ##TODO:POSSIAMO SCOMMENTARLO
                #st.session_state.messages.append({"role":"system","content": "Conversazione conclusa"})
                #show_chat_messages()
                response=""###DEVO FINIRE AL DOWNLOAD
            return response


def show_chat_messages():
    for message in st.session_state.messages:
        if any(el.get('type') == 'image_url' for el in message.get('content') if
               isinstance(message.get('content'), list)):
            continue
        else:
            if message["content"].startswith("Mi fai un riassunto della conversazione e in cui mi spieghi tutto"):
                continue
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"], unsafe_allow_html=True)


def handle_confirm(content):
    if (st.session_state.selected_value == "Domanda Prompt"):
        st.session_state.show_messages = False
    elif (st.session_state.selected_value == "Termina conversazione"):
        st.session_state.show_messages = False
    else:
        st.session_state.messages.append({"role": "user", "content": content})
        st.session_state.show_messages = True

def handle_download():
    st.session_state.closed_cycle=True

def handle_submit():
    st.session_state.show_messages = True


st.set_page_config(
    page_title="Medical Analysis",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
  <style>
      .css-zck4sz p {
        font-weight: bold;
        font-size: 18px;
      }
  </style>""", unsafe_allow_html=True)

st.sidebar.image(path + "/assets/logo_datawizard.png")

st.markdown("""
  <style>
      ul[class="css-j7qwjs e1fqkh3o7"]{
        position: relative;
        padding-top: 2rem;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
      }
      .css-17lntkn {
        font-weight: bold;
        font-size: 18px;
        color: grey;
      }
      .css-pkbazv {
        font-weight: bold;
        font-size: 18px;
      }
  </style>""", unsafe_allow_html=True)
st.markdown("""
              <style>
              #MainMenu {visibility: visible;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>
              """, unsafe_allow_html=True)
st.markdown(
    """<style>
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)
st.markdown(
    """<style>
div[class*="stNumberInput"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)
st.markdown(
    """<style>
div[class*="stTextInput"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 18px;
}
    </style>
    """, unsafe_allow_html=True)

st.subheader(":black_nib: **{}**".format('Caricamento file'))

if "disabled_options" not in st.session_state:
    st.session_state.disabled_options = False
    st.session_state.disabled_count = 0
if "selected_value" not in st.session_state:
    st.session_state.selected_value = None
if "decided_response" not in st.session_state:
    st.session_state.decided_response = None
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "show_messages" not in st.session_state:
    st.session_state["show_messages"] = True
if "closed_cycle" not in st.session_state:
    st.session_state.closed_cycle=None
if 'already_asked' not in st.session_state:
    st.session_state.already_asked = False

genre = st.sidebar.radio(
    "Tipologia Documento",
    ["Lettura Analisi", "Spiegazione Diagnosi", "Prescrizioni"],
    index=None,
    help="Seleziona un'opzione",
    key="radio_options",
    # disabled=st.session_state.disabled_options,
)
if genre:
    st.sidebar.write("Selezionato:", genre)
else:
    st.sidebar.warning("Seleziona una tipologia documento")

if not st.session_state.disabled_options:
    st.session_state.disabled_options = True

image_file = st.sidebar.file_uploader("Upload a medical document (jpg, png, jpeg, pdf or docx)",
                                      type=['jpg', 'png', 'jpeg', 'pdf', 'docx'])

base64_list, base64_image, text_doc = '', '', ''

if image_file:
    extension = image_file.name.split(".")[1]
    if extension in ['pdf', 'docx']:
        with open(f'{path}temp/{image_file.name}', mode='wb') as file:
            file.write(image_file.getvalue())
    if not st.session_state.already_asked:
        match extension:
            case 'pdf':
                base64_list = pdf_to_base64_images(f'{path}temp/{image_file.name}')
            case 'docx', 'doc':
                text_doc = extract_docx(file_path=f'{path}temp/{image_file.name}')
            case "jpg" | "jpeg" | "png":
                # medical_image = Image.open(image_file)
                image_content = image_file.read()
                base64_image = base64.b64encode(image_content).decode('utf-8')
            case _:
                st.error("Formato file non valido.. Riprovare il caricamento")

    if extension in ['docx', 'png', 'pdf'] and not st.session_state.already_asked:
        message_text = dict_messages_button.get(genre)
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-4-1106-preview"

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        # Display chat messages from history on app rerun
        ##TODO:SCOMMENTARE SE BISOGNA REINSERIRE IL PRIMO MESSAGGIO
        # for message in st.session_state.messages:
        #    with st.chat_message(message["role"]):
        #        st.markdown(message["content"])
        ##TODO:SCOMMENTARE SE BISOGNA REINSERIRE IL PRIMO MESSAGGIO
        # with st.chat_message("user"):
        #    st.markdown(message_text)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            if extension == 'docx':
                # response = get_completion(text_doc, client)
                st.session_state.messages.append({"role": "user", "content": text_doc})
                chat_list = st.session_state.messages
                with st.spinner("Stiamo analizzando la tua richiesta. Attendere prego.."):
                    response = get_text_to_chat(message_hist=chat_list)
                    text_doc = ''
                    st.session_state.already_asked = True
            else:
                message_placeholder = st.empty()
                if base64_image:
                    with st.spinner("Stiamo analizzando la tua richiesta. Attendere prego.."):
                        response, content = image_input_to_chat(message_text=message_text, file_ext=extension,
                                                                base_img=base64_image)
                        st.session_state.already_asked = True
                elif base64_list:
                    with st.spinner("Stiamo analizzando la tua richiesta. Attendere prego.."):
                        response, content = image_input_to_chat(message_text=message_text, base_img=base64_list)

                        st.session_state.already_asked = True
            st.session_state.messages.append({"role": "user", "content": content})
            full_response += response
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    response = select_and_confirm()

    # if response:
    #     full_response += response  # .choices[0].delta.get("content", "")
    #     message_placeholder.markdown(full_response + "▌")
    #     message_placeholder.markdown(full_response)
    #     st.session_state.messages.append({"role": "system", "content": full_response})
    #     show_chat_messages()
