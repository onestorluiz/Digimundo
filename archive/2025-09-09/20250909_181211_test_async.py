from apps.scripturemon.utils.async_tools import call_maybe_async
import asyncio

# Test sync function
def sync_func(x):
    return x * 2

# Test async function
async def async_func(x):
    await asyncio.sleep(0.01)
    return x * 3

# Test both
sync_result = call_maybe_async(sync_func, 5)
async_result = call_maybe_async(async_func, 5)

print(f"Sync result: {sync_result}")
print(f"Async result: {async_result}")
print("✅ Async tools working" if sync_result == 10 and async_result == 15 else "❌ Async tools failed")
