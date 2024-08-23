"""
Install the Google AI Python SDK
pip install google-generativeai
"""
import google.generativeai as genai
genai.configure(api_key="AIzaSyBKtLl0KuRsVi-coW_BGB92xsC808wg1lU") # Aqui va la llave que usted va a generar de Gemini
#Create the model
generation_config = {
"temperature": 1,
"top_p": 0.95,
"top_k": 64,
"max_output_tokens": 8192,
"response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
model_name="gemini-1.5-flash",
generation_config=generation_config,
)
chat_session = model.start_chat(
history=[
]
)
print('bienvenido, este es un programa para que solo con los ingredientes te podamos dar una receta ')
print('---------------------------------------------------------------------------------------------')

#Prompt
prompt = str( input('\ningrese los ingredientes-') )
prompt = 'Quiero una receta con solo estos ingredientes: ' + prompt
print('-------------------------------------------------------------')
response = chat_session.send_message(prompt)
print(response.text)

"""
*antes del proyecto*
1)biblioteca sin AI
2)ventajas yv desventajas
3)los problemas
"""


"""
*entrega de proyecto* 
1)estetica 
2)cambio de prompt
"""