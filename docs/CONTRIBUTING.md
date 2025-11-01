# Contributing to Fintech AI System

Thank you for your interest in contributing to the Fintech AI System! This document provides guidelines and best practices for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers have the right to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned with this Code of Conduct.

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- Code editor (VS Code recommended)
- Basic knowledge of React, FastAPI, and ML

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/fintech-ai-system.git
   cd fintech-ai-system
   ```
3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/fintech-ai-system.git
   ```

### Set Up Development Environment

**Backend Setup:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

**Verify Setup:**
```bash
# Run tests
pytest tests/

# Run backend
python run_api.py

# In another terminal, run frontend
cd frontend && npm run dev
```

## Development Workflow

### 1. Create a Feature Branch

```bash
# Fetch latest changes
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features (e.g., `feature/add-portfolio-tracking`)
- `fix/` - Bug fixes (e.g., `fix/sentiment-calculation-error`)
- `docs/` - Documentation (e.g., `docs/update-api-guide`)
- `refactor/` - Code refactoring (e.g., `refactor/database-layer`)
- `test/` - Adding tests (e.g., `test/add-signal-generator-tests`)

### 2. Make Changes

**Code Style:**
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Write clear, descriptive variable names
- Add comments for complex logic
- Keep functions small and focused

**Commit Messages:**
```bash
# Good commit messages
git commit -m "Add portfolio tracking feature with React components"
git commit -m "Fix sentiment score calculation for edge cases"
git commit -m "Update API documentation with new endpoints"

# Bad commit messages (avoid these)
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "WIP"
```

Commit message format:
```
<type>: <subject>

<body>

<footer>
```

Example:
```
feat: Add portfolio tracking dashboard

- Create Portfolio component with holdings table
- Add API endpoint for portfolio CRUD operations
- Implement real-time P&L calculations
- Add portfolio analytics charts

Closes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 3. Write Tests

**All new features must include tests:**

```python
# Example: tests/test_new_feature.py
import pytest
from your_module import YourClass

class TestYourFeature:
    def test_basic_functionality(self):
        """Test basic feature works correctly."""
        result = YourClass().method()
        assert result == expected_value

    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            YourClass().method(invalid_input)
```

**Test Coverage:**
- Aim for >80% code coverage
- Test happy path and edge cases
- Test error handling
- Test with various data types

**Run Tests:**
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=agents --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_sentiment.py

# Run specific test
pytest tests/test_sentiment.py::TestSentimentAnalyzer::test_positive_sentiment
```

### 4. Update Documentation

If your changes affect:
- **API endpoints** → Update `docs/API.md`
- **System architecture** → Update `docs/ARCHITECTURE.md`
- **Deployment** → Update `docs/DEPLOYMENT.md`
- **User-facing features** → Update `README.md`

### 5. Format and Lint Code

**Python:**
```bash
# Format with black
black agents/ backend/ tests/

# Lint with flake8
flake8 agents/ backend/ tests/

# Type checking with mypy
mypy agents/ backend/
```

**JavaScript:**
```bash
cd frontend

# Format with prettier
npm run format

# Lint with eslint
npm run lint
```

### 6. Push Changes

```bash
git push origin feature/your-feature-name
```

## Coding Standards

### Python Style Guide

**PEP 8 Compliance:**
```python
# Good
def calculate_sentiment_score(text: str) -> float:
    """
    Calculate sentiment score from text.

    Args:
        text: Input text to analyze

    Returns:
        Sentiment score between -1 and 1
    """
    # Implementation
    pass

# Bad
def calc(t):
    # No docstring, unclear names
    pass
```

**Docstrings:**
- Use Google-style docstrings
- Include type hints
- Document all public functions, classes, and modules
- Include examples for complex functions

**Example:**
```python
def analyze_earnings(
    ticker: str,
    transcript: str,
    include_signals: bool = True
) -> Dict[str, Any]:
    """
    Analyze earnings call transcript with sentiment and macro regime.

    This function orchestrates the full analysis pipeline including
    sentiment analysis, macro regime detection, and trading signal
    generation.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        transcript: Full earnings call transcript text
        include_signals: Whether to generate trading signals

    Returns:
        Dictionary containing analysis results with keys:
        - sentiment: Sentiment analysis results
        - macro: Macro regime classification
        - signals: Trading signals (if include_signals=True)

    Raises:
        ValueError: If ticker is invalid
        AnalysisError: If analysis pipeline fails

    Example:
        >>> result = analyze_earnings("AAPL", transcript_text)
        >>> print(result['sentiment']['overall_label'])
        'positive'
    """
    pass
