from setuptools import setup

setup(
    name='jiranator',
    version='1.0.0',
    author='Your Name',
    description='jiranator - CLI tool for interacting with Jira',
    packages=['jiranator'],
    entry_points={
        'console_scripts': [
            'jiranator = jiranator.__main__:main'
        ]
    }
)
