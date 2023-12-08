import setuptools

setuptools.setup(
    name="ko2kana",
    version="1.7",
    license='MIT',
    author="kdr",
    author_email="kdrhacker1234@gmail.com",
    description="Korean to Katakana",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kdrkdrkdr/ko2kana",
    packages=setuptools.find_packages(),
    package_data={'': ['*.txt', '*.csv']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'jamo',
        'g2p_en'
    ],
    py_modules = ['ko2kana']
)