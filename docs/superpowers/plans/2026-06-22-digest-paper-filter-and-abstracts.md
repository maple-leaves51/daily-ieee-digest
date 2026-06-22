# Digest Paper Filter And Abstracts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restrict the digest to likely real papers and include authors plus abstract text in each email entry.

**Architecture:** Extend the existing Crossref-based candidate model with author and abstract fields, reject metadata patterns that identify non-paper entries, and update the text/HTML renderers to emit the richer metadata. Cover the regression with focused unit tests around collection and rendering.

**Tech Stack:** Python 3 standard library, `unittest`, Crossref HTTP metadata

---

### Task 1: Add regression tests

**Files:**
- Create: `tests/test_daily_ieee_digest.py`
- Test: `tests/test_daily_ieee_digest.py`

- [ ] **Step 1: Write the failing tests**
- [ ] **Step 2: Run `python -m unittest tests/test_daily_ieee_digest.py -v` and confirm the new expectations fail**
- [ ] **Step 3: Implement the minimal production changes to satisfy the tests**
- [ ] **Step 4: Re-run `python -m unittest tests/test_daily_ieee_digest.py -v` until all tests pass**

### Task 2: Update script behavior

**Files:**
- Modify: `scripts/daily_ieee_digest.py`

- [ ] **Step 1: Extend `Candidate` with author and abstract fields**
- [ ] **Step 2: Parse Crossref `author` and `abstract` metadata**
- [ ] **Step 3: Reject entries with empty authors or non-paper title patterns**
- [ ] **Step 4: Update text and HTML email rendering to show authors and abstract text**

### Task 3: Update docs

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the old abstract-link-only description with authors + abstract delivery**
- [ ] **Step 2: Document the non-paper filtering rule at a high level**
