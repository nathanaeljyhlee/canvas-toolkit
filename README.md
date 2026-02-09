# Canvas Toolkit

**Export your Canvas LMS assignments to Excel, CSV, or JSON with one click.**

Built for MBA students who want to manage their assignments outside of Canvas. No coding required - just run the app and export your data.

---

## ✨ Features

- **📊 Multiple Export Formats**: Excel (with formatting), CSV, or JSON
- **🎨 Beautiful Excel Output**: Conditional formatting, filters, hyperlinks, multiple sheets
- **🚀 Zero Configuration**: Auto-detects all your courses
- **🔒 Secure**: Your API token never leaves your computer
- **💻 Cross-Platform**: Works on Windows, Mac, and Linux

---

## 🚀 Quick Start

### 1. Install Python

Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)

### 2. Install Canvas Toolkit

```bash
# Option A: Install from GitHub
pip install git+https://github.com/nathanaeljyhlee/canvas-toolkit.git

# Option B: Clone and install locally
git clone https://github.com/nathanaeljyhlee/canvas-toolkit.git
cd canvas-toolkit
pip install -r requirements.txt
```

### 3. Get Your Canvas API Token

See [SETUP.md](SETUP.md) for detailed instructions with screenshots.

**Quick version:**
1. Log into Canvas
2. Account → Settings
3. Scroll to "Approved Integrations"
4. Click "+ New Access Token"
5. Copy the token

### 4. Run the App

```bash
streamlit run canvas_toolkit.py
```

Your browser will open automatically to `http://localhost:8501`

**👉 New to Python? See [QUICK_START.md](QUICK_START.md) for a beginner-friendly guide with screenshots!**

---

## 📖 Usage

### Export to Excel (Recommended)

1. Run `streamlit run canvas_toolkit.py`
2. Enter your Canvas API token in the sidebar
3. Select courses to export (or "Select all")
4. Choose "Excel" as export format
5. Click "Export Assignments"
6. Download your formatted Excel file

**Excel output includes:**
- Multiple sheets (one per course + "All Assignments")
- Conditional formatting (overdue = red highlight)
- Clickable Canvas links
- Filters on all columns
- Auto-sized columns

### Export to CSV

Same steps as Excel, but choose "CSV" format. Great for importing into Google Sheets or other tools.

### Export to JSON

Choose "JSON" format for a structured data export with metadata (export timestamp, course list, etc.).

---

## 🎯 Use Cases

- **Weekly Planning**: Export upcoming assignments to plan your week
- **Deadline Tracking**: See all deadlines in one place (not scattered across Canvas)
- **Cross-Course View**: Compare workload across all courses
- **Offline Access**: Work with assignment data when offline
- **Custom Analysis**: Import into Excel/Sheets for custom tracking

---

## 🛠️ Advanced Usage

### Filter by Date Range

Coming in Phase 2! For now, export all assignments and filter in Excel.

### Sync with Notion

Coming in Phase 3! If you use Notion for task management, we'll add automatic sync.

---

## ❓ Troubleshooting

### "Invalid API token"
- Token expires after generation - regenerate a new one in Canvas
- Make sure you copied the full token (usually starts with `1~`)

### "No courses found"
- Check that your Canvas URL is correct (e.g., `https://babson.instructure.com`)
- Make sure you have active enrollments in Canvas

### "Module not found" errors
- Run `pip install -r requirements.txt` again
- Make sure you're in the canvas-toolkit directory

### Export button doesn't work
- Check browser console for errors
- Try refreshing the page
- Make sure you selected at least one course

---

## 🤝 Contributing

This tool was built for MBA students, by an MBA student. Contributions welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - feel free to use, modify, and share!

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the GUI
- Uses [Canvas LMS API](https://canvas.instructure.com/doc/api/)
- Inspired by the need for better assignment management at Babson College

---

## 📧 Support

- [Open an issue](https://github.com/nathanaeljyhlee/canvas-toolkit/issues) for bugs or feature requests
- Share with classmates who might find this useful!

---

**Made with ❤️ for MBA students**
