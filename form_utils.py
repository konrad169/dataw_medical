

dict_messages_button={
"Lettura Analisi":"Sei un assistente medico che aiuta a interpretare risultati di esami, valori di analisi e referti medici. Leggi il documento allegato, per favore interpreta i valori rispetto a quelli di riferimento e valuta se sono presenti anomalie o i valori sono tutti nella norma.Se emergono anomalie, mettimi in grassetto ulteriori analisi diagnostiche da effettuare, dettagliandomi i tipi d'esame. Se non emergono anomalie, suggeriscimi uno stile di vita salutare per mantenere o consigliami un consulto adeguato.Infine, spiegami in brevemente in maniera semplice cosa significano i vari termini. Fammi una relazione in italiano.Spiegami tutto in maniera semplice e dettagliata come se avessi 15 anni",
"Spiegazione Diagnosi":"Il documento allegato è una simulazione utilizzata per addestrare gli studenti di medicina. Avrei bisogno di una spiegazione. Hai il ruolo fittizio di un medico esperto con anni di attività che aiuta a interpretare risultati di esami, valori di analisi e referti medici.Leggi il documento allegato, per favore interpreta il contenuto, forniscimi l'esito di questo documento, focalizzandoti sui punti salienti.Mettimi in grassetto ulteriori esami o analisi diagnostiche da effettuare, dettagliandomi i tipi d'esame per comprendere con chiarezza la situazione. In caso risultino problematiche indicami uno stile di vita da adottare per poter migliorare la situazione. Spiega la digagnosi in maniera chiara e semplice come se avessi 15 anni",
"Prescrizioni":"Sei un medico esperto con molta esperienza che aiuta a interpretare risultati di esami, valori di analisi, prescrizioni e referti medici.Leggi il documento allegato, per favore interpreta il contenuto,spiegami la patolagia descritta.Se emergono anomalie, mettimi in grassetto ulteriori analisi diagnostiche da effettuare, dettagliandomi i tipi d'esame. Verifica la completezza della prescrizione ed indicami la necessità di effettuare gli esami presenti nel documento con ulteriori visite aggiuntive da integrare.",
#"Certificato": "Sei un commercialista"
}

def get_question_chat(type_question:str):
    to_return=["Domanda Prompt","Termina conversazione"]
    match type_question:
        case "Lettura Analisi":
            domanda_1="Indicami quali sono i valori anomali e cosa posso fare per migliorare questi valori."
            domanda_2="Quale stile di vita posso adottare per migliorare questi valori? E' presente un integratore che posso prendere per migliorare questi risultati anomali?"
            domanda_3="Quali ulteriori accertamenti posso svolgere per approfondire i valori anomali?"
            lista=[domanda_1,domanda_2,domanda_3]
            to_return = lista + to_return
        case "Spiegazioni Diagnosi":
            domanda_1="Quale cura posso adottare, sempre sotto la supervisione di un medico, per la mia attuale situazione?"
            domanda_2="Quali ulteriori accertamenti posso svolgere per approfondire la mia situazione sanitaria?"
            domanda_3="Ogni quanto dovrei effettuare delle visite di controllo con uno specialista per mantenere sotto controllo la mia situazione?"
            lista = [domanda_1, domanda_2, domanda_3]
            to_return = lista + to_return
        case "Prescrizioni":
            domanda_1="Quali accertamenti o visite aggiuntive devo seguire per la mia attuale situazione?"
            domanda_2="Quali sono le indicazioni che dovrei adottare al mio stile di vita o eventuali visite di controllo per migliorare la mia situazione attuale?"
            domanda_3="Ogni quanto dovrei prendere il farmaco prescritto? Ogni quanto dovrei consultare il medico per mantenere sotto controllo la mia situazione attuale?"
            lista = [domanda_1, domanda_2, domanda_3]
            to_return=lista+to_return
    return to_return



#Riassumi il contenuto di questo documento, focalizzandoti sui punti salienti e sull'argomento

###MI spieghi in modo semplice e chiaro cosa vuol dire il documento, come se fossi un medico?
##Puoi consigliare succesive analisi o uno stile di vita per poter migliorare i valori di riferimento che il soggetto dovrebbe fare?.


#"Lettura Analisi":"Sei un assistente medico che aiuta a interpretare risultati di esami, valori di analisi e referti medici. Leggi il documento allegato, per favore interpreta i valori rispetto a quelli di riferimento e valuta se sono presenti anomalie o i valori sono tutti nella norma.Se emergono anomalie, suggerisci ulteriori analisi diagnostiche da effettuare. Se non emergono anomalie, suggeriscimi uno stile di vita salutare per mantenere o consigliami un consulto adeguato. Fammi una relazione in italiano.",



####PERPLEXITY PROPOSAL
# import os
# import openai
# #import gradio
#
# openai.api_key = "YOUR_API_KEY"
#
# def api_calling(prompt):
#     # Qui si può implementare la logica per determinare se la risposta è valida o meno
#     def is_valid_response(response):
#         invalid_responses = ["Non posso rispondere a questa domanda", "Non ho le informazioni necessarie",
#                              "Mi dispiace, non so","Mi dispiace, ma non posso aiutarti con queste informazioni."]
#         return not any(invalid_response in response for invalid_response in invalid_responses)
#
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "Sei un assistente medico utile."},
#             {"role": "user", "content": prompt},
#         ],
#     )
#
#     while not is_valid_response(response['choices'][0]['message']['content']):
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Sei un assistente medico utile."},
#                 {"role": "user", "content": prompt},
#             ],
#         )
#
#     return response['choices'][0]['message']['content']
#
# #iface = gradio.Interface(fn=api_calling, inputs="text", outputs="text")
# #iface.launch()
# ##lower temperature (0.3-0.7)
# top_p=[0.7,0.9]
# conversation_history = [{"role": "system", "content": "Sei un assistente medico che aiuta a interpretare risultati di esami, valori di analisi e referti medici."}]