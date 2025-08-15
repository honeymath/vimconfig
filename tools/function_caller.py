import traceback
def call_function(func, args):
#    print(f"THE CALL FUNCTION{func} with {args} HAD BEEN CALLED", flush=True)
    """
    Due to the limitation of Vim, this is a wrapper function to call and catch the traceback. It has parameters,
    func: The funcation, it must be callable.
    args: This is the dictionary of the arguments that pass to the functions
    """
    __vimsocket_result = {}
    if not callable(func):
        __vimsocket_result["sucess"] = False
        __vimsocket_result["error"] = "The function is not callable"
        __vimsocket_result["result"] = ""
    try:
        __vimsocket_result["result"] = func(**args)
        __vimsocket_result["sucess"] = True
        __vimsocket_result["error"] = ""
    except Exception as e:
        __vimsocket_result["sucess"] = False
        __vimsocket_result["error"] = traceback.format_exc()
        __vimsocket_result["result"] = ""
    return __vimsocket_result


if __name__ == "__main__":
    # Test the function with a sample function
    def sample_function(a, b):
        return a + b

    args = {"a": 5, "b": 10}
    result = call_function(sample_function, args)
    print(result)  # Expected output: {'result': 15, 'sucess': True, 'error': ''}
    def failing_function(a, b):
        return a / b
    args = {"a": 5, "b": 0}
    result = call_function(failing_function, args)
    print(result)  # Expected output: {'result': '', 'sucess': False, 'error': 'division by zero'}
