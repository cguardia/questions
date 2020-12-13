import json


def get_params_for_repr(params):
    param_list = []
    for name, param in sorted(params.items()):
        param_str = json.dumps(param)
        if param_str == "true":
            param_str = "True"
        if param_str == "false":
            param_str = "False"
        param_list.append(f"{name}={param_str}")
    return "\n        " + ",\n        ".join(param_list)
