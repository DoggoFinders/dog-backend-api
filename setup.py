from setuptools import setup, find_packages

reqs = []
try:
    with open('requirements.txt') as f:
        reqs = [l.strip() for l in f.readlines() if l.strip()]
except:
    pass

print(reqs)
setup(
    name="doggo-backend-api",
    version="0.1",
    packages=find_packages(exclude=("tests*", "*tests", "tests")),
    install_requires=reqs,
    extras_require={"dev": ["flake8", "pytest", "black==20.8b1", "isort"]},
    python_requires='>=3.6'
)
