from setuptools import setup, find_packages
setup(
    name = "dnsdiag",
    version = "1.2.2",
	packages = find_packages(),
    install_requires = ['cymruwhois==1.4'],
    dependency_links = [
        "https://github.com/JustinAzoff/python-cymruwhois/archive/a34543335cbef02b1b615e774ce5b6187afb0cc2.zip#egg=cymruwhois-1.4"
    ],

    scripts = ['dnsping.py', 'dnstraceroute.py', 'dnseval.py'],
    classifiers=[
        "Topic :: System :: Networking",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
    ],

    author = "Babak Farrokhi",
    author_email = "babak@farrokhi.net",
    description = "DNS Diagnostics and measurement tools (ping, traceroute)",
    long_description = """
DNSDiag provides a handful of tools to measure and diagnose your DNS
performance and integrity. Using dnsping, dnstraceroute and dnseval tools
you can measure your DNS response quality from delay and loss perspective
as well as tracing the path your DNS query takes to get to DNS server.
""",
    license = "BSD",
    keywords = "dns traceroute ping",
    url = "https://dnsdiag.org/",
)
