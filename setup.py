from setuptools import setup

setup(
    name="PurplePi",
    version="0.1.0",
    packages=["purplepi", "purplepi.commands"],
    include_package_data=True,
    install_requires=["click",
        "adafruit-circuitpython-rgb-display",
        "yfinance",
        "lxml",],
    entry_points="""
        [console_scripts]
        purplepi=purplepi.cli:cli
    """,
)
