# Intelligent system for tracking and filtering market offers

![Python](https://img.shields.io/badge/python-3.14-blue)
![License](https://img.shields.io/badge/license-MIT-green)

The project is built using the Python programming language and makes use of the
Playwright and Ollama libraries.

Its main objective is to connect to platforms that list freelance job openings,
filter through them, and apply to the listings autonomously with the help of
artificial intelligence — in this case, using the Ollama `qwen3:8b` model
locally.

---

## Features
- Automated scraping of freelance job offers.
- Filtering and autonomous application using AI models.
- Configurable to work with different Ollama models.
- Modular design for easy extension to other platforms.

---

## Installation.
1. Download the `qwen3:8b` model locally from Ollama.
Note: the program also works with other models, but you will need to change the
name in the `client_ollama.py` file.

2. Install the necessary libraries:
```Shell
pip install -r requirements.txt
```

---

## Usage.
1. Start the llama model.
2. Run the main script:
```Shell
python workana.py
```

---

## Requirements.
* Locally downloaded Ollama model.
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

## To Do
* Add support for more freelance platforms.
* Improve filtering criteria with NLP.
* Dockerize the project for easier deployment.
* Add unit tests for scraping and filtering modules.

---

## Contributing
Contributions are welcome!
Please fork the repository, create a feature branch, and submit a pull request.
For major changes, open an issue first to discuss what you would like to change.

---

## License
This project is licensed under the MIT License