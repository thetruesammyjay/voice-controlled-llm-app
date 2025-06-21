from setuptools import setup, find_packages
import os

# Function to read requirements from a file
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Get the list of core dependencies
install_requires = read_requirements('requirements.txt')

# Get the list of development dependencies (optional, but good practice for setup.py)
# This will be used in the 'extras_require' argument
dev_requires = read_requirements('requirements-dev.txt')


setup(
    name='voice-controlled-llm-app',
    version='0.1.0', # Initial version of your application
    author='Samuel Justin Ifiezibe', # Replace with your name
    author_email='sammyjayisthename@gmail.com', # Replace with your email
    description='A multimodal AI application for voice-to-voice conversations with LLMs.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/thetruesammyjay/voice-controlled-llm-app', # Replace with your project's GitHub URL
    packages=find_packages(where='src'), # Automatically find packages in the 'src' directory
    package_dir={'': 'src'}, # Tell setuptools that packages are under 'src'
    include_package_data=True, # Include non-code files (like .txt prompts)
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires, # `pip install .[dev]` will install dev dependencies
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Communications :: Chat',
    ],
    python_requires='>=3.8', # Minimum Python version required
    # Entry points for command-line scripts
    entry_points={
        'console_scripts': [
            'voice-llm-app=main:main', # Maps 'voice-llm-app' command to src/main.py's main function
            # Note: This assumes main.py is directly importable.
            # If main.py is deeper, you might need:
            # 'voice-llm-app=src.main:main',
        ],
    },
)

