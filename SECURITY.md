# Security Considerations

This document outlines security considerations for Canvas Toolkit.

---

## API Token Handling

### Storage
- **Never commit API tokens to version control**
- Tokens should be stored in `.env` files (excluded via `.gitignore`)
- Pass tokens via environment variables or user input only

### Validation
- Canvas URLs are validated to prevent injection attacks
- Only `http://` and `https://` schemes are allowed
- Malformed URLs are rejected before making requests

### Transmission
- Tokens are sent via HTTPS to Canvas (never plain HTTP in production)
- Tokens are included in Authorization headers only
- Tokens never appear in error messages or logs

---

## HTML Content Parsing

### Parser Choice
- Uses Python's built-in `html.parser.HTMLParser`
- Stdlib parser is safe from injection attacks
- No external dependencies that could introduce vulnerabilities

### XSS Prevention
- HTML is parsed server-side only (no browser rendering)
- Extracted text is sanitized (tags removed)
- URLs from Canvas are preserved but not executed

### Malformed Content
- Parser handles malformed HTML gracefully (no crashes)
- Invalid dates return safe fallback strings
- Missing fields use safe defaults

---

## Canvas API Security

### Rate Limiting
- Client detects 429 (rate limit) responses
- Raises `RateLimitError` for user handling
- No automatic retries (prevents amplification)

### Error Handling
- API errors include context but not sensitive data
- Token validation happens before data requests
- Failed requests for one course don't affect others

### Request Validation
- All URLs are constructed from validated base URL
- Parameters are passed via requests library (prevents injection)
- No raw string concatenation for URLs

---

## Export File Security

### File Paths
- User-provided file paths are validated
- Paths are resolved to absolute paths
- No directory traversal attacks possible

### Excel/CSV Output
- Content is written using trusted libraries (pandas, openpyxl, xlsxwriter)
- No formula injection (all cells treated as data)
- No macros or executable content

### JSON Output
- Standard library `json` module used
- No eval() or exec() on user data
- Safe serialization only

---

## Dependency Security

### Minimal Dependencies
- Only 6 production dependencies (requests, pandas, streamlit, openpyxl, xlsxwriter, python-dotenv)
- All are well-maintained, widely-used libraries
- Regular updates recommended via `pip list --outdated`

### Audit Commands
```bash
# Check for known vulnerabilities
pip install safety
safety check

# Update dependencies
pip install --upgrade -r requirements.txt
```

---

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email the maintainer directly (see GitHub profile)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

Security issues will be addressed within 48 hours.

---

## Security Best Practices for Users

### Token Management
- Generate tokens with minimal required permissions
- Rotate tokens regularly (monthly recommended)
- Revoke tokens immediately if compromised
- Use separate tokens for testing vs production

### Environment Setup
- Run on trusted machines only
- Keep Python and dependencies updated
- Use virtual environments to isolate packages
- Don't share `.env` files or screenshots containing tokens

### Data Privacy
- Exported files contain your Canvas data (treat as confidential)
- Don't share exports publicly (may contain due dates, course info, etc.)
- Store exports securely (encrypted drive recommended)
- Delete exports when no longer needed

---

## Security Checklist for Contributors

When contributing code:

- [ ] No hardcoded tokens or credentials
- [ ] All user input validated before use
- [ ] No `eval()`, `exec()`, or similar dynamic execution
- [ ] No raw SQL or command injection risks
- [ ] Error messages don't leak sensitive data
- [ ] Dependencies are pinned to specific versions
- [ ] Tests cover security-relevant edge cases
- [ ] Documentation updated if security model changes

---

**Last Updated:** 2026-02-11
