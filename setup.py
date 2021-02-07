from setuptools import setup

setup(name="polifonia_app",
      version="0.0.1",
      description="Backend for the polyphony webApp",
      author="Timofey Kazantsev",
      author_email="pianoist@ya.ru",
      license="GNU GPLv3",
      classifiers=["Programming Language :: Python :: 3"],
      packages=['polifonia_app'],
      install_requires=[
          'flask',
          'flask-wtf',
          'transliterate',
      ],
      python_requires=">=3.7")
