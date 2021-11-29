from flask import Flask,jsonify, request
import random
from flask_cors import CORS

app = Flask(__name__)
config = {
  'ORIGINS': [
    'http://localhost:5500',  
    'http://127.0.0.1:5500',  
  ],
}

CORS(app, resources={ r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)

random_number = None
guesses_taken = 0 

@app.route("/range", methods=["POST"])
def enter_the_range():
    ''' 
        function for user to enter the range  
        '''
    data = request.get_json()
    rangestart = data.get("rangestart")
    rangestop = data.get("rangestop")
    global random_number
    random_number = random.randrange(int(rangestart), int(rangestop))
    global guesses_taken
    guesses_taken = 0
    return jsonify({"message" : "range has been inputed"})


def generate_score(guesses_taken):
    '''
    fuction to generate the score 
    '''
    initial_score = 5
    score = initial_score - guesses_taken
    return score

@app.route("/guess", methods=["POST"])
def guess_the_random_number():
    '''
    fuction for the user to guess what the random number is.
    '''
    data = request.get_json()
    guess = int(data.get("guess"))
    hints = [] 
    global guesses_taken

    if guesses_taken < 6:
        if guess == random_number:
            return jsonify({"message" : "correct", "score" : generate_score(guesses_taken)})
        if guess < random_number:
            hints.append("Your guess is too low")
        if guess > random_number :
            hints.append("Your guess is too high")
        if random_number % 2 == 0:
            hints.append("The random number is a multiple of 2")
        if random_number % 3 == 0:
            hints.append("The random number is a multiple of 3")
        if random_number % 5 == 0:
            hints.append("The random number is a multiple of 5")
        guesses_taken += 1
    else:
        return jsonify({ "message": "No more tries, go back andtry again"})
    return jsonify({"message" : "incorect guess try again", "hints" : hints })

if __name__ == ("__main__"):
    app.run(debug= True)