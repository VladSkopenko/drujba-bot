from setuptools import setup, find_packages

setup(
    name='bot_drujba',
    version='1.0.0',
    description="Bot assistant",
    url="https://github.com/artemLink/drujba",
    author="Drujba team",
    packages=find_packages(),
    package_dir={'drujba': 'drujba'},
    install_requires=[
        'rich',
        'art',
        'prompt_toolkit',
        'colorama',
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            "go_drujba = drujba.account:start",
        ],
    },
)