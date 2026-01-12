# SIMGuard Project Structure

This document provides a comprehensive overview of the SIMGuard project structure and file organization.

## 📁 Directory Structure

```
SIMGuard/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT License
├── 📄 CHANGELOG.md                 # Version history and changes
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 .gitignore                   # Git ignore rules
├── 📄 index.html                   # Frontend main page
├── 📄 styles.css                   # Frontend CSS styles
├── 📄 script.js                    # Frontend JavaScript
├── 📄 sample_logs.csv              # Sample data for testing
├── 📁 backend/                     # Backend Flask API
│   ├── 📄 app.py                   # Main Flask application
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 README.md                # Backend documentation
│   ├── 📄 run.py                   # Startup script
│   ├── 📄 test_api.py              # API testing suite
│   ├── 📄 .gitkeep                 # Ensures directory tracking
│   └── 📁 uploads/                 # File upload directory
│       └── 📄 .gitkeep             # Ensures directory tracking
├── 📁 docs/                        # Documentation
│   ├── 📄 DEPLOYMENT.md            # Deployment guide
│   └── 📄 PROJECT_STRUCTURE.md     # This file
└── 📁 .git/                        # Git repository data (hidden)
```

## 📋 File Descriptions

### Root Directory Files

#### 📄 README.md
- **Purpose**: Main project documentation and entry point
- **Content**: Project overview, features, installation, usage guide
- **Audience**: Developers, users, academic reviewers
- **Maintenance**: Update with new features and changes

#### 📄 LICENSE
- **Purpose**: Legal license for the project (MIT License)
- **Content**: Copyright notice and usage permissions
- **Audience**: Legal compliance, contributors
- **Maintenance**: Rarely changed

#### 📄 CHANGELOG.md
- **Purpose**: Version history and release notes
- **Content**: Detailed changes, new features, bug fixes
- **Audience**: Developers, users tracking updates
- **Maintenance**: Update with each release

#### 📄 CONTRIBUTING.md
- **Purpose**: Guidelines for project contributors
- **Content**: Development setup, coding standards, PR process
- **Audience**: Contributors, developers
- **Maintenance**: Update as project evolves

#### 📄 .gitignore
- **Purpose**: Specify files Git should ignore
- **Content**: Python cache, virtual environments, uploads, logs
- **Audience**: Git version control system
- **Maintenance**: Add new patterns as needed

### Frontend Files

#### 📄 index.html
- **Purpose**: Main web interface
- **Content**: HTML structure, navigation, sections
- **Technology**: HTML5 with semantic elements
- **Features**: Responsive design, accessibility
- **Size**: ~200 lines

#### 📄 styles.css
- **Purpose**: Visual styling and layout
- **Content**: CSS variables, responsive design, animations
- **Technology**: CSS3 with modern features
- **Features**: Cybersecurity theme, mobile-first design
- **Size**: ~800 lines

#### 📄 script.js
- **Purpose**: Interactive functionality
- **Content**: File upload, API integration, chart rendering
- **Technology**: Vanilla JavaScript ES6+
- **Features**: Async/await, error handling, real-time updates
- **Size**: ~500 lines

#### 📄 sample_logs.csv
- **Purpose**: Test data for demonstration
- **Content**: Simulated user activity logs
- **Format**: CSV with required columns
- **Use Case**: Testing, demos, development
- **Size**: 20 sample records

### Backend Directory

#### 📄 backend/app.py
- **Purpose**: Main Flask application and API
- **Content**: All API endpoints, detection algorithms, PDF generation
- **Technology**: Python 3.8+, Flask, Pandas, FPDF
- **Features**: RESTful API, CORS, error handling
- **Size**: ~800 lines

#### 📄 backend/requirements.txt
- **Purpose**: Python package dependencies
- **Content**: Pinned versions of required packages
- **Technology**: pip package manager format
- **Maintenance**: Update versions as needed
- **Packages**: Flask, Pandas, NumPy, FPDF2, Flask-CORS

#### 📄 backend/README.md
- **Purpose**: Backend-specific documentation
- **Content**: API documentation, endpoints, examples
- **Audience**: API users, backend developers
- **Maintenance**: Update with API changes

#### 📄 backend/run.py
- **Purpose**: Application startup script
- **Content**: Dependency checks, directory setup, server start
- **Technology**: Python script
- **Features**: Environment validation, helpful output
- **Size**: ~100 lines

