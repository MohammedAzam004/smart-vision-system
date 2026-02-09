# Contributing to AI Vision Hub

First off, thank you for considering contributing to AI Vision Hub! It's people like you that make this project a great tool for learning and exploring computer vision.

## 🤝 Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what is best for the community

## 🎯 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior**
- **Actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, OpenCV version)

**Example Bug Report:**
```markdown
Title: Face detection fails in low light conditions

Description: Face detection doesn't work when room lighting is dim.

Steps to Reproduce:
1. Run face_detection.py
2. Reduce room lighting
3. Face not detected

Expected: Face should be detected with some accuracy
Actual: No detection at all

Environment:
- OS: Windows 11
- Python: 3.11
- OpenCV: 4.13.0
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

- **Clear title and detailed description**
- **Step-by-step mockup** of how it would work
- **Why this enhancement would be useful** to most users
- **Alternative solutions** you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our coding standards
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit with clear messages**
6. **Submit a pull request**

## 📝 Coding Standards

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifics:

```python
# Good: Descriptive variable names
face_cascade = cv2.CascadeClassifier('model.xml')
detected_faces = face_cascade.detectMultiScale(gray_image)

# Bad: Unclear names
fc = cv2.CascadeClassifier('model.xml')
d = fc.detectMultiScale(g)
```

### Comments and Documentation

- **Inline comments**: Explain complex logic
- **Function docstrings**: Describe purpose, parameters, returns
- **Module docstrings**: Overview of file purpose

```python
def detect_faces(image, scale_factor=1.1, min_neighbors=5):
    """
    Detect faces in an image using Haar Cascade classifier.
    
    Args:
        image: Input image in BGR format
        scale_factor: Image pyramid scale reduction (default 1.1)
        min_neighbors: Minimum neighbor rectangles (default 5)
    
    Returns:
        List of tuples containing (x, y, w, h) for each detected face
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scale_factor, min_neighbors)
    return faces
```

### Error Handling

Always include proper error handling:

```python
# Good
try:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
except Exception as e:
    print(f"Error: {e}")
    return None

# Bad
image = cv2.imread(image_path)  # No error handling
```

## 🌿 Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Adding tests

Examples:
- `feature/gpu-acceleration`
- `fix/camera-access-error`
- `docs/update-readme`

## 💬 Commit Message Guidelines

Format: `<type>: <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat: Add GPU acceleration support
fix: Resolve camera initialization error on Mac
docs: Update installation instructions for Linux
refactor: Optimize face detection performance
```

## 🧪 Testing

Before submitting:

1. **Test on your platform**
2. **Test basic functionality** of affected features
3. **Check for regressions** in existing features
4. **Consider edge cases**

### Manual Testing Checklist

- [ ] Code runs without errors
- [ ] Feature works as intended
- [ ] Existing features still work
- [ ] Documentation is updated
- [ ] No new warnings introduced

## 📚 Documentation Updates

When adding features or making changes:

1. **Update main README.md** if project structure changes
2. **Update relevant script README** if functionality changes
3. **Add inline comments** for complex logic
4. **Include usage examples** for new features

## 🎨 Adding New Features

### Before Starting

1. **Check existing issues** - maybe someone is already working on it
2. **Create an issue** to discuss the feature
3. **Get feedback** before investing time

### Development Process

1. Fork and create a branch
2. Implement the feature
3. Test thoroughly
4. Document the feature
5. Submit pull request

### New Script Template

If adding a new CV project:

```python
"""
Script Name - Brief Description

Author: Your Name
Date: YYYY-MM-DD
Purpose: Detailed purpose of the script
"""

import cv2
import numpy as np

def main():
    """Main function with clear workflow."""
    # Initialize
    # Process
    # Display
    # Cleanup
    pass

if __name__ == "__main__":
    main()
```

## 🐛 Debugging Tips

### Common Issues

**Camera Not Opening:**
```python
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    # Try alternative indices: 1, 2, etc.
```

**Model Files Missing:**
```python
import os
model_path = "models/haarcascade_frontalface_default.xml"
if not os.path.exists(model_path):
    print(f"Model file not found: {model_path}")
```

## 🚀 Performance Optimization

When optimizing:
1. **Profile first** - identify bottlenecks
2. **Optimize algorithms** before parallelizing
3. **Document trade-offs** (speed vs accuracy)
4. **Provide optional parameters** for users to choose

## 📦 Adding Dependencies

If you need to add a new package:

1. **Ensure it's necessary** - avoid bloat
2. **Check licensing** - must be compatible
3. **Update requirements.txt**
4. **Document in README** why it's needed

## ✅ Pull Request Checklist

Before submitting:

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tested on local machine
- [ ] Related issues referenced

## 🏆 Recognition

Contributors will be:
- Listed in project documentation
- Credited in release notes
- Acknowledged in commits

## 💡 Project Priorities

Current focus areas:
1. **Performance optimization**
2. **Cross-platform compatibility**
3. **Documentation improvements**
4. **Adding new CV projects**
5. **Test coverage**

## 📞 Getting Help

Need help contributing?
- Check existing documentation
- Review similar pull requests
- Open an issue with questions
- Be specific about what you need help with

## 🌟 First-Time Contributors

New to open source? Welcome! We're happy to help:

1. **Start small** - fix typos, improve docs
2. **Ask questions** - no question is too basic
3. **Learn from feedback** - reviews help you grow
4. **Take your time** - quality over speed

### Good First Issues

Look for issues labeled:
- `good-first-issue`
- `documentation`
- `help-wanted`

## 📋 Project Structure

Understanding the codebase:
```
snapchat_/
├── app.py                     # Main Streamlit app
├── face_detection.py          # Individual CV scripts
├── models/                    # Haar Cascade XML files
├── *.md                       # Documentation files
├── requirements.txt           # Dependencies
└── .gitignore                 # Git exclusions
```

## 🔄 Review Process

What happens after you submit:

1. **Automated checks** run (if configured)
2. **Maintainer review** within 5-7 days
3. **Feedback provided** if changes needed
4. **Merge** once approved
5. **Release notes** updated

## ❤️ Thank You!

Your contributions make this project better for everyone. Whether it's:
- Reporting a bug
- Suggesting a feature
- Improving documentation
- Writing code

**Every contribution matters!**

---

**Questions?** Open an issue or reach out to the maintainers.

**Ready to contribute?** Fork the repo and get started!

---

*Last updated: February 9, 2026*
