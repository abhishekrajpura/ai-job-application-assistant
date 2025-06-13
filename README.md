# AI Job Application Assistant

An intelligent automation system that finds job postings, tailors your resume using AI, and submits applications automatically across multiple job boards.

## Features

- 🔍 **Smart Job Scraping**: Automatically finds relevant job postings from multiple platforms
- 🤖 **AI-Powered Resume Tailoring**: Uses LLM to customize your resume for each job
- 📝 **Automated Applications**: Fills out and submits job applications automatically
- 📊 **Application Tracking**: Monitors application status and success rates
- 🎯 **Intelligent Matching**: Scores job relevance to avoid irrelevant applications
- 🛡️ **Anti-Detection**: Human-like behavior patterns to avoid bot detection

## Supported Platforms

- Indeed
- LinkedIn (Coming Soon)
- Glassdoor (Coming Soon)
- Company Career Pages (Coming Soon)

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Chrome browser (for Selenium)
- OpenAI API key or Anthropic API key

### Installation

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

4. **Set up configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and preferences
   ```

5. **Configure your master resume**
   ```bash
   cp config/master_resume.json.example config/master_resume.json
   # Edit with your resume information
   ```

6. **Run the setup script**
   ```bash
   python scripts/setup.py
   ```

### Usage

#### Basic Usage
```bash
# Run the job application bot
python src/main.py

# Run with specific job board
python src/main.py --platform indeed

# Run with custom filters
python src/main.py --location "Toronto, ON" --keywords "data analyst"
```

#### Dashboard
```bash
# Start the monitoring dashboard
streamlit run src/dashboard/app.py
```

#### Configuration

Edit `config/job_preferences.yaml` to customize:
- Job search criteria
- Application limits
- Filtering preferences
- Resume tailoring settings

## Project Structure

```
ai-job-application-assistant/
├── src/                    # Main source code
│   ├── scrapers/          # Job scraping modules
│   ├── resume/            # Resume tailoring and generation
│   ├── application/       # Application submission logic
│   └── dashboard/         # Monitoring dashboard
├── config/                # Configuration files
├── data/                  # Database and output files
├── tests/                 # Unit tests
└── scripts/               # Utility scripts
```

## Configuration

### Environment Variables (.env)
```bash
# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Database
DATABASE_URL=sqlite:///data/jobs.db

# Application Settings
MAX_APPLICATIONS_PER_DAY=50
DELAY_BETWEEN_APPLICATIONS=300  # seconds

# Browser Settings
HEADLESS_BROWSER=true
BROWSER_TIMEOUT=30
```

### Master Resume (config/master_resume.json)
Your master resume should be in JSON format as shown in the examples. This serves as the source of truth for all tailored resumes.

### Job Preferences (config/job_preferences.yaml)
Configure job search criteria, location preferences, salary ranges, and keywords.

## Development

### Running Tests
```bash
pytest tests/
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
- **Data Privacy**: Secure handling of personal information
- **Quality Control**: Manual review options for applications

## Troubleshooting

### Common Issues

1. **Browser not found**: Install Chrome or update webdriver
2. **Captcha detected**: Reduce application frequency
3. **Login required**: Check credentials and session management
4. **Rate limited**: Increase delays between requests

See `docs/TROUBLESHOOTING.md` for detailed solutions.

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
- 💬 Discussions: [GitHub Discussions](https://github.com/abhishekrajpura/ai-job-application-assistant/discussions)

## Roadmap

- [ ] LinkedIn integration
- [ ] Glassdoor support
- [ ] Company career page automation
- [ ] Advanced ML for job matching
- [ ] Mobile app dashboard
- [ ] Multi-language support