# Contributing to SIMGuard

Thank you for your interest in contributing to SIMGuard! This document provides guidelines for contributing to this final year cybersecurity project.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, browser)
   - Screenshots if applicable

### Suggesting Enhancements

1. **Check if the enhancement already exists** in issues or discussions
2. **Describe the enhancement** clearly with use cases
3. **Explain why this enhancement would be useful** to the project
4. **Consider the scope** - keep suggestions focused and achievable

### Code Contributions

#### Getting Started

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/SIMGuard.git
cd SIMGuard
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Set up development environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Development Guidelines

##### Backend (Python/Flask)

- **Follow PEP 8** style guidelines
- **Add docstrings** to all functions and classes
- **Include type hints** where appropriate
- **Write unit tests** for new functionality
- **Update API documentation** if adding new endpoints

Example:
```python
def analyze_user_behavior(user_data: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Analyze user behavior for suspicious SIM swap activities.
    
    Args:
        user_data: DataFrame containing all records for a specific user
        
    Returns:
        List of suspicious activities with details
    """
    # Implementation here
```

##### Frontend (HTML/CSS/JavaScript)

- **Use semantic HTML** elements
- **Follow CSS naming conventions** (BEM methodology preferred)
- **Write clean, commented JavaScript**
- **Ensure responsive design** works on all devices
- **Test cross-browser compatibility**

Example:
```javascript
/**
 * Analyze uploaded file using backend API
 * @returns {Promise<void>}
 */
async function analyzeFile() {
    // Implementation here
}
```

#### Testing

##### Backend Testing
```bash
cd backend
python test_api.py
```

##### Frontend Testing
- Test in multiple browsers (Chrome, Firefox, Safari, Edge)
- Verify responsive design on different screen sizes
- Test file upload with various CSV formats
- Validate error handling scenarios

#### Commit Guidelines

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(backend): add new detection algorithm for device fingerprinting
fix(frontend): resolve chart rendering issue on mobile devices
docs(api): update endpoint documentation with new parameters
```

#### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update the README** if necessary
5. **Create a detailed pull request description**

Pull Request Template:
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Other (please describe)

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## 🔧 Development Setup

### Prerequisites
- Python 3.8+
- Git
- Modern web browser
- Text editor/IDE

### Local Development

1. **Clone and setup**
```bash
git clone https://github.com/yourusername/SIMGuard.git
cd SIMGuard
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Run backend**
```bash
python app.py
```

3. **Open frontend**
Open `index.html` in your browser

### Project Structure
```
SIMGuard/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── test_api.py        # API tests
│   ├── run.py             # Startup script
│   └── uploads/           # File upload directory
├── index.html             # Frontend main page
├── styles.css             # Frontend styles
├── script.js              # Frontend JavaScript
├── sample_logs.csv        # Sample data
├── README.md              # Project documentation
├── CONTRIBUTING.md        # This file
└── .gitignore            # Git ignore rules
```

## 🎯 Areas for Contribution

### High Priority
- **Machine Learning Integration**: Replace mock detection with real ML models
- **Database Support**: Add persistent data storage
- **User Authentication**: Implement user management system
- **Real-time Monitoring**: Add live data streaming capabilities

### Medium Priority
- **Advanced Visualizations**: Enhanced charts and graphs
- **Export Formats**: Additional report formats (Excel, JSON)
- **API Rate Limiting**: Implement request throttling
- **Logging Improvements**: Enhanced logging and monitoring

### Low Priority
- **UI/UX Enhancements**: Visual improvements and animations
- **Mobile App**: Native mobile application
- **Docker Support**: Containerization
- **CI/CD Pipeline**: Automated testing and deployment

## 📋 Code Review Process

1. **Automated checks** must pass (linting, tests)
2. **Manual review** by project maintainers
3. **Testing** on different environments
4. **Documentation review** for completeness
5. **Final approval** and merge

## 🐛 Bug Reports

When reporting bugs, please include:

- **Environment details** (OS, Python version, browser)
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Error messages** or logs
- **Screenshots** if applicable

## 💡 Feature Requests

For new features, please provide:

- **Clear description** of the feature
- **Use case** and benefits
- **Implementation suggestions** (if any)
- **Potential challenges** or considerations

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Cybersecurity Best Practices](https://owasp.org/)

## 🙏 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

## 📞 Questions?

If you have questions about contributing:
- Create an issue with the "question" label
- Contact the project maintainer
- Check existing documentation

Thank you for contributing to SIMGuard! 🛡️
