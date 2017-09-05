from setuptools import setup, find_packages

tests_require = ('pytest', 'pytest-cov', 'codecov', 'mock')
docs_require = ('sphinx', 'sphinx-autobuild', 'sphinx_rtd_theme')

setup(
    name='snippy',
    version='0.1.0',
    author='Heikki J. Laaksonen',
    author_email='laaksonen.heikki.j@gmail.com',
    url='https://github.com/heilaaks/snippy',
    description='A small command line tool to manage command and troubleshooting examples.',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console'
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
        'Topic :: Utilities'
    ],
    keywords='cli code command troubleshooting manager',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'snippy = snip:main'
        ],
    },
    install_requires=[],
    extras_require={
        'dev': tests_require + docs_require,
        'test': tests_require,
    },
    tests_require=tests_require,
    test_suite='tests'
)
