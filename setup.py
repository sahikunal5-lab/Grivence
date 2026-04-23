from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requiremts = []
    with open(file_path) as file_obj:
        requiremts = file_obj.readlines()
        requiremts = [req.replace("\n","") for req in requiremts]

        if HYPEN_E_DOT in requiremts:
            requiremts.remove(HYPEN_E_DOT)
    
    return requiremts


setup(
    name="Grivence",
    version="0.0.1",
    author='Kunal',
    author_email="sahikunal5@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')

)