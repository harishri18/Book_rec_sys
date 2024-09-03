from flask import Flask, render_template, request
import dill
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the models using dill
with open('content_based_recommender_with_ratings.dill', 'rb') as file:
    content_based_recommender_with_ratings = dill.load(file)

with open('item_based_recommender.dill', 'rb') as file:
    item = dill.load(file)

with open('content_based_recommender_with_actual_ratings.dill', 'rb') as file:
    simi_sco = dill.load(file)


with open('books.dill', 'rb') as file:
    books = dill.load(file)

with open('df.dill', 'rb') as file:
    df= dill.load(file)

with open('pt.dill', 'rb') as file:
    pt = dill.load(file)

with open('similarity_scores.dill', 'rb') as file:
    similarity_scores = dill.load(file)

@app.route('/')
def index():
    # Show top 10 books on the homepage
    top_books = df.nlargest(10, 'rating')
    return render_template('ind.html',
                           book_name=list(top_books['Book_title'].values),
                           author=list(top_books['Book-Author'].values),
                           image=list(top_books['Image-URL-M'].values),
                           votes=list(top_books['rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_id = request.form.get('user_id')
    user_input = request.form.get('user_input')

    # Ensure recommendations are user-specific
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []

    # Include the input book as the first recommendation
    input_book_info = books[books['Book-Title'] == user_input].drop_duplicates('Book-Title')
    data.append([
        input_book_info['Book-Title'].values[0],
        input_book_info['Book-Author'].values[0],
        input_book_info['Image-URL-M'].values[0]
    ])
    data=[]
    for i in similar_items:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(items)

    # "People Also Search For" Section (Similar books)
    people_also_search = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[5:10]

    also_search_data = []
    for i in people_also_search:
        items = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        also_search_data.append(items)

    return render_template('recommend.html', user_id=user_id, data=data, also_search_data=also_search_data)

if __name__ == '__main__':
    app.run(debug=True)
