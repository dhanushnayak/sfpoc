import setuptools

with open("README.md",'r',encoding="utf-8") as f: long_description = f.read()

__version__ = "1.1"

REPO_NAME =  "sfpro"
AUTHOR_USER_NAME = "dhanush"
SRC_REPO = "sfpro"
AUTHOR_EMAIL =  "dhanushnayak.ram@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Snowflake_POC",
    long_description=long_description,
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
)