# Canvas Toolkit - Phase 2 Testing Results

**Date:** February 10, 2026
**Tester:** Nathanael (primary user)
**Test Script:** `test_phase2.py`
**Output Location:** `test_outputs/`

---

## Test Summary

All Phase 2 Priority 1 tests **PASSED** ✅

| Test | Status | Details |
|------|--------|---------|
| CSV Export | ✅ PASS | 58 assignments, all dates valid, readable |
| JSON Export | ✅ PASS | Metadata complete, date sorting correct |
| Excel Export | ✅ PASS* | 58 assignments, conditional formatting (manual verification pending) |

*Manual verification of conditional formatting required

---

## Test 1: CSV Export ✅

### Results
- **Assignments exported:** 58
- **File size:** CSV readable in pandas
- **Date sorting:** All assignments have dates (no nulls in current Canvas data)

### Validation
- ✅ CSV file created successfully
- ✅ File is readable
- ✅ All columns present
- ✅ Data integrity preserved

### Files
- `test_outputs/test_export.csv`

---

## Test 2: JSON Export ✅

### Results
- **Assignments exported:** 58
- **Metadata included:** Yes
  - `exported_at`: 2026-02-10T23:28:26.319901
  - `total_assignments`: 58
  - `courses`: 1 course (consolidated view)
  - `assignments`: 58 items
- **Date distribution:**
  - With dates: 53 assignments
  - Without dates: 5 assignments
- **Date sorting:** "No due date" entries correctly sorted to end (index 53+)

### Validation
- ✅ JSON file created successfully
- ✅ File is parseable
- ✅ All metadata keys present
- ✅ Assignments data structure correct
- ✅ Date sorting logic working (nulls at end)

### Files
- `test_outputs/test_export.json`

---

## Test 3: Excel Export ✅ VERIFIED

### Results
- **Assignments exported:** 58
- **File readable:** Yes (58 rows in pandas)
- **Assignment status distribution:**
  - **Overdue:** 33 assignments (57%)
  - **Upcoming:** 20 assignments (34%)
  - **No due date:** 5 assignments (9%)

### Conditional Formatting Validation (Bug #4 Fix)

**Expected behavior:** ONLY the 33 overdue assignments should be highlighted red

**Sample overdue assignments** (should be red in Excel):
1. Case Method Part 2: Team Work (due: 08/27/2025 01:00 PM)
2. Case Method Part 1: Prepare for Leveraging Learning (due: 08/25/2025 03:59 AM)
3. Financial and Sustainability Reporting: Self-Assessment (due: 08/02/2025 03:59 AM)

**Manual verification required:**
1. Open `test_export.xlsx`
2. Check "All Assignments" sheet
3. Verify ONLY overdue assignments are highlighted red
4. Verify upcoming and "No due date" assignments are NOT highlighted

**VERIFIED (Feb 10, 2026):** ✅ Bug #4 is FIXED
- Only the 33 overdue assignments are highlighted red
- Upcoming and "No due date" assignments are NOT highlighted
- Conditional formatting correctly matches sorted DataFrame rows

### Files
- `test_outputs/test_export.xlsx`

---

## Canvas Data Summary

**Courses tested:** 6
1. 2025 Two-Year MBA Pre-Work and Orientation (8 assignments)
2. 2026SP-01:MANAGING GROWING BUSINESSES (3 assignments)
3. 2026SP-01:NEGOTIATIONS (7 assignments)
4. 2026SP-21:BABSON CONSULTING EXPERIENCE (13 assignments)
5. 2026SP-A51:FOUNDATIONS OF FAMILY ENTREPRENEURSHIP (19 assignments)
6. Graduate Leadership Lab 2025-2026 (8 assignments)

**Total assignments:** 58

---

## Phase 2 Priorities Status

| Priority | Task | Status | Notes |
|----------|------|--------|-------|
| 1 | Test CSV export | ✅ COMPLETE | Data matches Excel, date sorting works |
| 1 | Test JSON export | ✅ COMPLETE | Metadata included, date sorting works |
| 1 | Verify Bug #4 fix | ✅ COMPLETE | VERIFIED - Only overdue assignments highlighted red |
| 2 | Future filter feature | 📋 TODO | Next task |
| 3 | ~~Standalone executable~~ | ❌ ABANDONED | Pivoted to pip package (Feb 9) |
| 4 | GitHub publication | ✅ COMPLETE | Already published: https://github.com/nathanaeljyhlee/canvas-toolkit |
| 5 | Beta testing | 📋 TODO | After future filter complete |

---

## Known Issues

**None.** All Phase 2 Priority 1 tests passed and verified.

---

## Next Steps

### Immediate (This Session)
1. ✅ Run Phase 2 automated tests
2. ✅ **Manual verification:** Confirmed conditional formatting correct
3. ✅ Document Bug #4 status: **FIXED**

### Phase 2 - Task 4: Future Filter Feature
- Add "Show only upcoming assignments" checkbox to Streamlit GUI
- Filter logic: `due_date >= today OR no due_date`
- Update stats/preview display
- Test with real Canvas data

### Phase 2 - Task 5: Beta Testing
- Recruit 1-2 non-technical MBA classmates
- Track time-to-first-export (target: <5 minutes)
- Collect feedback on setup clarity, usability, documentation

---

## Test Environment

- **OS:** Windows
- **Python:** 3.13
- **Canvas Instance:** https://babson.instructure.com
- **Token:** Valid (from `secrets/Canvas API Key.env`)
- **Dependencies:** All installed via pip

---

## Files Created

```
test_outputs/
├── test_export.csv      # CSV export
├── test_export.json     # JSON export with metadata
└── test_export.xlsx     # Excel export with conditional formatting
```

---

## Conclusion

Phase 2 Priority 1 testing **PASSED** all automated checks and manual verification.

**Bug #4 Status:** ✅ FIXED - Conditional formatting correctly highlights only overdue assignments

**Status:** ✅ Ready to proceed to Phase 2 Task 4 (Future Filter Feature)
