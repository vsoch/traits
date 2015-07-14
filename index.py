from flask import Flask, render_template
import pandas
import os

app = Flask(__name__)

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.route('/')
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

    return render_template('index.html',table=table,search=searchcontent)

if __name__ == '__main__':
    app.debug = True
    app.run()
