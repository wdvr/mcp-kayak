from setuptools import setup, find_packages

setup(
    name="mcp_kayak",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastmcp",
        "fastapi",
        "python-dotenv",
        "httpx",
    ],
    python_requires=">=3.10",
)
