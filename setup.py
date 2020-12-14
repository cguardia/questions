#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0',
                'email_validator',
                'Jinja2',
                'pydantic',
                'requests',
                'simpleeval',
                ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3.6', ]

setup(
    author="Carlos de la Guardia",
    author_email='cguardia@yahoo.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description="Questions is a form library that uses the power of SurveyJS for the UI.",
    entry_points={
        'console_scripts': [
            'download_surveyjs=questions.cli:download_surveyjs',
            'list_resources=questions.cli:list_resources',
            'generate_code=questions.cli:generate_code',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='questions',
    name='questions',
    packages=find_packages(include=['questions', 'questions.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cguardia/questions',
    version='0.7.0a4',
    zip_safe=False,
)
