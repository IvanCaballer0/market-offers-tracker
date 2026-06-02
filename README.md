# Intelligent system for tracking and filtering market offers

# Intelligent System for Tracking and Filtering Market Offers

![Python](https://img.shields.io/badge/python-3.14-blue)
![Playwright](https://img.shields.io/badge/playwright-v1.44-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple)
![License](https://img.shields.io/badge/license-MIT-green)

An autonomous, AI-driven web scraping and job application assistant. The system connects to freelance platforms, parses detailed job listings using Playwright, and leverages Local or Cloud-hosted Large Language Models (LLMs) to evaluate project viability and draft custom, context-aware proposals.

---

## Features
- **Automated Deep Scraping:** Navigates natively through job search results, bypassing dynamic pagination and dynamic content rendering via Playwright.
- **AI-Powered Viability Assessment:** Evaluates multi-layered job specifications (budgets, raw text description, required skills) against a predefined freelancer profile.
- **Dynamic Proposal Generation:** Automatically drafts customized technical proposals, setting realistic milestones and calculating budget estimations under a strict financial threshold.
- **Hybrid LLM Support:** Seamlessly switches between local execution (Ollama) for zero-cost, private inference, and cloud infrastructure (NVIDIA NIM) for high-performance reasoning.
- **Persistent Session Management:** Employs persistent browser contexts to safely reuse authentication states, diminishing bot-detection risks.

---

## Project Structure
- `workana.py` → Core application script and browser automation engine.
- `client_ollama.py` → Integration wrapper for locally hosted Ollama models.
- `requirements.txt` → Production and development dependencies.
- `.env` → Local environment configuration variables (Git ignored).
- `.gitignore` → System specification files and secure environment boundaries.

---

## Installation & Setup

1. Environment Cloning & Dependencies
First, clone the repository and install the required Python packages along with the Playwright browser binaries:

```shell
# Install python packages
pip install -r requirements.txt
```

```shell
# Install required browser binaries for Playwright
playwright install
```

### If you want to use the script with a locally hosted model.
2. Create an `.env` file in the script’s root directory with the variables `EMAIL` and `PASSWORD` (credentials for the page where the ad is published).
3. Download the `qwen3:8b` model locally from Ollama.
NOTE: The program also works with other models, but you will need to change the model name in the `client_ollama.py` file.
4. Start Ollama and do not close it.
5. Use the command:
```
python workana.py -model=“local”
```

### If you want to use the script with a model hosted in the cloud.
2. Create a .env file in the script’s root directory with the variables EMAIL, PASSWORD (credentials for the page where the ad is published), and NVIDIA_API.
3. Create an account at (https://build.nvidia.com/)[https://build.nvidia.com/] and generate an API Key.
4. Paste the API Key into the .env file generated in step 1 and use the NVIDIA_API variable.
NOTE: By default, the script uses the “qwen/qwen3-coder-480b-a35b-instruct” model. If you want to use a different one, you can change the name in the “client_nvidia.py” file.
5. Use the command. 
```
python workana.py -model=“cloud”
```

---

## Requirements.
* A locally downloaded Ollama model or an NVIDIA API key.
* Python version 3.14 or later.

---

## Project structure.
- workana.py → Main script
- client_ollama.py → Ollama client integration
- requirements.txt → Dependencies
- README.md → Documentation
- .env → Environment variables (ignored by Git)
- .gitignore → Git ignore rules
- .venv/ → Virtual environment (ignored)

---

## Contributing
Contributions are welcome!
Please fork the repository, create a feature branch, and submit a pull request.
For major changes, open an issue first to discuss what you would like to change.

---

## License
Distributed under the MIT License. See LICENSE for more information.