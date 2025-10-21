"""
Async tools for safe coroutine execution
Provides thread-safe execution without nest_asyncio
"""

import asyncio
import threading
import queue
import inspect
import time
from typing import Any, Callable, Optional, Union
from concurrent.futures import TimeoutError


class AsyncExecutor:
    """Thread-safe async executor with private event loop"""
    
    def __init__(self):
        self._thread = None
        self._loop = None
        self._ready = threading.Event()
        self._shutdown = False
        
    def _run_loop(self):
        """Run event loop in dedicated thread"""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._ready.set()
        
        # Run until shutdown
        self._loop.run_forever()
        self._loop.close()
    
    def start(self):
        """Start the executor thread"""
        if self._thread is None or not self._thread.is_alive():
            self._shutdown = False
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()
            self._ready.wait(timeout=2)  # Wait for loop to be ready
            
    def stop(self):
        """Stop the executor"""
        self._shutdown = True
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join(timeout=1)
            
    def run_coro(self, coro, timeout: float = 2.5) -> Any:
        """Run a coroutine with timeout"""
        if not self._loop or not self._thread.is_alive():
            self.start()
            
        # Create a future to hold the result
        future = asyncio.run_coroutine_threadsafe(
            self._add_timeout(coro, timeout),
            self._loop
        )
        
        try:
            return future.result(timeout=timeout + 0.5)  # Extra time for internal timeout
        except TimeoutError:
            future.cancel()
            raise TimeoutError(f"Coroutine execution timed out after {timeout}s")
        except Exception as e:
            # Propagate the original exception
            raise e
            
    async def _add_timeout(self, coro, timeout: float):
        """Add timeout to coroutine"""
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Async operation timed out after {timeout}s")


# Global executor (lazy init)
_global_executor = None


def run_coro_blocking(coro, timeout: float = 2.5) -> Any:
    """
    Execute a coroutine in a blocking manner with timeout
    
    Args:
        coro: The coroutine to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        The result of the coroutine
        
    Raises:
        TimeoutError: If execution exceeds timeout
        Exception: Any exception from the coroutine
    """
    global _global_executor
    
    if _global_executor is None:
        _global_executor = AsyncExecutor()
        
    return _global_executor.run_coro(coro, timeout)


def call_maybe_async(func: Callable, *args, timeout: float = 2.5, **kwargs) -> Any:
    """
    Call a function that might be sync or async
    
    Args:
        func: The function to call
        *args: Positional arguments
        timeout: Maximum execution time for async functions
        **kwargs: Keyword arguments
        
    Returns:
        The result of the function call
        
    Raises:
        TimeoutError: If async execution exceeds timeout
        Exception: Any exception from the function
    """
    # Check if it's a coroutine function
    if inspect.iscoroutinefunction(func):
        # Create the coroutine
        coro = func(*args, **kwargs)
        # Run it blocking
        return run_coro_blocking(coro, timeout)
    
    # Check if it's a regular function
    result = func(*args, **kwargs)
    
    # Check if the result is awaitable
    if inspect.iscoroutine(result):
        # It returned a coroutine, await it
        return run_coro_blocking(result, timeout)
    elif hasattr(result, '__await__'):
        # It's an awaitable object
        async def await_it():
            return await result
        return run_coro_blocking(await_it(), timeout)
    else:
        # It's a regular sync result
        return result


def is_async_callable(func: Callable) -> bool:
    """
    Check if a callable is async (coroutine function)
    
    Args:
        func: The function to check
        
    Returns:
        True if async, False if sync
    """
    return inspect.iscoroutinefunction(func)


def wrap_async_as_sync(async_func: Callable, timeout: float = 2.5) -> Callable:
    """
    Wrap an async function to be callable as sync
    
    Args:
        async_func: The async function to wrap
        timeout: Default timeout for execution
        
    Returns:
        A sync wrapper function
    """
    def sync_wrapper(*args, **kwargs):
        return call_maybe_async(async_func, *args, timeout=timeout, **kwargs)
    
    sync_wrapper.__name__ = f"sync_{async_func.__name__}"
    sync_wrapper.__doc__ = f"Sync wrapper for {async_func.__name__}"
    
    return sync_wrapper


# Cleanup on module unload
import atexit

def _cleanup():
    """Cleanup global executor on exit"""
    global _global_executor
    if _global_executor:
        _global_executor.stop()
        _global_executor = None

atexit.register(_cleanup)


__all__ = [
    'run_coro_blocking',
    'call_maybe_async',
    'is_async_callable',
    'wrap_async_as_sync',
    'AsyncExecutor'
]