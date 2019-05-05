from setuptools import setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='jsons',
    version='0.1.0',
    author='Ramon Hagenaars',
    author_email='ramon.hagenaars@gmail.com',
    description='Dependency injection for Python',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/ramonhagenaars/jacked',
    packages=[
        'jacked',
    ],
    test_suite='tests',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)