from flask import Flask,render_template,request
import pickle
import numpy as np

app=Flask(__name__)

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

@app.route('/')
def display_popular():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].values,
                           author=popular_df['Book-Author'].values,
                           image=popular_df['Image-URL-M'].values,
                           votes=popular_df['num_ratings'].values,
                           rating=[round(value, 2) for value in popular_df['avg_rating'].values]
                           )

@app.route('/recommend')
def recommend_page():
    books_names=pt.index
    return render_template('recommendation.html',books_names=books_names)

def recommend(book_name):
    book_index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[book_index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Publisher'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

@app.route('/recommend_books',methods=['post'])
def recommend_books():
    books_names = pt.index
    book_name=request.form['book']
    data=recommend(book_name)
    return render_template('recommendation.html',data=data,books_names=books_names,book_name=book_name)

if __name__== '__main__':
    app.run(debug=True)