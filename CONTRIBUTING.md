# Contributing to Canvas Toolkit

Thank you for considering contributing! This document provides guidelines for contributing to Canvas Toolkit.

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Git installed
- Canvas LMS account (for testing)
- Canvas API token (for integration testing)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/canvas-toolkit.git
   cd canvas-toolkit
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in editable mode
   ```

4. **Set up your API token**
   ```bash
   # Create .env file (never commit this!)
   echo 'CANVAS_API_TOKEN=your_token_here' > .env
   echo 'CANVAS_BASE_URL=https://your-school.instructure.com' >> .env
   ```

5. **Run tests**
   ```bash
   pytest tests/ -v
   ```

---

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check existing issues to avoid duplicates
- Verify the bug exists in the latest version
- Collect relevant information (Python version, OS, error messages)

**Bug report should include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)
- Python version, OS, Canvas instance (if relevant)

### Suggesting Features

Feature requests should:
- Explain the problem you're trying to solve
- Describe the proposed solution
- Provide use cases or examples
- Consider alternatives you've thought about

**Note:** Features should align with project goals (simple, focused assignment export tool).

### Submitting Code Changes

#### Before You Start
- Check if an issue exists for your change
- Comment on the issue to avoid duplicate work
- For large changes, discuss in an issue first

#### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run full test suite
   pytest tests/ -v

   # Test with real Canvas data
   python test_phase2.py  # Requires Canvas token
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Clear description of your changes"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

---

## Code Style

### Python Style Guide
- Follow PEP 8 conventions
- Use type hints for function signatures
- Maximum line length: 100 characters (not strict)
- Use descriptive variable names

### Documentation
- Add docstrings to all public functions/classes
- Use Google-style docstrings
- Update README.md if adding user-facing features
- Add inline comments for complex logic only

### Example Function
```python
def get_course_assignments(self, course_id: str) -> List[Dict]:
    """
    Fetch all assignments for a specific course.

    Args:
        course_id: Canvas course ID

    Returns:
        List of assignment dictionaries

    Raises:
        CanvasAPIError: If the API request fails
    """
    endpoint = f"/api/v1/courses/{course_id}/assignments"
    return self._make_request(endpoint)
```

---

## Testing Guidelines

### Writing Tests
- Use pytest framework
- Organize tests by module (e.g., `test_html_parser.py`)
- Test both success cases and edge cases
- Mock external API calls where appropriate

### Test Structure
```python
class TestFeatureName:
    """Test suite for FeatureName."""

    def test_basic_functionality(self):
        """Test the happy path."""
        # Arrange
        input_data = ...

        # Act
        result = function_under_test(input_data)

        # Assert
        assert result == expected_output

    def test_edge_case(self):
        """Test handling of edge case."""
        # Test code here
```

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_html_parser.py -v

# With coverage
pytest tests/ --cov=canvas_toolkit --cov-report=html
```

---

## Project Structure

```
canvas-toolkit/
├── canvas_toolkit/          # Main package
│   ├── client/             # Canvas API client
│   ├── models/             # Data models
│   ├── writers/            # Export writers
│   └── utils/              # Utilities (HTML parser, etc.)
├── tests/                  # Unit tests
├── examples/               # Example scripts
├── docs/                   # Documentation
├── canvas_toolkit.py       # Streamlit GUI entry point
├── README.md              # User documentation
├── CONTRIBUTING.md        # This file
├── SECURITY.md            # Security guidelines
└── requirements.txt       # Dependencies
```

---

## Code Review Process

All submissions require review. Pull requests should:
- Pass all tests (automated CI will check)
- Have clear commit messages
- Include tests for new features
- Update documentation if needed
- Be focused (one feature/fix per PR)

**Review criteria:**
- Code quality and style
- Test coverage
- Documentation completeness
- Security considerations
- Performance impact

---

## Adding New Features

### Before You Code
1. Open an issue to discuss the feature
2. Get feedback from maintainers
3. Confirm the feature aligns with project goals

### Implementation Checklist
- [ ] Feature code implemented
- [ ] Unit tests added (aim for >80% coverage)
- [ ] Integration test added (if applicable)
- [ ] Documentation updated (README, docstrings)
- [ ] Example added (if helpful for users)
- [ ] No breaking changes to existing API
- [ ] Security considerations addressed

---

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `test:` Adding or updating tests
- `refactor:` Code change that doesn't fix a bug or add a feature
- `perf:` Performance improvement
- `chore:` Build process or auxiliary tool changes

**Examples:**
```
feat: Add filter for upcoming assignments only

Adds a checkbox in the GUI to show only assignments with
due dates in the future. Keeps assignments with no due date.

Closes #42
```

```
fix: Handle malformed HTML in announcements

HTMLParser now gracefully handles unclosed tags and returns
safe fallback text instead of crashing.
```

---

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- No harassment or discrimination

### Communication
- GitHub Issues: Bug reports, feature requests
- Pull Requests: Code discussions
- Email: Security issues only (see SECURITY.md)

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in the project README

---

## Questions?

If you have questions not covered here:
- Check existing issues/PRs
- Open a new issue with your question
- Be patient - maintainers are volunteers

---

**Thank you for contributing to Canvas Toolkit!**