```

**Type Hints:**
```python
from typing import List, Dict, Optional, Tuple, Any

def process_data(
    items: List[str],
    config: Dict[str, Any],
    max_items: Optional[int] = None
) -> Tuple[List[Dict], int]:
    """Process data with type hints."""
    pass
```

### JavaScript Style Guide

**ES6+ Features:**
```javascript
// Good: Use const/let, arrow functions, destructuring
const analyzeData = async (ticker) => {
  const { data } = await api.analyze(ticker);
  return data;
};

// Bad: Use var, old function syntax
var analyzeData = function(ticker) {
  api.analyze(ticker, function(data) {
    return data;
  });
};
```

**React Best Practices:**
```javascript
// Good: Functional components with hooks
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  return <div>{/* ... */}</div>;
}

// Good: PropTypes or TypeScript
Dashboard.propTypes = {
  ticker: PropTypes.string.isRequired,
  onAnalyze: PropTypes.func
};
```

### Database Conventions

**SQL Style:**
```sql
-- Good: Clear, formatted SQL
CREATE TABLE IF NOT EXISTS companies (
    ticker TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    sector TEXT,
    market_cap REAL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Use parameterized queries
cursor.execute(
    "INSERT INTO companies (ticker, name) VALUES (?, ?)",
    (ticker, name)
)
```

### API Design

**RESTful Conventions:**
- Use plural nouns for resources (`/companies`, not `/company`)
- Use HTTP methods correctly (GET, POST, PUT, DELETE)
- Return proper status codes
- Include pagination for list endpoints
- Version your API (`/v1/analyze`)

**Example:**
```python
@app.get("/companies", response_model=CompanyList)
async def list_companies(
    limit: int = 10,
    offset: int = 0,
    sector: Optional[str] = None
):
    """
    Get list of companies with pagination.

    Query params:
    - limit: Number of results (default 10, max 100)
    - offset: Pagination offset (default 0)
    - sector: Filter by sector (optional)
    """
    # Implementation
    pass
```

## Testing

### Test Structure

Organize tests to mirror source code:
```
tests/
├── conftest.py           # Shared fixtures
├── test_sentiment.py     # agents/sentiment_analyzer.py
├── test_macro.py         # agents/macro_detector.py
├── test_orchestrator.py  # backend/orchestrator.py
├── test_api.py          # API endpoint tests
└── test_database.py     # backend/database.py
```

### Writing Good Tests

**AAA Pattern (Arrange, Act, Assert):**
```python
def test_sentiment_analysis():
    # Arrange
    analyzer = SentimentAnalyzer()
    text = "Revenue grew 20% year over year."

    # Act
    result = analyzer.analyze(text)

    # Assert
    assert result['label'] == 'positive'
    assert result['confidence'] > 0.8
```

**Test Isolation:**
```python
@pytest.fixture
def temp_database():
    """Create temporary database for testing."""
    db_path = tempfile.mktemp(suffix='.db')
    db = Database(db_path)
    db.create_tables()

    yield db

    # Cleanup
    db.close()
    os.remove(db_path)
```

**Mocking External APIs:**
```python
from unittest.mock import patch

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'data': 'test'}
    result = fetch_data()
    assert result == {'data': 'test'}
```

### Test Categories

**Unit Tests:**
- Test individual functions/classes
- Mock external dependencies
- Fast execution (<1ms per test)

**Integration Tests:**
- Test multiple components together
- Use real database (temporary)
- Test API endpoints
- Medium speed (~100ms per test)

**End-to-End Tests:**
- Test complete user workflows
- Use real services
- Slower execution (~1s per test)

### Running Tests Locally

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov --cov-report=html

# Run specific category
pytest tests/ -m unit
pytest tests/ -m integration

# Run in parallel (faster)
pytest tests/ -n auto

# Watch mode (re-run on changes)
pytest-watch tests/
```

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] All tests pass locally
- [ ] Added tests for new features
- [ ] Updated documentation
- [ ] Commit messages are clear
- [ ] No merge conflicts with main
- [ ] Code is self-documenting or well-commented

### Creating Pull Request

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub:**
   - Go to your fork on GitHub
   - Click "Compare & pull request"
   - Fill out the PR template

