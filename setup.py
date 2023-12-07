import setuptools

setuptools.setup(
    name="ko2kana",
    version="1.3",
    license='MIT',
    author="kdr",
    author_email="kdrhacker1234@gmail.com",
    description="Korean to Katakana",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kdrkdrkdr/ko2kana",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'g2pk2',
        'jamo',
        'cmake',
        'jaconv',
        'pyopenjtalk',
        'g2pk2',
    ],
    py_modules = ['ko2kana']
)