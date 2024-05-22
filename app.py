from flask import Flask, request, jsonify
from datetime import datetime
import pytz
from flask_cors import CORS
import spacy

app = Flask(__name__)
CORS(app)

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Extract information from user input
def extract_information(text):
    doc = nlp(text)
    # Extract individual nouns
    nouns = [token.text for token in doc if token.pos_ == 'NOUN']
    # Perform Named Entity Recognition (NER)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return nouns, entities

# Generate response based on user input
def generate_response(user_input, nouns, entities):
    # Example response generation based on extracted nouns and entities
    if nouns:
        response = f"I noticed you mentioned {', '.join(nouns)}."
    else:
        response = "I'm not sure I understand. Can you provide more information?"
    if entities:
        response += f" I also found these named entities: {', '.join([f'{entity[0]} ({entity[1]})' for entity in entities])}"
    return response

@app.route('/message', methods=['POST'])
def message():
    message = request.form['message']
    if "what's the time now in" in message:
        country = message.split("in")[-1].strip()
        timezone = pytz.timezone(country)
        current_time = datetime.now(timezone)
        return str(current_time)
    else:
        return "I don't understand."

@app.route('/remove-unwanted-phrases', methods=['POST'])
def remove_unwanted_phrases():
    data = request.get_json()
    text = data['text']
    # Extract information and named entities from user input
    nouns, entities = extract_information(text)
    # Generate response based on extracted information
    response = generate_response(text, nouns, entities)
    return jsonify({'nouns': nouns, 'entities': entities, 'response': response})

if __name__ == '__main__':
    app.run(port=5000)
