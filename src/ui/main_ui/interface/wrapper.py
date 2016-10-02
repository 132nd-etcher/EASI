# coding=utf-8
def interfaced_method(obj_name):
    """
    Calls method 'func' of object 'object_name' via the main_ui_threading.MainGuiThreading class.

    If set, 'object_name' must be a existing member of the MainUi.

    If 'object_name is None, then 'func' will be evaluated against the MainUi itself.

    :param obj_name: name of the object
    :return: decorator
    """
    def decorator(func):
        def _wrapper(cls, *args, **kwargs):
            try:
                return cls.do(obj_name, '{}'.format(func.__name__), *args, **kwargs)
            except AttributeError:
                raise AttributeError('unknown function in MainInterface: {}'.format(func.__name__))

        return _wrapper

    return decorator
