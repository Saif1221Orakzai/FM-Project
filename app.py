from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from utils.parser import parse_feature_model
from utils.translator import translate_to_propositional_logic
from utils.sat_solver import check_configuration, find_minimum_working_product

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'

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
    
    # Convert the parsed features into options for the user to select
    feature_names = feature_model['features']  # Assuming `parse_feature_model` returns a dictionary with a 'features' key
    
    return render_template('visualize.html', model=feature_model, logic=logic_formula, features=feature_names)

@app.route('/validate', methods=['POST'])
def validate_selection():
    # Get the selected features from the form
    selected_features = [int(feature) for feature in request.form.getlist('features')]  # Convert to integers
    
    # Get the propositional logic formula from the form (you may need to handle it better if it is not in a simple format)
    logic_formula = request.form.get('logic')
    
    # Check if the configuration is valid
    is_valid, reasons = check_configuration(selected_features, logic_formula)
    
    return jsonify({'is_valid': is_valid, 'reasons': reasons})

@app.route('/minimize', methods=['POST'])
def minimize_features():
    # Get the selected features from the form
    selected_features = [int(feature) for feature in request.form.getlist('features')]
    
    # Get the propositional logic formula from the form
    logic_formula = request.form.get('logic')
    
    # Parse the logic formula into clauses
    clauses = [parse_clause(clause) for clause in logic_formula.split(' ∧ ')]
    
    # Find the minimal working product (set of features)
    minimum_working_set = find_minimum_working_product(clauses, selected_features)
    
    return jsonify({'minimum_working_set': minimum_working_set})

# Helper function to parse the clauses into a format suitable for the SAT solver
def parse_clause(clause):
    """
    Convert a clause from propositional logic to a format suitable for SAT solver.
    Clause should be in the form 'p ∨ q ∨ ¬r'
    This function converts it to a list of integers, where ¬ is represented by a negative sign.
    """
    literals = clause.replace('¬', '-').split(' ∨ ')
    return [int(lit.strip()) for lit in literals]

if __name__ == '__main__':
    app.run(debug=True)