3. **PR Title Format:**
   ```
   [Type] Brief description of changes
   ```

   Examples:
   - `[Feature] Add portfolio tracking dashboard`
   - `[Fix] Resolve sentiment calculation edge case`
   - `[Docs] Update API documentation for new endpoints`

4. **PR Description Template:**
   ```markdown
   ## Description
   Brief description of what this PR does and why.

   ## Changes Made
   - Change 1
   - Change 2
   - Change 3

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Integration tests added/updated
   - [ ] Manual testing completed

   ## Screenshots (if applicable)
   [Add screenshots of UI changes]

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Tests pass locally
   - [ ] Documentation updated
   - [ ] No breaking changes (or documented if needed)

   ## Related Issues
   Closes #123
   Fixes #456
   ```

### Code Review Process

1. **Automated Checks:**
   - Tests must pass (CI/CD)
   - Linting must pass
   - Code coverage maintained (>80%)

2. **Human Review:**
   - At least one maintainer approval required
   - Address all review comments
   - Keep discussions constructive

3. **Review Timeline:**
   - Initial review within 2-3 business days
   - Follow-up reviews within 1-2 business days
   - Stale PRs closed after 30 days of inactivity

### Responding to Feedback

**Be receptive:**
```markdown
# Good response
Thanks for the feedback! I've updated the code to use
dependency injection as you suggested. Much cleaner now.

# Polite disagreement (if needed)
I see your point about refactoring this. However, I think
the current approach is clearer because [reason]. What do
you think about [alternative]?
```

### After Approval

1. **Squash commits** (if requested)
2. **Rebase on main** (if needed)
3. **Maintainer will merge** your PR
4. **Delete your branch** after merge

## Issue Guidelines

### Reporting Bugs

**Use the bug template:**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.11.5]
- Node version: [e.g., 18.17.0]
- Browser: [e.g., Chrome 115]

## Screenshots/Logs
[Add relevant screenshots or error logs]

## Additional Context
Any other relevant information
```

### Requesting Features

**Use the feature template:**
```markdown
## Feature Description
Clear description of the proposed feature

## Problem It Solves
What problem does this solve for users?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Other ways to solve this problem

## Additional Context
Mockups, examples, research, etc.
```

### Good Issue Titles

```
# Good
- "Sentiment analyzer fails on transcripts >10,000 characters"
- "Add export to Excel functionality for analytics dashboard"
- "API returns 500 error when FRED API key is invalid"

# Bad
- "It doesn't work"
- "Feature request"
- "Help!"
```

## Community

### Communication Channels

- **GitHub Issues:** Bug reports and feature requests
- **GitHub Discussions:** Questions and community discussions
- **Discord:** Real-time chat and support
- **Email:** security@yourdomain.com (for security issues only)

### Getting Help

**Before asking:**
1. Check existing issues and discussions
2. Read the documentation
3. Search Stack Overflow

**When asking:**
1. Be specific about the problem
2. Include error messages and logs
3. Share relevant code snippets
4. Describe what you've tried

### Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Given credit in documentation
- Invited to contributor meetings (for significant contributions)

## Development Tips

### Useful Commands

```bash
# Backend
python run_api.py          # Start API server
pytest tests/              # Run tests
black agents/ backend/     # Format code
flake8 agents/ backend/    # Lint code

# Frontend
npm run dev               # Start dev server
npm run build             # Build for production
npm run lint              # Lint code
npm test                  # Run tests

# Database
python -c "from backend.database import Database; db = Database(); db.create_tables()"

# Git
git fetch upstream        # Get latest changes
git rebase upstream/main  # Rebase on main
git log --oneline -10     # View recent commits
```

### Debugging

**Backend:**
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use VS Code debugger
# Set breakpoint, press F5
```

**Frontend:**
```javascript
// Use browser DevTools
console.log('Debug:', data);
debugger;  // Pauses execution
```

### Common Issues

**"ModuleNotFoundError"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Port already in use"**
```bash
# Kill process on port
lsof -ti:8000 | xargs kill -9
```

**"Tests failing locally"**
```bash
# Clean test artifacts
pytest --cache-clear
rm -rf .pytest_cache __pycache__
```

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Questions?

Feel free to reach out:
- Open a discussion on GitHub
- Join our Discord server
- Email: contributors@yourdomain.com

Thank you for contributing to Fintech AI System!
