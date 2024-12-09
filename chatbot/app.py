import csv
import re
import random


movies = []
with open('/Users/soha/Desktop/chatbot/movies.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        movies.append({'name': row[0], 'year': row[1], 'description': row[2]})
# Responses for the chatbot
R_GREETING = "Hello! I'm a movie chatbot. Ask me about any movie you like."
R_HI="Hey"
R_BYE = "Goodbye! It was nice talking to you."
R_UNKNOWN = "I'm sorry, I didn't understand what you meant. Can you rephrase your question?"
R_DESCRIPTION = "The movie {} was released in {}. Here's a brief description: {}"
R_QUIT = "Quiting the bot"
#movies list
Comedy_list=["Dumb and Dumber","Scary movie","Airplane!","The hangover"]
Action_list=["The Terminator","John Wick","The Dark Knight","The Raid","Mission: Impossible"]
Scifi_list=["Inception","Blade Runner","The Matrix","Interstellar","The Terminator"]
Drama_list=["No Country for Old Men",'The Godfather',"Forrest Gump","The Social Network","Top Gun"]
Horror_list=["The Exorcist","The Conjuring","Hereditary","Get out","Martyrs"]
Telugu_list=["Khaleja","Baahubali","Chatrapathi"]
Thriller_list=["No Country for Old Men","Shutter Island","The Departed","The Usual Suspects","Memento"]
Romance_list=["Titanic","Her","La La Land","Lost in Translation"]

comedy_keywords = ['comedy', 'funny', 'humorous']
drama_keywords = ['drama', 'serious', 'emotional']
action_keywords = ['action', 'adventure', 'thrilling']
scifi_keywords = ['sci-fi', 'science fiction', 'futuristic']
horror_keywords = ['horror', 'scary', 'creepy']
telugu_keywords = ['telugu', 'tollywood', 'andhra']
thriller_keywords = ['thriller', 'suspenseful', 'mystery']
romance_keywords = ['romance', 'romantic', 'love']
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True
    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0
# Function to generate a response based on user input
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    # Check if user wants to end the conversation
    request_types = {
    'comedy': message_probability(split_message, comedy_keywords),
    'drama': message_probability(split_message, drama_keywords),
    'action': message_probability(split_message, action_keywords),
    'scifi': message_probability(split_message, scifi_keywords),
    'horror': message_probability(split_message, horror_keywords),
    'telugu': message_probability(split_message, telugu_keywords),
    'thriller': message_probability(split_message, thriller_keywords),
    'romance': message_probability(split_message, romance_keywords)
    }

    sorted_requests = sorted(request_types.items(), key=lambda x: x[1], reverse=True)

    # Get the response for the most likely request type
    for request_type, probability in sorted_requests:
        if probability > 0:
            if request_type == 'comedy':
                temp=random.choice(Comedy_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'drama':
                temp=random.choice(Drama_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'action':
                temp=random.choice(Action_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'scifi':
                temp=random.choice(Scifi_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'horror':
                temp=random.choice(Horror_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'telugu':
                temp=random.choice(Telugu_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'thriller':
                temp=random.choice(Thriller_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
            elif request_type == 'romance':
                temp=random.choice(Romance_list)
                return 'I would recommend watching {} \nDESCRIPTION: {}'.format(temp,get_response(temp))
    for movie in movies:
            if movie['name'].lower().startswith(user_input.lower()):
                return R_DESCRIPTION.format(movie['name'], movie['year'], movie['description'])
    for movie in movies:
                for word in split_message:
                    if movie['name'].lower().endswith(word):
                        return R_DESCRIPTION.format(movie['name'], movie['year'], movie['description'])  
    # If no other match is found, return unknown response
    return R_UNKNOWN

print(R_GREETING)
while True:
    user_input = input('> ')
    bot_response = get_response(user_input)
    print(bot_response)
    if (user_input=='quit') or (user_input=='close'):
        break


    
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get-response")
def get_bot_response():
    user_input = request.args.get("user-input")
    # process user input and generate bot response
    bot_response = "Hello, I'm a movie chatbot!"
    return jsonify({"bot-response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
