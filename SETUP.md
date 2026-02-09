# Canvas Toolkit Setup Guide

Complete setup instructions with screenshots for non-technical users.

---

## Prerequisites

### 1. Install Python

**Windows:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download Python 3.11 (or latest 3.x version)
3. Run installer
4. ✅ **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

**Mac:**
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Download macOS installer
3. Run installer and follow prompts

**Verify installation:**
```bash
python --version
# Should show: Python 3.x.x
```

---

## Installation

### Option 1: Install from GitHub (Easiest)

```bash
pip install git+https://github.com/nathanaeljyhlee/canvas-toolkit.git
```

### Option 2: Clone and Install Locally

```bash
# Clone repository
git clone https://github.com/nathanaeljyhlee/canvas-toolkit.git

# Navigate to directory
cd canvas-toolkit

# Install dependencies
pip install -r requirements.txt
```

---

## Getting Your Canvas API Token

### Step-by-Step (with screenshots coming soon)

1. **Log into Canvas**
   - Go to your school's Canvas URL (e.g., `https://babson.instructure.com`)
   - Log in with your credentials

2. **Navigate to Settings**
   - Click your profile picture (top left)
   - Select **Account**
   - Click **Settings**

3. **Scroll to Approved Integrations**
   - Scroll down the Settings page
   - Find section titled **Approved Integrations**

4. **Generate New Token**
   - Click **+ New Access Token**
   - A dialog box will appear

5. **Fill in Token Details**
   - **Purpose**: Enter "Canvas Toolkit Export"
   - **Expires**: Leave blank (no expiration)
   - Click **Generate Token**

6. **Copy Your Token**
   - ⚠️ **CRITICAL**: Copy the token NOW
   - It will look like: `1~HBUfR7a6ccHcLYUczWZEADmt...`
   - This is the ONLY time you'll see it
   - Save it somewhere safe (password manager recommended)

7. **Token Copied!**
   - Click **OK** to close the dialog
   - Your token is now active

---

## Running the App

### First Time Setup

1. **Open Terminal/Command Prompt**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter

2. **Navigate to canvas-toolkit directory**
   ```bash
   cd path/to/canvas-toolkit
   ```

3. **Run Streamlit app**
   ```bash
   streamlit run canvas_toolkit.py
   ```

4. **Browser Opens Automatically**
   - App will open at `http://localhost:8501`
   - If not, manually go to that URL

### Using the App

1. **Enter Canvas URL** (sidebar)
   - Default: `https://babson.instructure.com`
   - Change if using different Canvas instance

2. **Paste API Token** (sidebar)
   - Click the password field
   - Paste your token (Ctrl+V or Cmd+V)

3. **Click "How to get your Canvas API token"** (optional)
   - Expander with step-by-step instructions
   - Use if you lost these setup notes

4. **Wait for Connection Test**
   - App will test your token
   - Green ✅ = Success
   - Red ❌ = Invalid token (regenerate)

5. **Select Courses**
   - "Select all courses" is checked by default
   - Or uncheck and select specific courses

6. **Choose Export Format**
   - **Excel** (recommended): Beautiful formatting, multiple sheets
   - **CSV**: Simple, import to Google Sheets
   - **JSON**: Structured data with metadata

7. **Click "Export Assignments"**
   - Wait for spinner (fetching data)
   - See stats: Total assignments, courses, upcoming

8. **Download File**
   - Click "Download [Format] File" button
   - File saves to your Downloads folder

9. **Preview (Optional)**
   - Click "Preview" expander
   - See first 10 assignments in table

---

## Regular Usage

After first-time setup, just run:

```bash
streamlit run canvas_toolkit.py
```

The app remembers your settings (cached in browser).

---

## Troubleshooting

### Python not found

**Problem**: `python: command not found`

**Solution**:
- Reinstall Python, check "Add to PATH"
- Or use `python3` instead of `python`

### pip not found

**Problem**: `pip: command not found`

**Solution**:
```bash
python -m pip install -r requirements.txt
```

### Invalid API Token

**Problem**: "❌ Invalid API token"

**Solution**:
- Regenerate token in Canvas (old one might have expired)
- Make sure you copied the FULL token
- Token should start with `1~`

### No Courses Found

**Problem**: "No active courses found"

**Solution**:
- Check Canvas URL is correct
- Make sure you're enrolled in active courses
- Try checking "Include concluded courses" (coming in Phase 2)

### Browser Doesn't Open

**Problem**: Streamlit runs but browser doesn't open

**Solution**:
- Manually go to `http://localhost:8501`
- Or run: `streamlit run canvas_toolkit.py --server.headless false`

### Port Already in Use

**Problem**: "Address already in use"

**Solution**:
```bash
# Use a different port
streamlit run canvas_toolkit.py --server.port 8502
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install package
pip install -e .
```

### Permission Denied (Windows)

**Problem**: Can't write output file

**Solution**:
- Run terminal as Administrator
- Or change output filename to a different location

---

## Security Best Practices

### Protect Your API Token

- ❌ **Never** commit your token to GitHub
- ❌ **Never** share your token with others
- ❌ **Never** post your token in Slack/Teams
- ✅ **Do** store in password manager
- ✅ **Do** regenerate if compromised

### What the Token Can Do

Your Canvas API token can:
- ✅ Read your courses and assignments
- ✅ Read your grades
- ❌ **Cannot** change grades
- ❌ **Cannot** submit assignments
- ❌ **Cannot** delete anything

**This app only reads data - it never modifies Canvas.**

### Revoking Access

To revoke the token:
1. Go to Canvas → Account → Settings
2. Scroll to "Approved Integrations"
3. Find "Canvas Toolkit Export"
4. Click "Delete" or ❌

---

## Next Steps

1. ✅ Export your first assignment list
2. ✅ Share with classmates (send them this repo link)
3. ✅ Open an issue if you find bugs
4. ✅ Star the repo if you find it useful!

---

## Getting Help

- **Documentation**: Re-read this guide
- **Issues**: [Open an issue on GitHub](https://github.com/nathanaeljyhlee/canvas-toolkit/issues)
- **Classmates**: Ask in your class Slack/Teams

---

**Good luck with your assignments! 📚**
