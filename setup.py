from setuptools import setup

setup(
    name="test01",
    version="0.1.0",
    py_modules=["app", "models"],
    install_requires=[
        "Flask>=2.0",
        "Flask-SQLAlchemy>=3.0",
    ],
)
