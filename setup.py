from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fd:
    read_me = fd.read()

requirements = []
with open("requirements.txt", "r", encoding="utf-8") as fd:
    requirements = fd.read().splitlines()

setup(
    name='illustrate',
    version='1.0.1',
    author='m9m',
    license='MIT',
    project_urls={
        "Website": "https://www.keeganm.net",
        "Github": "https://github.com/m9m/illustrate",
    },
    description="Simplistic & powerful crypto analytics through Discord",
    long_description=read_me,
    long_description_content_type="text/markdown",
    url="https://github.com/m9m/illustrate",
    python_requires=">=3.8.0",
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages()
)
