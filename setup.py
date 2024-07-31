from setuptools import setup, find_packages

setup(
    name='Calificator',  
    version='0.1',  
    packages=find_packages(where='src'),  # Busca los paquetes en el directorio 'src'
    package_dir={'': 'src'},  # Define el directorio raíz de los paquetes
    install_requires=[
        'numpy>=2.0.1',  
        'pandas>=2.2.2',  
    ],
  

)
