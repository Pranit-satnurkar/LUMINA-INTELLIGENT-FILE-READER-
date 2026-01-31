# Contributing to LUMINA

Thank you for your interest in contributing to LUMINA! 🎉 We welcome contributions from the community and are grateful for your support.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## 🤝 Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- **Be respectful**: Treat everyone with respect and kindness
- **Be collaborative**: Work together and help each other
- **Be inclusive**: Welcome newcomers and diverse perspectives
- **Be professional**: Keep discussions focused and constructive

---

## 🚀 How Can I Contribute?

### Reporting Bugs

If you find a bug, please create an issue with:

- **Clear title**: Describe the issue concisely
- **Steps to reproduce**: Detailed steps to recreate the bug
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: OS, Python version, Node version, etc.
- **Screenshots**: If applicable

### Suggesting Features

We love new ideas! To suggest a feature:

- **Check existing issues**: Avoid duplicates
- **Describe the feature**: What problem does it solve?
- **Provide examples**: How would it work?
- **Consider alternatives**: Are there other solutions?

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

---

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Virtual environment tool (venv, conda, etc.)

### Backend Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/LUMINA-INTELLIGENT-FILE-READER-.git
cd LUMINA-INTELLIGENT-FILE-READER-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run tests
pytest

# Start development server
uvicorn backend.main:app --reload
```

### Mobile App Setup

```bash
# Navigate to mobile app
cd mobile-app

# Install dependencies
npm install

# Start Expo
npx expo start
```

---

## 📝 Coding Standards

### Python (Backend)

- **Style Guide**: Follow [PEP 8](https://pep8.org/)
- **Formatting**: Use `black` for code formatting
- **Linting**: Use `flake8` for linting
- **Type Hints**: Use type hints where appropriate
- **Docstrings**: Use Google-style docstrings

```python
def process_document(file_path: str, chunk_size: int = 1000) -> list[str]:
    """
    Process a document and split it into chunks.
    
    Args:
        file_path: Path to the document file
        chunk_size: Size of each chunk in characters
        
    Returns:
        List of text chunks
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Implementation here
    pass
```

### JavaScript (Mobile App)

- **Style Guide**: Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **Formatting**: Use `prettier` for code formatting
- **Linting**: Use `eslint` for linting
- **Components**: Use functional components with hooks
- **Naming**: Use PascalCase for components, camelCase for functions

```javascript
// Good
const ChatMessage = ({ message, timestamp }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <View>
      <Text>{message}</Text>
    </View>
  );
};
```

### File Organization

- Keep files focused and single-purpose
- Use meaningful file and variable names
- Group related functionality together
- Avoid deep nesting (max 3-4 levels)

---

## 📦 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Feature
feat(backend): add support for DOCX files

# Bug fix
fix(mobile): resolve PDF upload crash on Android

# Documentation
docs: update installation instructions

# Refactoring
refactor(bot): simplify RAG pipeline logic
```

---

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**: Sync with the main repository
2. **Create a branch**: Use a descriptive name
   ```bash
   git checkout -b feat/add-ocr-support
   ```
3. **Make changes**: Follow coding standards
4. **Test thoroughly**: Ensure all tests pass
5. **Update documentation**: If needed
6. **Commit changes**: Follow commit guidelines

### Submitting PR

1. **Push to your fork**
   ```bash
   git push origin feat/add-ocr-support
   ```

2. **Create Pull Request** on GitHub with:
   - **Clear title**: Describe the change
   - **Description**: Explain what and why
   - **Related issues**: Link to issues (e.g., "Fixes #123")
   - **Screenshots**: If UI changes
   - **Testing**: How you tested the changes

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] All tests pass
   - [ ] Added new tests
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No new warnings
   ```

### Review Process

- Maintainers will review your PR
- Address feedback promptly
- Keep discussions professional
- Be patient - reviews take time

---

## 🧪 Testing Guidelines

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_bot.py
```

### Writing Tests

```python
import pytest
from backend.bot import create_rag_chain

def test_rag_chain_creation():
    """Test RAG chain is created successfully."""
    chain = create_rag_chain()
    assert chain is not None
    
def test_document_processing():
    """Test document processing with sample PDF."""
    result = process_pdf("tests/fixtures/sample.pdf")
    assert len(result) > 0
```

### Mobile App Tests

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

---

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Explain complex logic with inline comments
- Keep comments up-to-date with code changes

### README Updates

- Update README.md if you add features
- Add examples for new functionality
- Update tech stack if dependencies change

### API Documentation

- Document new API endpoints
- Include request/response examples
- Note any breaking changes

---

## 🎯 Areas for Contribution

We especially welcome contributions in these areas:

- 🔍 **OCR Support**: Add support for scanned PDFs
- 📄 **File Formats**: Support for DOCX, TXT, etc.
- 🌐 **Internationalization**: Multi-language support
- 🎨 **UI/UX**: Mobile app improvements
- 🧪 **Testing**: Increase test coverage
- 📖 **Documentation**: Improve guides and examples
- ⚡ **Performance**: Optimization opportunities
- 🔒 **Security**: Security enhancements

---

## 💬 Questions?

- **Issues**: Open an issue for questions
- **Discussions**: Use GitHub Discussions for general topics
- **Email**: Contact maintainers for private matters

---

## 🙏 Thank You!

Every contribution, no matter how small, is valuable. Thank you for helping make LUMINA better!

---

<div align="center">
  <p>Made with ❤️ by the LUMINA community</p>
</div>
