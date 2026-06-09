# Streamlit Environment Troubleshooting Notes

## What happened

- Your `python` is aliased to `/usr/bin/python3` (Xcode's Python 3.9), so `python -m venv venv` built the venv on **Xcode Python 3.9**.
- The `externally-managed-environment` error came from running `pip install` **without a venv active** (against Homebrew's Python). That's PEP 668 protecting the system Python — expected.
- The `No module named streamlit` error inside the venv just means **streamlit was never actually installed into the venv yet**. The venv works fine; it's just empty.
- On top of that, conda `(base)` is also active, which muddies which Python wins.

## Cleanest fix

Recreate the venv on your Homebrew Python 3.13 and install into it. Run these **one at a time**:

```bash
# 1. Get out of conda base and the broken venv
conda deactivate
deactivate 2>/dev/null

# 2. Remove the old venv (built on Xcode 3.9)
rm -rf venv

# 3. Create a fresh venv with Homebrew Python 3.13 explicitly
/opt/homebrew/bin/python3 -m venv venv

# 4. Activate it
source venv/bin/activate

# 5. Install requirements INTO the venv
pip install -r requirements.txt

# 6. Run the app
streamlit run app.py
```

**The key rule:** only install *after* `source venv/bin/activate`, and use `streamlit run app.py` directly once it's installed (the venv puts `streamlit` on your PATH).

---

## Understanding the error: `ModuleNotFoundError: No module named 'streamlit'`

This is a three-column note — an **error → cause → fix** entry. Reading across:

| Column | Meaning |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | **The error** Python threw |
| `Not in the right environment` | **The cause** — Python can't find streamlit because it's looking in a Python environment where streamlit was never installed |
| `Make sure your virtual environment is activated before running.` | **The fix** — activate the venv (where streamlit lives) before running the app |

### In plain terms

Streamlit isn't installed **globally** on your machine — it's (supposed to be) installed **inside your project's virtual environment**. When you run Python without that venv activated, Python uses a different interpreter that has no idea streamlit exists, so it errors.

The reason you got the error even *with* `(venv)` showing was that streamlit hadn't actually been installed into that venv yet — the install step kept failing or running against the wrong Python.

### The fix in two parts

1. Activate the venv → `source venv/bin/activate`
2. Make sure streamlit is actually installed in it → `pip install -r requirements.txt`

Then `streamlit run app.py` will find it.
