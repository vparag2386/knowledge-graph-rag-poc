# PyCharm Configuration

If you're having import issues in PyCharm, follow these steps:

## Method 1: Mark Directory as Sources Root (Recommended)

1. Right-click on the `rag_agent` folder in PyCharm's Project view
2. Select **Mark Directory as** → **Sources Root**
3. Run the scripts again

## Method 2: Configure Python Interpreter

1. Go to **File** → **Settings** (or **PyCharm** → **Preferences** on Mac)
2. Navigate to **Project: knowledge-graph-rag-poc** → **Python Interpreter**
3. Make sure the virtual environment `venv` is selected
4. Click **OK**

## Method 3: Add to PYTHONPATH

1. Right-click on the project root in PyCharm
2. Select **Mark Directory as** → **Sources Root**

## Running Scripts in PyCharm

### Option 1: Run Configuration
1. Right-click on `test_wikipedia.py`
2. Select **Run 'test_wikipedia'**

### Option 2: Terminal
1. Open PyCharm's terminal (bottom panel)
2. Run:
   ```bash
   python test_wikipedia.py
   ```

## Troubleshooting

If you still see import errors:
1. **Invalidate Caches**: File → Invalidate Caches / Restart
2. **Rebuild Project**: Build → Rebuild Project
3. **Check Interpreter**: Make sure `venv` is selected as the Python interpreter

The scripts now have dual import support and should work in both PyCharm and command line!
