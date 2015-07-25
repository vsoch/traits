from flask import Flask, render_template
import pandas
import os

app = Flask(__name__)

from cognitiveatlas import load_behaviors, Behavior, get_json
import random
import json

def get_behavior(trait):
    return Behavior(trait)


@app.route('/about')
def show_about():
    return render_template('about.html')


@app.route('/')
def explore_traits():
    
    # Read in behavioral terms and cattell terms
    traits = load_behaviors()
    cattell = pandas.read_pickle("data/pickle/cattell_personality_282.pkl").trait.unique().tolist()
    behaviors = [x.replace("\xc3\xaf","i") for x in traits + cattell]
        

    # Generate Behavior object with related terms
    behavior = get_behavior(random.sample(traits,1)[0])
    if len(behavior.is_a) == 0:   
        myjson = {"nodes":[{"name":behavior.trait}],"links":[]}
    else:
        myjson = get_json(behavior)
    prettyjson = json.dumps(myjson, sort_keys=True, indent=4, separators=(',', ': '))

    return render_template('index.html',prettyjson=prettyjson,behavior=behavior.trait,behaviors=behaviors)


@app.route('/cattell')
def show_traits():

    # Load the personality traits
    traits = pandas.read_pickle("data/pickle/cattell_personality_282.pkl")

    # Replace NaN with empty cells
    traits = traits.fillna("")

    # Render into a table
    table = traits.to_html(index=None,classes="table table-striped table-bordered")

    # Add the id
    table = table.replace('class="dataframe',' id="chart" class="dataframe')  

    # Match terms with their opposites
    terms = traits.trait.tolist()
    opposites = traits.opposite.tolist()
    searchcontent = zip(terms,opposites)

    return render_template('cattell.html',table=table,search=searchcontent)


if __name__ == '__main__':
    app.debug = True
    app.run()
