from flask import Flask, render_template, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from io import BytesIO
import base64


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'


class BabyForm(FlaskForm):

    babyname = StringField("Enter baby name(s) seperated by commas")
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = BabyForm()

    if form.validate_on_submit():
        
        session['babyname'] = form.babyname.data
        df = pd.read_feather('static/files/names.feather')
        selectedname = df[(df.Name == f'{session["babyname"]}') & (df.Sex == 'M')].set_index('Year')
        print(selectedname)
        fig = Figure(figsize=(14,3))
        ax = fig.add_subplot(111)
        ax.plot(selectedname.Count.index.values.astype(np.uint16),selectedname.Count.values)
        #ax.legend()
        ax.grid()
        #ax.set_title(f'speed = {round(speed_leading,2)} kmh')
        #ax.set_xlabel('Time (s)')
        #ax.set_ylabel('Speed Sensor')

        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        imgdata = base64.b64encode(buf.getbuffer()).decode("ascii")
        #elgin.Count.plot(label='Elgin')

        return render_template('index.html', form=form, imgdata = imgdata)

    return render_template('index.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
