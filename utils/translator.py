def translate_to_propositional_logic(feature_model):
    logic_formula = []
    feature_map = {}  # This will map feature names to unique integers
    
    feature_counter = 1  # Start assigning integers from 1
    for feature in feature_model['features']:
        feature_name = feature['name']
        
        # Map feature names to unique integers
        feature_map[feature_name] = feature_counter
        feature_counter += 1
        
        mandatory = feature.get('mandatory', False)

        # Add the feature logic to the formula
        if mandatory:
            logic_formula.append(f"{feature_map[feature_name]}")  # For mandatory: just the feature
        else:
            logic_formula.append(f"¬{feature_map[feature_name]}")  # For optional: negated feature

        # Handle groups (OR and XOR)
        for group in feature.get('groups', []):
            group_type = group['type']
            group_features = group['features']

            if group_type == 'xor':
                xor_clause = " ∨ ".join(str(feature_map[f]) for f in group_features)
                logic_formula.append(f"({xor_clause})")
            elif group_type == 'or':
                or_clause = " ∨ ".join(str(feature_map[f]) for f in group_features)
                logic_formula.append(f"({or_clause})")

    return " ∧ ".join(logic_formula)