import os


# get an env var, if the env var is not provided the program crash
def expect_env_var(var):
    res = os.environ.get(var)
    if res == None:
        print("error: please provide env ", var)
        exit(1)
    return res
