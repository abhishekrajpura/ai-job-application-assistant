# AI Job Application Assistant

An intelligent automation system that finds job postings, tailors your resume using AI, and submits applications automatically across multiple job boards. **Now with local LLM support for complete privacy!**

## Features

- 🔍 **Smart Job Scraping**: Automatically finds relevant job postings from multiple platforms
- 🤖 **AI-Powered Resume Tailoring**: Uses LLM to customize your resume for each job
- 🏠 **Local LLM Support**: Complete privacy with Ollama, LM Studio, or Transformers
- 📝 **Automated Applications**: Fills out and submits job applications automatically
- 📊 **Application Tracking**: Monitors application status and success rates
- 🎯 **Intelligent Matching**: Scores job relevance to avoid irrelevant applications
- 🛡️ **Anti-Detection**: Human-like behavior patterns to avoid bot detection

## 🏠 Local LLM Support (NEW!)

Run everything locally for **complete privacy** and **zero API costs**:

- **🔒 Private**: Your data never leaves your machine
- **💰 Free**: No ongoing API subscription fees
- **⚡ Fast**: No network latency once loaded
- **📶 Offline**: Works without internet connection

### Supported Local LLM Options

1. **[Ollama](https://ollama.ai/)** (Recommended) - Easy setup, great performance
2. **[LM Studio](https://lmstudio.ai/)** - User-friendly GUI interface
3. **Transformers** - Direct integration with Hugging Face models

## Quick Start

### Option A: Local LLM Setup (Recommended)

```bash
# 1. Clone and setup
git clone https://github.com/abhishekrajpura/ai-job-application-assistant.git
cd ai-job-application-assistant
./scripts/setup.sh

# 2. Quick local LLM setup
python scripts/setup_local_llm.py

# 3. Test with local LLM
python src/main.py --llm-provider local --dry-run
```

### Option B: Cloud LLM Setup

```bash
# 1. Clone and setup
git clone https://github.com/abhishekrajpura/ai-job-application-assistant.git
cd ai-job-application-assistant
./scripts/setup.sh

# 2. Add API key to .env
echo "OPENAI_API_KEY=your_key_here" >> .env
# OR
echo "ANTHROPIC_API_KEY=your_key_here" >> .env

# 3. Test with cloud LLM
python src/main.py --llm-provider cloud --dry-run
```

## Supported Platforms

- Indeed
- LinkedIn (Coming Soon)
- Glassdoor (Coming Soon)
- Company Career Pages (Coming Soon)

## Installation

### Prerequisites

- Python 3.9 or higher
- Chrome browser (for Selenium)
- 4GB+ RAM (for local LLMs)
- Local LLM software OR OpenAI/Anthropic API key

### Detailed Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhishekrajpura/ai-job-application-assistant.git
   cd ai-job-application-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Choose your LLM setup:**

   **🏠 For Local LLMs (Private & Free):**
   ```bash
   python scripts/setup_local_llm.py
   ```
   
   **☁️ For Cloud LLMs (API-based):**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Configure your resume**
   ```bash
   cp config/master_resume.json.example config/master_resume.json
   # Your resume data is already there!
   ```

## Usage

### Basic Usage
```bash
# Run with local LLM (private)
python src/main.py --llm-provider local

# Run with cloud LLM
python src/main.py --llm-provider cloud

# Run with specific job board
python src/main.py --platform indeed --location "Toronto, ON"

# Dry run (no actual applications)
python src/main.py --dry-run
```

### Local LLM Options
```bash
# Use Ollama (recommended)
python src/main.py --llm-provider local --local-provider ollama --local-model llama2

# Use LM Studio
python src/main.py --llm-provider local --local-provider lmstudio

# Use direct Transformers
python src/main.py --llm-provider local --local-provider transformers
```

### Dashboard
```bash
# Start the monitoring dashboard
streamlit run src/dashboard/app.py
```

## Configuration

### Local LLM Settings (.env)
```bash
# Local LLM Provider
LLM_PROVIDER=local
LOCAL_LLM_PROVIDER=ollama
LOCAL_LLM_MODEL=llama2

# Performance tuning
LOCAL_LLM_TEMPERATURE=0.3
LOCAL_LLM_MAX_TOKENS=2000
```

### Cloud LLM Settings (.env)
```bash
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
LLM_PROVIDER=cloud
```

### Job Preferences (config/job_preferences.yaml)
Configure job search criteria, location preferences, salary ranges, and keywords.

## Project Structure

```
ai-job-application-assistant/
├── src/                    # Main source code
│   ├── scrapers/          # Job scraping modules
│   ├── resume/            # Resume tailoring and generation
│   │   ├── local_llm_tailor.py    # Local LLM integration
│   │   └── resume_tailor.py       # Cloud LLM integration
│   ├── application/       # Application submission logic
│   └── dashboard/         # Monitoring dashboard
├── config/                # Configuration files
├── data/                  # Database and output files
├── docs/                  # Documentation
│   └── LOCAL_LLM_SETUP.md # Detailed local LLM guide
├── tests/                 # Unit tests
└── scripts/               # Utility scripts
    ├── setup_local_llm.py # Local LLM quick setup
    └── test_task2.py      # Resume system tests
```

## Local LLM Performance Guide

### Memory Requirements
- **Small models** (1-3B parameters): 4GB+ RAM
- **Medium models** (7-13B parameters): 8GB+ RAM  
- **Large models** (30B+ parameters): 16GB+ RAM

### Recommended Models
- **Balanced**: `llama2` (4GB) - Good speed and quality
- **Fast**: `microsoft/DialoGPT-medium` (1GB) - Quick responses
- **Quality**: `llama2:13b` (7GB) - Better results, needs more RAM

### Speed Tips
- Use GPU acceleration if available
- Try quantized models (4-bit/8-bit)
- Keep local LLM server running in background

## Development

### Running Tests
```bash
# Test all components
python scripts/test_task2.py

# Test local LLM specifically
python src/resume/local_llm_tailor.py

# Test cloud LLM
python src/resume/resume_tailor.py
```

### Code Formatting
```bash
black src/
flake8 src/
```

### Adding New Job Boards
1. Create a new scraper in `src/scrapers/`
2. Inherit from `BaseScraper`
3. Implement required methods
4. Add configuration in `config/site_configs/`

## Safety & Ethics

- **Respect Rate Limits**: Built-in delays and limits to avoid overwhelming job sites
- **Terms of Service**: Review and comply with each platform's terms
- **Data Privacy**: Local LLMs keep all data on your machine
- **Quality Control**: Manual review options for applications

## Troubleshooting

### Local LLM Issues

1. **"Model not found" error**:
   ```bash
   # For Ollama
   ollama pull llama2
   ```

2. **"Connection refused" error**:
   ```bash
   # Make sure Ollama is running
   ollama serve
   ```

3. **Out of memory errors**:
   - Use a smaller model (DialoGPT-medium instead of Llama2)
   - Close other applications
   - Try quantized models

### General Issues

1. **Browser not found**: Install Chrome or update webdriver
2. **Captcha detected**: Reduce application frequency
3. **Login required**: Check credentials and session management

See `docs/LOCAL_LLM_SETUP.md` for detailed troubleshooting.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes. Users are responsible for complying with job board terms of service and applicable laws. Use responsibly and ethically.

## Support

- 📧 Issues: [GitHub Issues](https://github.com/abhishekrajpura/ai-job-application-assistant/issues)
- 📖 Documentation: [Wiki](https://github.com/abhishekrajpura/ai-job-application-assistant/wiki)
- 🏠 Local LLM Guide: [docs/LOCAL_LLM_SETUP.md](docs/LOCAL_LLM_SETUP.md)
- 💬 Discussions: [GitHub Discussions](https://github.com/abhishekrajpura/ai-job-application-assistant/discussions)

## Roadmap

- [x] Local LLM integration (Ollama, LM Studio, Transformers)
- [x] Cloud LLM support (OpenAI, Anthropic)
- [x] Resume validation and tailoring
- [x] Indeed job scraping
- [ ] LinkedIn integration
- [ ] Glassdoor support
- [ ] Company career page automation
- [ ] Advanced ML for job matching
- [ ] Mobile app dashboard
- [ ] Multi-language support

---

## 🚀 Get Started in 2 Minutes

```bash
git clone https://github.com/abhishekrajpura/ai-job-application-assistant.git
cd ai-job-application-assistant
./scripts/setup.sh
python scripts/setup_local_llm.py
python src/main.py --llm-provider local --dry-run
```

**Enjoy private, free AI-powered job applications!** 🎉