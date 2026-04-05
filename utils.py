import time
from datetime import datetime
from functools import wraps

# Global dictionary to track last execution times
_execution_times = {}


def debug(message):
    """
    Print a custom debug message with timestamp.
    
    Args:
        message (str): The debug message to print
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[DEBUG {timestamp}] {message}")


def monitor_execution_time(func_name=None):
    """
    Decorator to monitor and print time between function executions.
    Can also be used as a context manager or called directly to mark time points.
    
    Args:
        func_name (str, optional): Name to track execution time for
        
    Returns:
        float: Time elapsed (in seconds) since last execution of this function/name
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            name = func_name or func.__name__
            current_time = time.time()
            
            if name in _execution_times:
                elapsed = current_time - _execution_times[name]
                debug(f"Time since last '{name}' execution: {elapsed:.4f}s")
            else:
                debug(f"First execution of '{name}'")
            
            _execution_times[name] = current_time
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def mark_time(identifier):
    """
    Mark a time point and return elapsed time since last mark for this identifier.
    
    Args:
        identifier (str): Unique identifier for this time point
        
    Returns:
        float: Elapsed time (in seconds) since last mark, or None if first call
    """
    current_time = time.time()
    
    if identifier in _execution_times:
        elapsed = current_time - _execution_times[identifier]
        debug(f"Time since last mark '{identifier}': {elapsed:.4f}s")
    else:
        #debug(f"First time mark for '{identifier}'")
        elapsed = None
    
    _execution_times[identifier] = current_time
    return elapsed
