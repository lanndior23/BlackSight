from setuptools import setup, find_packages

setup(
    name="blacksight",
    version="5.0.0",
    author="lanndior",
    description="Advanced Terminal-Based Ethical Hacking Toolkit",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        'console_scripts': ['blacksight=main:main']
    },
    include_package_data=True,
)
