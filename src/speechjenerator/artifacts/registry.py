"""
Implements a simple decorator-based model registry for dynamically managing
different artifact classes.

This system allows concrete subclasses to register themselves
using a specific string key, enabling the application to instantiate the 
correct class based on a configuration setting without explicit imports.
"""

ARTIFACT_REGISTRY = {}

def register_model(name):
    """
    A decorator factory used to register a subclass.

    The decorated class is stored in the global ARTIFACT_REGISTRY dictionary
    under the provided `name`.

    Args:
        name (str): The string key used to reference the model class
                    in the configuration.

    Returns:
        Callable: A decorator function that takes a class and registers it.
    """
    def decorator(cls):
        ARTIFACT_REGISTRY[name] = cls
        return cls
    return decorator


def get_class(artifact_name):
    """
    Retrieves and instantiates the correct class based on the
    configuration dictionary.

    It looks up the class in ARTIFACT_REGISTRY using `artifact_name`.

    Args:
        artifact_name: Must correspond to a registered artifact name.

    Returns:
        An instantiated object of the registered class.

    Raises:
        KeyError: If the value of `artifact_name` is not found in the
                  ARTIFACT_REGISTRY.
    """
    Class_ = ARTIFACT_REGISTRY[artifact_name]
    artifact = Class_()

    return model_object