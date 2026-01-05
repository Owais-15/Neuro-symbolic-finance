# Contributing to Neuro-Symbolic Stock Predictor

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🎯 Ways to Contribute

- **Bug Reports**: Open an issue describing the bug and how to reproduce it
- **Feature Requests**: Suggest new features via GitHub issues
- **Code Contributions**: Submit pull requests with improvements
- **Documentation**: Help improve docs, add examples, fix typos
- **Testing**: Add unit tests, improve test coverage

## 🚀 Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/Neuro-symbolic-finance.git
cd Neuro-symbolic-finance
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Tests
```bash
pytest tests/ -v
```

## 📝 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Write clean, readable code
- Follow existing code style
- Add docstrings to functions
- Update tests if needed

### 3. Test Your Changes
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_technical_indicators.py -v

# Check code coverage
pytest --cov=src tests/
```

### 4. Commit
```bash
git add .
git commit -m "feat: add your feature description"
```

**Commit Message Format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding tests
- `refactor:` Code refactoring

### 5. Push and Create PR
```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

## 🧪 Testing Guidelines

- All new features must include tests
- Maintain or improve test coverage
- Tests should be deterministic (no random failures)
- Use descriptive test names

Example:
```python
def test_rsi_bounds():
    """Test that RSI is always between 0 and 100"""
    prices = pd.Series(range(100, 150))
    rsi = calculate_rsi(prices)
    assert 0 <= rsi <= 100
```

## 📚 Documentation Guidelines

- Update README.md if adding new features
- Add docstrings to all functions
- Include examples in docstrings
- Update relevant docs in `docs/` folder

Example docstring:
```python
def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
    """
    Calculate Relative Strength Index.
    
    Args:
        prices: Series of closing prices
        period: Lookback period (default: 14)
        
    Returns:
        RSI value between 0 and 100
        
    Example:
        >>> prices = pd.Series([100, 102, 101, 103])
        >>> rsi = calculate_rsi(prices)
        >>> print(f"RSI: {rsi:.2f}")
    """
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Minimal code to reproduce
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: Python version, OS, dependencies

Example:
```markdown
**Bug**: RSI calculation returns NaN for short price series

**Steps to Reproduce**:
```python
prices = pd.Series([100, 101, 102])
rsi = calculate_rsi(prices, period=14)
print(rsi)  # Returns NaN
```

**Expected**: Should return a valid RSI or raise informative error

**Environment**: Python 3.10, Windows 11
```

## 💡 Feature Requests

When suggesting features:

1. **Use Case**: Explain why this feature is needed
2. **Proposed Solution**: How it should work
3. **Alternatives**: Other approaches you considered

## ⚖️ Code of Conduct

Please be respectful and constructive. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## 🙏 Questions?

- Open a GitHub issue for technical questions
- Check existing issues and documentation first
- Be patient and respectful

Thank you for contributing! 🚀
