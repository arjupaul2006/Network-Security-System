'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path: str) -> List[str]:
    """
    get all requirements
    """

    try:
        requirements = []
        with open(file_path, 'rb') as file_obj:
            lines = file_obj.readlines()

            for line in lines:
                requirement = line.strip()

                if requirements and requirements != HYPEN_E_DOT:
                    requirements.append(requirement)

    except FileExistsError:
        print('Requirements.txt Not Found')
        

    return requirements

setup(
    name='Network Security System',
    version='0.0.1',
    author='Arju Paul',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)