from pycosat import solve

def check_configuration(selected_features, logic_formula):
    """
    Check if the selected features satisfy the given propositional logic formula.
    """
    clauses = [parse_clause(clause) for clause in logic_formula.split(' ∧ ')]
    is_valid = solve(clauses, assumptions=selected_features)
    reasons = [] if is_valid else "Unsatisfiable"  # Reason could be model or failure
    return is_valid, reasons

def parse_clause(clause):
    """
    Convert a clause from propositional logic to a format suitable for SAT solver.
    Clause should be in the form 'p ∨ q ∨ ¬r'
    This function converts it to a list of integers, where ¬ is represented by a negative sign.
    """
    literals = clause.replace('¬', '-').split(' ∨ ')
    return [int(lit.strip()) for lit in literals]

def find_minimum_working_product(clauses, selected_features):
    """
    Find the minimal set of features that satisfy the propositional formula.
    This function will simplify the clause set iteratively by removing features
    that do not affect the result.
    """
    # Try the selected features first
    result = solve(clauses, assumptions=selected_features)
    
    if result:
        # Once we find a valid configuration, try to minimize the set of selected features
        working_set = selected_features.copy()
        for feature in selected_features:
            temp_set = working_set.copy()
            temp_set.remove(feature)
            # Test if removing the feature still results in a valid solution
            if not solve(clauses, assumptions=temp_set):
                working_set.remove(feature)  # If it no longer satisfies, keep the feature
        return working_set
    return []  # Return an empty list if no solution found
