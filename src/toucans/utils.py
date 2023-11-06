from jinja2 import Environment, meta


def extract_template_params(template_str):
    """
    Extract variables from a Jinja2 template string.

    Parameters:
    - template_str (str): The Jinja2 template as a string.

    Returns:
    - set: A set of variable names found in the template.
    """
    env = Environment()

    # Parse the template string to create an Abstract Syntax Tree (AST)
    ast = env.parse(template_str)

    # Use the meta module to find all variables in the AST
    variables = meta.find_undeclared_variables(ast)

    return list(variables)


def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]
