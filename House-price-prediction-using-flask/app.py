from flask import Flask, render_template, request, flash, redirect, url_for
import numpy as np
import pickle
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        floors = request.form.get('floors')
        yr_built = request.form.get('yr_built')

        # Validate inputs
        if not all([bedrooms, bathrooms, floors, yr_built]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))

        # Convert to float and validate ranges
        try:
            bedrooms = float(bedrooms)
            bathrooms = float(bathrooms)
            floors = float(floors)
            yr_built = float(yr_built)
        except ValueError:
            flash('Please enter valid numbers', 'error')
            return redirect(url_for('index'))

        # Validate ranges
        if not (0 < bedrooms < 20 and 0 < bathrooms < 20 and 0 < floors < 10 and 1800 < yr_built < 2025):
            flash('Please enter values within reasonable ranges', 'error')
            return redirect(url_for('index'))

        # Make prediction
        arr = np.array([bedrooms, bathrooms, floors, yr_built])
        pred = model.predict([arr])
        
        # Format the prediction as currency
        formatted_price = "${:,.2f}".format(float(pred[0]))
        flash(f'Predicted House Price: {formatted_price}', 'success')
        
    except Exception as e:
        flash('An error occurred while making the prediction', 'error')
        print(f"Error: {str(e)}")
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
