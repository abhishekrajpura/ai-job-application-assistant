from setuptools import setup, find_packages

setup(
    name="ai-job-application-assistant",
    version="1.0.0",
    description="Automated job application system with AI-powered resume tailoring",
    author="Abhishek Rajpura",
    author_email="abhishekrajpura3@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "selenium>=4.15.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
        "openai>=1.3.0",
        "pandas>=2.1.0",
        "pyyaml>=6.0.0",
        "python-dotenv>=1.0.0",
        "streamlit>=1.28.0",
    ],
    entry_points={
        "console_scripts": [
            "job-bot=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)