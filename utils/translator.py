def translate_to_propositional_logic(feature_model):
    # Initialize the propositional logic formula
    logic_formula = []

    for feature in feature_model['features']:
        # Ensure 'type' exists and default to 'optional' if it's missing
        feature_type = feature.get('type', 'optional')

        # Process the feature based on its type
        if feature_type == 'mandatory':
            logic_formula.append(f"{feature['name']} is mandatory")
        else:
            logic_formula.append(f"{feature['name']} is optional")
        
        # You can add other logic here for specific group types or other feature properties

    return logic_formula
