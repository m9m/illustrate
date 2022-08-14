from setuptools import setup, find_packages

with open("README.md", "r") as fd:
    read_me = fd.read()
    
with open("requirements.txt", "r") as fd:
    requirements = fd.read()

setup(
    name='illustrate',
    version='1.0.1',
    author='m9m',
    license='MIT',
    project_urls={
        "Website": "https://m9m.dev",
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