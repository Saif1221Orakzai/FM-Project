from pysat.formula import CNF
from pysat.solvers import Solver

def check_configuration(selected_features, logic_formula):
    """
    Checks if the selected features satisfy the propositional logic formula.
    """
    # Convert the logic formula into clauses
    clauses = []
    for clause in logic_formula.split(" ∧ "):  # Split into individual clauses
        literals = clause.replace("¬", "-").split(" ∨ ")  # Convert ¬ to negative literals
        cleaned_literals = [lit.strip() for lit in literals if lit.strip() and lit.strip() != "()"]
        if cleaned_literals:
            clauses.append([int(lit) for lit in cleaned_literals])  # Convert to integers

    # Debugging: Print the clauses
    print("Clauses:", clauses)

    # Create a CNF object with the clauses
    cnf = CNF(from_clauses=clauses)

    # Convert selected_features to integer literals (positive for selected, negative for deselected)
    assumptions = [int(f) for f in selected_features]

    # Debugging: Print assumptions
    print("Assumptions:", assumptions)

    # Check if the configuration satisfies the CNF formula
    with Solver(bootstrap_with=cnf) as solver:
        is_valid = solver.solve(assumptions=assumptions)
        reasons = [] if is_valid else ["Configuration is unsatisfiable"]
        
        # Debugging: Output result of solver
        print("Solver Result:", is_valid)
        
        return is_valid, reasons

def find_minimum_working_product(clauses, selected_features):
    """
    Find the minimal set of features that satisfy the propositional formula.
    This function will simplify the clause set iteratively by removing features
    that do not affect the result.
    """
    with Solver(bootstrap_with=clauses) as solver:
        # First, check if the selected features provide a valid configuration
        if solver.solve(assumptions=selected_features):
            # Working set initially is all selected features
            working_set = selected_features.copy()

            # Try removing features to find a minimal working set
            for feature in selected_features:
                temp_set = working_set.copy()
                temp_set.remove(feature)
                if solver.solve(assumptions=temp_set):
                    working_set.remove(feature)  # Feature can be safely removed
            return working_set
        else:
            return []  # No valid configuration found