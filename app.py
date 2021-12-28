from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import json
import pandas as pd

#load data
file_reading = json.loads(open('dummy.json').read())
df = pd.DataFrame.from_dict(file_reading['data'])
#clean data
df['title'] = df['title'].str.replace('\t', '')
df['title'] = df['title'].str.replace('\n', '')


#inisiasi web
def create_app():
  app = Flask(__name__)
  Bootstrap(app)
  return app

app = Flask(__name__)

#menampilkan list film
@app.route('/')
def home():
    title, genre, rating, duration, quality, trailer, watch= \
        df['title'].tolist(), df['genre'].tolist(), df['rating'].tolist(), df['duration'].tolist(), df['quality'].tolist(), df['trailer'].tolist(), df['watch'].tolist()
    return render_template('home.html', data_list=zip(title,genre,rating,duration,quality,trailer,watch))


#route ke form upload
@app.route('/formUpload')
def upload():
    return render_template('formUpload.html')


#delete film
@app.route('/handle_delete', methods=["GET","POST"])
def handle_delete():
    global df
    if request.method == 'POST':
        post_id = int(request.form.get('delete'))
        if post_id is not None:
            df = df.drop(df.index[post_id-1])
            df.to_json('temp.json', orient='records', lines=True)
            return redirect("/")


#upload film
@app.route('/handle_upload', methods=['POST'])
def handle_upload():
    global df
    list_genre = []
    title = request.form['title']
    rating = request.form['rating']
    trailer = request.form['trailer']
    watch = request.form['watch']
    duration = request.form['duration']
    quality = request.form['quality']
    if request.form.get('drama'):
        list_genre.append('Drama')
    if request.form.get('horor'):
        list_genre.append('Horor')
    if request.form.get('romance'):
        list_genre.append('Romance')
    if request.form.get('action'):
        list_genre.append('Action')

    new_row = {'title': title, 'genre': list_genre, 'rating': rating, 'duration': str(duration)+' min',
               'quality': quality, 'trailer': trailer, 'watch': watch}
    df = df.append(new_row, ignore_index=True)
    df.to_json('temp.json', orient='records', lines=True)
    return redirect("/")

#run app
if __name__ == '__main__':
    app.run()