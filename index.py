from flask import Flask, render_template, jsonify
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

def get_behaviors_df():
    # Read in behavioral terms and cattell terms
    traits = load_behaviors()
    cattell = pandas.read_pickle("data/pickle/cattell_personality_282.pkl").trait.unique().tolist()
    df = pandas.DataFrame()
    df["traits"] =  [x.replace("\xc3\xaf","i") for x in traits + cattell]
    df["sources"] = ["CNP" for x in range(len(traits))] + ["cattell" for x in range(len(cattell))]
    df["ids"] = [x.replace(" ","").replace("(","").replace(")","") for x in df.traits]
    return df.sort(columns="traits")
 
def get_prettyjson(behavior):
    if len(behavior.is_a) == 0:   
        myjson = {"nodes":[{"name":behavior.trait,"definition":""}],"links":[]}
    else:
        myjson = get_json(behavior)
    return json.dumps(myjson, sort_keys=True, indent=4, separators=(',', ': '))

def render_index(trait,df):
    behavior = get_behavior(trait)
    prettyjson = get_prettyjson(behavior)
    behaviors = zip(df.traits.tolist(),range(len(df.index)),df.ids.tolist(),df.sources.tolist())

    return render_template('index.html',prettyjson=prettyjson,behavior=behavior.trait,behaviors=behaviors)


@app.route('/download/<traitid>')
def download_trait(traitid):
    df = get_behaviors_df()
    
    # Find the selected trait
    trait = str(df["traits"][df["ids"] == traitid].tolist()[0])
    behavior = get_behavior(trait)
    if len(behavior.is_a) == 0:   
        myjson = {"nodes":[{"name":behavior.trait,"definition":""}],"links":[]}
    else:
        myjson = get_json(behavior)
    return jsonify(**myjson)

   
@app.route('/view/<traitid>')
def select_traits(traitid):
    df = get_behaviors_df()
    
    # Find the selected trait
    trait = str(df["traits"][df["ids"] == traitid].tolist()[0])
    return render_index(trait,df)

@app.route('/')
def explore_traits():
    
    df = get_behaviors_df()
    behaviors = zip(df.traits.tolist(),range(len(df.index)),df.ids.tolist(),df.sources.tolist())    

    # Generate Behavior object with related terms
    trait = random.sample(df.traits.tolist(),1)[0]
    return render_index(trait,df)

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
    app.run(host="0.0.0.0")
