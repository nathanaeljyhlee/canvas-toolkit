# Canvas Toolkit - Comprehensive Improvement Plan

**Date:** Feb 11, 2026
**Goal:** Improve code quality, robustness, testing, documentation, and security without introducing complexity or bugs

---

## Current State Assessment

### Strengths
✅ Good type hints throughout
✅ Solid docstrings on most functions
✅ Clean separation of concerns (client, models, writers)
✅ Proper error handling in API client
✅ Dataclass models are clean and maintainable

### Gaps Identified
⚠️ Minimal test coverage (only import test)
⚠️ HTML parser has no malformed input tests
⚠️ No validation for empty/malformed API responses
⚠️ Missing edge case handling in date parsing
⚠️ Print statements for errors (should use logging)
⚠️ No input sanitization documentation

---

## Improvement Areas

### 1. Testing (High Priority)
**Impact:** Prevent regressions, catch bugs early
**Files to add:** `tests/test_html_parser.py`, `tests/test_models.py`, `tests/test_client.py`

**Specific tests:**
- HTML parser: Malformed HTML, XSS attempts, empty input, nested tags
- Models: Missing required fields, invalid dates, null handling
- Client: Pagination edge cases, empty responses, malformed JSON

### 2. Robustness (High Priority)
**Impact:** Handle edge cases gracefully without crashes
**Files to modify:** `html_parser.py`, `announcement.py`, `module.py`

**Specific improvements:**
- Add try-except for malformed HTML parsing
- Validate date strings before parsing
- Handle missing/null fields in API responses
- Add defensive checks for empty lists

### 3. Error Handling (Medium Priority)
**Impact:** Better debugging, clearer user feedback
**Files to modify:** `canvas_client.py`, `excel_writer.py`

**Specific improvements:**
- Replace print() with logging module
- Add context to error messages (which course failed, why)
- Add timeout handling for API requests

### 4. Documentation (Low Priority)
**Impact:** Easier onboarding for contributors
**Files to add:** `CONTRIBUTING.md`, inline comments for complex logic

**Specific improvements:**
- Document HTML parser security considerations
- Add architecture diagram to README
- Clarify date handling edge cases

### 5. Security (Medium Priority)
**Impact:** Prevent vulnerabilities
**Files to audit:** `html_parser.py`, `canvas_client.py`

**Specific improvements:**
- Document that HTMLParser is stdlib (safe from injection)
- Add URL validation for Canvas URLs
- Ensure no token leakage in error messages

---

## Implementation Order

**Phase 1: Critical Path (Do First)**
1. Add HTML parser tests (security-relevant)
2. Add input validation for Canvas URLs
3. Improve error handling in client (add context)

**Phase 2: Testing Foundation**
4. Add model tests (edge cases)
5. Add client tests (mocked API responses)
6. Add writer tests (validate output)

**Phase 3: Polish**
7. Replace print() with logging
8. Add inline comments for complex logic
9. Create CONTRIBUTING.md

---

## Success Criteria

✅ Test coverage >70% for critical paths (parser, models, client)
✅ No new bugs introduced (run existing test_phase2.py)
✅ All tests pass
✅ No breaking API changes
✅ Token count <50k for entire improvement session

---

## Risk Mitigation

- Test each change immediately after making it
- Keep changes small and isolated
- Run existing tests after each file modification
- Commit after each completed improvement
- Document any assumptions made