#### 📄 backend/test_api.py
- **Purpose**: Comprehensive API testing suite
- **Content**: Automated tests, interactive mode
- **Technology**: Python with requests library
- **Features**: Full test coverage, error scenarios
- **Size**: ~300 lines

#### 📁 backend/uploads/
- **Purpose**: Temporary file storage for uploads
- **Content**: User-uploaded CSV files (temporary)
- **Security**: Files automatically cleaned up
- **Git**: Directory tracked, files ignored

### Documentation Directory

#### 📄 docs/DEPLOYMENT.md
- **Purpose**: Deployment instructions and guides
- **Content**: Local, production, Docker deployment options
- **Audience**: DevOps, system administrators
- **Maintenance**: Update with new deployment methods

#### 📄 docs/PROJECT_STRUCTURE.md
- **Purpose**: This file - project organization guide
- **Content**: File descriptions, architecture overview
- **Audience**: Developers, contributors
- **Maintenance**: Update when structure changes

## 🏗️ Architecture Overview

### Frontend Architecture
```
Browser
├── HTML (Structure)
├── CSS (Presentation)
└── JavaScript (Behavior)
    ├── File Upload
    ├── API Communication
    ├── Data Visualization
    └── User Interface
```

### Backend Architecture
```
Flask Application
├── API Endpoints
│   ├── /upload (File handling)
│   ├── /analyze (Detection logic)
│   ├── /results (Data retrieval)
│   └── /report (PDF generation)
├── Detection Engine
│   ├── SIM Change Detection
│   ├── Location Analysis
│   ├── Device Fingerprinting
│   └── Behavioral Analytics
└── Data Processing
    ├── CSV Parsing
    ├── Validation
    └── Analysis
```

### Data Flow
```
1. User uploads CSV file
2. Frontend sends file to backend
3. Backend validates and processes file
4. Detection algorithms analyze data
5. Results stored in memory
6. Frontend displays results
7. User can download PDF report
```

## 🔧 Development Workflow

### Adding New Features

1. **Frontend Changes**
   - Modify `index.html` for structure
   - Update `styles.css` for styling
   - Enhance `script.js` for functionality

2. **Backend Changes**
   - Add endpoints to `app.py`
   - Update `requirements.txt` if needed
   - Add tests to `test_api.py`

3. **Documentation**
   - Update relevant README files
   - Add to CHANGELOG.md
   - Update API documentation

### File Naming Conventions

- **HTML/CSS/JS**: Lowercase with hyphens (kebab-case)
- **Python**: Lowercase with underscores (snake_case)
- **Documentation**: UPPERCASE.md for important docs
- **Directories**: Lowercase, descriptive names

### Code Organization

- **Frontend**: Single-page application structure
- **Backend**: Modular functions within single file
- **Documentation**: Separate files by purpose
- **Tests**: Comprehensive coverage in dedicated files

## 📊 File Statistics

| Category | Files | Total Lines | Languages |
|----------|-------|-------------|-----------|
| Frontend | 3 | ~1,500 | HTML, CSS, JS |
| Backend | 4 | ~1,200 | Python |
| Documentation | 6 | ~2,000 | Markdown |
| Configuration | 3 | ~100 | Various |
| **Total** | **16** | **~4,800** | **6** |

## 🔍 Key Design Decisions

### Single-Page Application
- **Rationale**: Simplicity, no build process required
- **Benefits**: Easy deployment, fast loading
- **Trade-offs**: Limited scalability for complex features

### Monolithic Backend
- **Rationale**: Academic project scope, simplicity
- **Benefits**: Easy to understand and deploy
- **Trade-offs**: Less modular than microservices

### In-Memory Processing
- **Rationale**: Stateless operation, security
- **Benefits**: No persistent data concerns
- **Trade-offs**: Limited to single-session analysis

### PDF Reports
- **Rationale**: Professional output for academic use
- **Benefits**: Portable, formatted reports
- **Trade-offs**: Server-side generation overhead

## 🚀 Future Enhancements

### Potential Structure Changes
- **Database integration**: Add `models/` directory
- **Machine learning**: Add `ml/` directory
- **User authentication**: Add `auth/` module
- **Real-time features**: Add WebSocket support
- **Mobile app**: Add `mobile/` directory

### Scalability Considerations
- **Microservices**: Split backend into services
- **Database**: Add persistent storage layer
- **Caching**: Implement Redis for performance
- **Load balancing**: Multiple backend instances

---

This structure is designed for clarity, maintainability, and academic presentation while remaining flexible for future enhancements.
