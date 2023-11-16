 from flask import Flask, render_template, request
import openai
import os
import pdf2text

app = Flask(__name__)

# Configura tu clave de API de OpenAI
openai.api_key = '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'

# Ruta al directorio que contiene tus documentos PDF
pdf_directory = 'pdf_files'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preguntar', methods=['POST'])
def preguntar():
    pregunta = request.form['pregunta']

    # Lee el contenido de los documentos PDF
    contenido_pdf = ''
    for filename in os.listdir(pdf_directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, filename)
            contenido_pdf += pdf2text.extract_text(pdf_path)

    # Combina el contenido de los PDF y la pregunta
    entrada_modelo = f"Contenido de los PDF: {contenido_pdf}\nPregunta: {pregunta}"

    # Realiza la solicitud a la API de GPT-3.5
    respuesta = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=entrada_modelo,
        max_tokens=150
    )

    respuesta_chatbot = respuesta['choices'][0]['text']
    
    return render_template('index.html', pregunta=pregunta, respuesta=respuesta_chatbot)

if __name__ == '__main__':
    app.run(debug=True)
python app.py
