# Fixing Tkinter on macOS with pyenv

## Problem
Your Python installation (via pyenv) doesn't have tkinter support compiled in, which is needed for the GUI versions of the app.

## Solutions

### Option 1: Use the CLI Version (Easiest) ✅
**No installation needed - works right now!**

```bash
python3 ffmpeg_cli.py
```

This version has all the same features but uses a command-line interface instead of a GUI.

---

### Option 2: Reinstall Python with Tkinter Support

#### Step 1: Install tk via Homebrew
```bash
brew install tcl-tk
```

#### Step 2: Reinstall Python with tkinter support
```bash
# For Python 3.12.4
env \
  PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
  LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
  CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
  CFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
  pyenv install --force 3.12.4
```

#### Step 3: Verify tkinter works
```bash
python3 -c "import tkinter; print('Tkinter works!')"
```

#### Step 4: Run the GUI app
```bash
python3 ffmpeg_app_simple.py
```

---

### Option 3: Use System Python

macOS comes with Python that usually includes tkinter:

```bash
# Check if system Python has tkinter
/usr/bin/python3 -c "import tkinter; print('Tkinter works!')"

# If it works, run the app with system Python
/usr/bin/python3 ffmpeg_app_simple.py
```

---

## Recommendation

**Use the CLI version (`ffmpeg_cli.py`)** - it has all the same features and works without any additional setup! The GUI is nice to have but not necessary.

The CLI version even supports drag-and-drop (you can drag a file into the terminal) and has a colored, user-friendly interface.

