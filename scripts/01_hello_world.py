# This goes to stdout -> logs/hello_<job_id>.log
print("Hello World!")

# This goes to stderr -> logs/hello_<job_id>.err because division by zero is forbidden
oops = 1 / 0
