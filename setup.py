from setuptools import setup, find_packages

setup(
    name="file-tracker",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'colorama>=0.4.6',
        'tabulate>=0.9.0',
        'tqdm>=4.66.1',
        'python-dateutil>=2.8.2',
    ],
    entry_points={
        'console_scripts': [
            'ftrack=ftrack:main',
        ],
    },
    author="Your Name",
    description="A file tracking and management system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="MIT",
) 