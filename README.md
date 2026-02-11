# Canvas Toolkit

**Export your Canvas LMS content (assignments, announcements, modules) to Excel, CSV, or JSON with one click.**

Built for MBA students who want to manage their course content outside of Canvas. No coding required - just run the app and export your data.

📺 **[Watch Demo Video](https://www.youtube.com/watch?v=CSk8Edhxy3I)** - See it in action!

---

## ✨ Features

- **📚 Multi-Content Export**: Assignments, announcements (last 30 days), and module content
- **📊 Multiple Export Formats**: Excel (with formatting), CSV, or JSON
- **🎨 Beautiful Excel Output**: Conditional formatting, filters, hyperlinks, multiple sheets
- **🔍 Smart Parsing**: Extracts plain text and links from HTML announcements
- **📑 Hierarchical Modules**: Preserves Canvas module structure with indentation
- **🚀 Zero Configuration**: Auto-detects all your courses
- **🔒 Secure**: Your API token never leaves your computer
- **💻 Cross-Platform**: Works on Windows, Mac, and Linux

---

## 🚀 Quick Start (5 Minutes)

**👉 New to Python? See [QUICK_START.md](QUICK_START.md) for a beginner-friendly guide with screenshots!**

### Windows Users (Easiest)

1. **Install Python** (one-time setup)
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add Python to PATH" during install
   - Click "Install Now"

2. **Install Canvas Toolkit**
   - Download this repo (green "Code" button → "Download ZIP")
   - Extract and double-click `install-canvas-toolkit.bat`
   - Wait for "Installation successful!"

3. **Run the app**
   - Double-click `run-canvas-toolkit.bat`
   - Browser opens automatically!

### Mac/Linux or Command Line

```bash
# Install
pip install git+https://github.com/nathanaeljyhlee/canvas-toolkit.git

# Run
streamlit run canvas_toolkit.py
```

### Get Your Canvas API Token

1. Log into Canvas → Account → Settings
2. Scroll to "Approved Integrations"
3. Click "+ New Access Token"
4. Copy the token (shown only once!)

Full instructions: [SETUP.md](SETUP.md)

---

## 📖 Usage

### Export to Excel (Recommended)

1. Run `streamlit run canvas_toolkit.py`
2. Enter your Canvas API token in the sidebar
3. Select courses to export (or "Select all")
4. **Choose content types** (Assignments ✓, Announcements, Modules)
5. Choose "Excel" as export format
6. Click "Export Content"
7. Download your formatted Excel file

**Excel output includes:**
- Multiple sheets (All Assignments, All Announcements, All Modules)
- Conditional formatting:
  - Assignments: Overdue (red), Upcoming (yellow)
  - Announcements: Recent (last 7 days, green)
- Clickable Canvas links
- Module items with hierarchical indentation
- Filters on all columns
- Auto-sized columns

### Export to CSV

Same steps as Excel, but choose "CSV" format. When multiple content types are selected, creates separate files:
- `filename_assignments.csv`
- `filename_announcements.csv`
- `filename_modules.csv`

Great for importing into Google Sheets or other tools.

### Export to JSON

Choose "JSON" format for a structured data export with metadata (export timestamp, counts, etc.). All content types are combined in one file with separate sections.

---

## 🎯 Use Cases

- **Weekly Planning**: Export upcoming assignments to plan your week
- **Deadline Tracking**: See all deadlines in one place (not scattered across Canvas)
- **Cross-Course View**: Compare workload across all courses
- **Announcement Tracking**: Keep important announcements in one searchable file
- **Module Navigation**: Export course roadmap with all readings, assignments, and resources
- **Offline Access**: Work with course content when offline
- **Custom Analysis**: Import into Excel/Sheets for custom tracking

---

## 🛠️ Features

### Content Type Selection

Choose which content to export:
- **📚 Assignments** (default): All assignments with due dates, points, submission types
- **📢 Announcements**: Last 30 days, with HTML parsing and embedded link extraction
- **📑 Modules**: Course structure with all pages, files, assignments, and resources

### Future-Only Filter

Use the **"Show only upcoming assignments"** checkbox to filter out past assignments and focus on what's coming up.

### Upcoming Features

- **Date Range Picker** - Custom date ranges for announcements (7/30/90 days)
- **Module Filtering** - Filter by item type (Page, Assignment, Quiz, etc.)
- **Notion Sync** - Automatic sync with Notion for task management
- **Attachment Download** - Auto-download announcement attachments

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
