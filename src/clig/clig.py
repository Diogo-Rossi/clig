import inspect
from argparse import ArgumentParser
from typing import Callable, Any, Tuple


def run(command: Callable[..., Any]):
    parser = ArgumentParser()
    signature = inspect.signature(command)
    parameters = signature.parameters
    for par_name in parameters:
        par = parameters[par_name]
        par_type = str
        par_default = None
        nargs = None
        if par.annotation != par.empty:
            if hasattr(par.annotation, "__metadata__"):
                print("TODO")
                print(par.annotation.__origin__)
                print(par.annotation.__metadata__)
            if callable(par.annotation):
                par_type = par.annotation
        if par.default != par.empty:
            nargs = "?"
            par_default = par.default
        parser.add_argument(par_name, default=par_default, nargs=nargs, type=par_type)
    args = parser.parse_args()
    command(**vars(args))
