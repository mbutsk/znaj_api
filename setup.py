from setuptools import setup, find_packages



setup(
    name='znaj_api',
    version='0.0.1',
    description='znaj.by API',
    author='mbutsk',
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    zip_safe=False
)