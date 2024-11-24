from subprocess import run

if __name__ == "__main__":
    run("poetry version patch", shell=True, check=True)
    run("poetry publish --build", shell=True, check=True)