from tasks import add
result = add.delay(4, 4)
#delay() is used to call a task
print(result.ready())
#ready() returns whether the task has finished processing or not.
print(result.get(timeout=1))
#get() is used for getting results
result.get(propagate=False)
#In case the task raised an exception, get() will re-raise the exception, but you can override this by specifying the propagate argument