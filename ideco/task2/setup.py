from setuptools import setup, find_packages


setup(
    name="port_scanner_srv",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["aiodns~=2.0.0", "aiohttp>=3.2.0"],
    data_files=[("", ["LICENSE"])],
    author="Konstantin Shevchenko",
    author_email="kos.shevchenko@gmail.com",
    license="MIT",
    description="Simple REST API server witch realizes port scanner.",
    long_description="Simple REST API server witch realizes port scanner.\n"
                     "input:\"GET /<hostname or ip>/<start port>/<end port>\"\n"
                     "JSON output: [{\"port\": integer, \"state\": \"(open|close)\"}]",
    keywords="simple port scanner asyncio REST API server aiohttp",
    url="https://github.com/Konstantin-Sh/interview_tasks/tree/master/ideco/task2",
    classifie=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)