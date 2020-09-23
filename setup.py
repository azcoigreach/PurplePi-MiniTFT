from setuptools import setup

setup(
    name="PurplePi",
    version="0.0.1",
    packages=["purplepi", "purplepi.commands"],
    include_package_data=True,
    install_requires=["click",
        "pyfiglet",
        "yfinance",],
    entry_points="""
        [console_scripts]
        purplepi=purplepi.cli:cli
    """,
)
