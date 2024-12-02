from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from utils.parser import parse_feature_model
from utils.translator import translate_to_propositional_logic
from utils.sat_solver import check_configuration, find_minimum_working_product

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'

# Ensure uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

feature_map = {
    'Application': 1,
    'Catalog': 2,
    'Filtered': 3,
    'Notification': 4,
    'Location': 5,
    'Payment': 6,
    'WiFi': 7,
    'GPS': 8,
    'CreditCard': 9,
    'Discount': 10,
    'ByDiscount': 11,
    'ByWeather': 12,
    'ByLocation': 13,
    'SMS': 14,
    'Call': 15
}

def validate_logic_formula(logic_formula):
    """
    Checks if the logic formula contains only valid literals and operators.
    """
    # Define valid literals and operators
    valid_literals = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    valid_operators = {'∧', '∨', '¬', '(', ')'}
    
    # Check for invalid characters
    for char in logic_formula:
        if char not in valid_literals and char not in valid_operators and char != ' ':
            print(f"Warning: Invalid character '{char}' in logic formula.")
            return False

    # Check if the formula has balanced parentheses
    open_parens = 0
    for char in logic_formula:
        if char == '(':
            open_parens += 1
        elif char == ')':
            open_parens -= 1
        if open_parens < 0:
            return False

    if open_parens != 0:
        return False

    return True

# Routes
@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file uploaded!')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file!')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Parse and validate XML
        parsed_model = parse_feature_model(filepath)
        return redirect(url_for('visualize', filepath=filepath))
    return 'Upload Failed', 400

@app.route('/visualize')
def visualize():
    filepath = request.args.get('filepath')
    feature_model = parse_feature_model(filepath)
    logic_formula = translate_to_propositional_logic(feature_model)

    return render_template('visualize.html', model=feature_model, logic=logic_formula, features=feature_model['features'])

@app.route('/validate', methods=['POST'])
def validate_selection():
    logic_formula = request.form.get('logic')
    
    # Map selected features (name) to their integer IDs
    selected_features = [feature_map[feature] for feature in request.form.getlist('features')]

    # Validate the logic formula
    if not validate_logic_formula(logic_formula):
        return jsonify({'is_valid': False, 'reasons': ['Invalid characters in the formula']})

    # Check if the configuration is valid
    is_valid, reasons = check_configuration(selected_features, logic_formula)
    
    return jsonify({'is_valid': is_valid, 'reasons': reasons})

@app.route('/minimize', methods=['POST'])
def minimize_features():
    logic_formula = request.form.get('logic')
    selected_features = request.form.getlist('features')

    clauses = [clause.split(' ∨ ') for clause in logic_formula.split(' ∧ ')]
    minimum_working_set = find_minimum_working_product(clauses, selected_features)

    return jsonify({'minimum_working_set': minimum_working_set})

if __name__ == '__main__':
    app.run(debug=True)