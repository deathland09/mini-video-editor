# 📁 Project Structure

This document explains the organization of the FFmpeg Mini App repository.

## 🎯 Directory Layout

```
ffmpeg-mini-app/
├── src/                          # Source code
│   ├── __init__.py               # Package initialization
│   └── main.py                   # Main CLI application
├── scripts/                       # Build and utility scripts
│   ├── build.py                  # Cross-platform build script
│   └── setup.py                  # Package setup (moved from root)
├── docs/                         # Documentation
│   ├── guides/                   # User guides and tutorials
│   ├── examples/                 # Usage examples
│   └── PROJECT_STRUCTURE.md     # This file
├── assets/                       # Static assets (images, etc.)
├── __test__/                     # Test files (git ignored)
│   ├── test_drag_drop.py         # Drag-and-drop tests
│   ├── test_setup.py             # Environment tests
│   ├── demo_split.py             # Demo scripts
│   └── README.md                 # Test documentation
├── .github/                      # GitHub configuration
│   └── workflows/                # CI/CD workflows
│       └── build.yml             # Automated builds
├── README.md                     # Main project documentation
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies
├── setup.py                      # Package installation
└── .gitignore                    # Git ignore rules
```

## 📂 Directory Descriptions

### `src/` - Source Code
- **Purpose**: Contains the main application code
- **Files**: 
  - `main.py` - Main CLI application
  - `__init__.py` - Package initialization

### `scripts/` - Build Scripts
- **Purpose**: Contains build and utility scripts
- **Files**:
  - `build.py` - Cross-platform executable builder
  - `setup.py` - Package setup configuration

### `docs/` - Documentation
- **Purpose**: All project documentation
- **Subdirectories**:
  - `guides/` - User guides and tutorials
  - `examples/` - Usage examples and demos

### `assets/` - Static Assets
- **Purpose**: Images, icons, and other static files
- **Usage**: For documentation and releases

### `__test__/` - Test Files
- **Purpose**: Development and testing files
- **Status**: Git ignored (not committed)
- **Files**: Test scripts and demo files

### `.github/` - GitHub Configuration
- **Purpose**: GitHub-specific configuration
- **Files**: CI/CD workflows for automated builds

## 🎯 Benefits of This Structure

✅ **Clean Separation** - Source code, scripts, and docs are separated  
✅ **Professional Layout** - Follows Python packaging best practices  
✅ **Easy Navigation** - Clear directory purposes  
✅ **Scalable** - Easy to add new features and documentation  
✅ **Git Friendly** - Proper .gitignore for clean commits  

## 🚀 Development Workflow

### Adding New Features
1. **Source Code**: Add to `src/` directory
2. **Documentation**: Add to `docs/` directory
3. **Tests**: Add to `__test__/` directory
4. **Build**: Update `scripts/build.py` if needed

### Building Executables
```bash
# Run build script
python3 scripts/build.py

# Output: dist/FFmpegMiniApp
```

### Testing
```bash
# Run tests
cd __test__
python3 test_setup.py
python3 test_drag_drop.py
```

## 📦 Distribution

### For End Users
- Download executable from `dist/` directory
- No Python installation required

### For Developers
- Clone repository
- Install dependencies: `pip install -r requirements.txt`
- Use CLI: `python3 src/main.py`

## 🔧 Maintenance

### Adding Dependencies
- Update `requirements.txt`
- Update `setup.py` if needed

### Updating Documentation
- Main docs: `README.md`
- Detailed guides: `docs/guides/`
- Examples: `docs/examples/`

### Version Management
- Update version in `src/__init__.py`
- Update version in `setup.py`
- Create GitHub release

---

This structure provides a clean, professional, and maintainable codebase for the FFmpeg Mini App.
