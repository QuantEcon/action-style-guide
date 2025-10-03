# First-Time Setup Checklist

Use this checklist to get the QuantEcon Style Checker working for the first time.

## ☑️ Pre-Flight Check

- [ ] You have the `style-guide-database.md` file (43KB, contains all rules)
- [ ] You have a lecture file to check (markdown format)
- [ ] You've decided which method to use (see options below)

---

## 🚀 Option 1: Web Interface (Recommended for First Try)

**Time required**: 5 minutes  
**Setup required**: None  
**Cost**: Free tier available

### Steps

- [ ] **Step 1**: Go to [claude.ai](https://claude.ai)
- [ ] **Step 2**: Create account or log in (if needed)
- [ ] **Step 3**: Start a new conversation
- [ ] **Step 4**: Click the attachment button (📎)
- [ ] **Step 5**: Upload these three files:
  - [ ] `claude-style-checker-prompt.md`
  - [ ] `style-guide-database.md`
  - [ ] Your lecture file (or `quantecon-test-lecture.md` for testing)
- [ ] **Step 6**: Type and send this message:
  ```
  Please follow the instructions in claude-style-checker-prompt.md 
  to review the lecture against the style guide.
  ```
- [ ] **Step 7**: Wait for Claude's response (30-60 seconds)
- [ ] **Step 8**: Review the violations and suggested fixes

### ✅ Success Criteria
You should see a structured response with:
- Summary section with total violations
- Critical issues organized by category
- Specific fixes for each violation
- Recommendations summary

### 🐛 Troubleshooting
- **File upload fails**: Try smaller lecture file first
- **Claude says "I don't see the files"**: Re-upload them
- **Output is incomplete**: Ask Claude to continue
- **Too generic**: Make sure you uploaded the prompt file

---

## 🖥️ Option 2: Python Script (Best for Automation)

**Time required**: 10 minutes  
**Setup required**: Python 3.7+, pip, API key  
**Cost**: Pay per use (~$0.02-0.20 per lecture)

### Prerequisites

- [ ] Python 3.7 or higher installed
  ```bash
  python --version  # Should show 3.7+
  ```
- [ ] pip package manager working
  ```bash
  pip --version
  ```

### Steps

#### A. Get Claude API Key

- [ ] **A1**: Go to [console.anthropic.com](https://console.anthropic.com/)
- [ ] **A2**: Sign up or log in
- [ ] **A3**: Navigate to "API Keys"
- [ ] **A4**: Click "Create Key"
- [ ] **A5**: Copy the key (starts with `sk-ant-...`)
- [ ] **A6**: Save it securely (you won't see it again!)

#### B. Install Dependencies

- [ ] **B1**: Open terminal/command prompt
- [ ] **B2**: Navigate to the project directory:
  ```bash
  cd /path/to/prompt-experiments
  ```
- [ ] **B3**: Install the Anthropic SDK:
  ```bash
  pip install anthropic
  ```
- [ ] **B4**: Verify installation:
  ```bash
  python -c "import anthropic; print('OK')"
  ```
  Should print: `OK`

#### C. Configure API Key

Choose one method:

**Method 1: Environment Variable (Recommended)**
- [ ] **C1**: Set the API key:
  ```bash
  # macOS/Linux
  export ANTHROPIC_API_KEY='sk-ant-your-key-here'
  
  # Windows (Command Prompt)
  set ANTHROPIC_API_KEY=sk-ant-your-key-here
  
  # Windows (PowerShell)
  $env:ANTHROPIC_API_KEY='sk-ant-your-key-here'
  ```
- [ ] **C2**: Verify it's set:
  ```bash
  echo $ANTHROPIC_API_KEY
  ```

**Method 2: Pass to Script**
- [ ] Use `--api-key` flag when running (less secure, not recommended)

#### D. Test Run

- [ ] **D1**: Try with the test lecture:
  ```bash
  python style_checker.py quantecon-test-lecture.md
  ```
- [ ] **D2**: Wait for response (30-60 seconds)
- [ ] **D3**: Review the output in your terminal

#### E. Use on Real Lecture

- [ ] **E1**: Run on your lecture:
  ```bash
  python style_checker.py path/to/your/lecture.md
  ```
- [ ] **E2**: Save output to file:
  ```bash
  python style_checker.py your-lecture.md --output review.md
  ```
- [ ] **E3**: Review `review.md` file

### ✅ Success Criteria
- No errors during installation
- Script completes successfully
- Output shows structured review with violations
- Cost information displayed at end

### 🐛 Troubleshooting

**"anthropic module not found"**
- [ ] Run: `pip install anthropic` again
- [ ] Try: `python3 -m pip install anthropic`
- [ ] Check: You're using the right Python version

**"API key not set"**
- [ ] Verify key is in environment: `echo $ANTHROPIC_API_KEY`
- [ ] Try passing directly: `--api-key sk-ant-...`
- [ ] Check key is valid at console.anthropic.com

**"File not found"**
- [ ] Check you're in the right directory: `pwd`
- [ ] Use absolute paths: `/full/path/to/lecture.md`
- [ ] Verify file exists: `ls -l your-lecture.md`

**"Permission denied"**
- [ ] Make script executable: `chmod +x style_checker.py`
- [ ] Run with Python: `python style_checker.py ...`

**"Rate limit exceeded"**
- [ ] Wait a few minutes
- [ ] Check your API usage at console.anthropic.com
- [ ] Upgrade your plan if needed

---

## 📋 Option 3: Copy-Paste Method (No Account Needed)

**Time required**: 5 minutes  
**Setup required**: None  
**Cost**: Free tier available

### Steps

- [ ] **Step 1**: Go to [claude.ai](https://claude.ai)
- [ ] **Step 2**: Start a new conversation
- [ ] **Step 3**: Open `claude-style-checker-prompt.md` in a text editor
- [ ] **Step 4**: Copy the entire contents
- [ ] **Step 5**: Paste into Claude's chat box
- [ ] **Step 6**: Add a line: `## Style Guide Database`
- [ ] **Step 7**: Open `style-guide-database.md` and copy contents
- [ ] **Step 8**: Paste below the previous content
- [ ] **Step 9**: Add a line: `## Lecture to Review`
- [ ] **Step 10**: Open your lecture file and copy contents
- [ ] **Step 11**: Paste below the previous content
- [ ] **Step 12**: Send the message
- [ ] **Step 13**: Review Claude's response

### ✅ Success Criteria
Same as Option 1

### 🐛 Troubleshooting
- **Message too long**: Split the lecture into sections
- **Formatting issues**: Use plain text editor, not Word

---

## 🧪 Testing Your Setup

After setup, test with the intentional violations test file:

### Web or Copy-Paste Method
- [ ] Use `quantecon-test-lecture.md` instead of your lecture
- [ ] Verify Claude finds violations in all categories
- [ ] Check violations match the section headers in the test file

### Python Script Method
- [ ] Run: `python style_checker.py quantecon-test-lecture.md`
- [ ] Should find ~40+ violations
- [ ] Should detect issues in Writing, Math, Code, Figures, etc.

---

## 📚 Next Steps After Setup

Once you have it working:

- [ ] Read [QUICK-START.md](QUICK-START.md) for tips
- [ ] Check [example-interactions.md](example-interactions.md) for advanced usage
- [ ] Try different focus modes (e.g., `--focus writing`)
- [ ] Integrate into your workflow

---

## 💡 Tips for Success

### First Review
- [ ] Start with a small lecture (500-1000 lines)
- [ ] Use quick mode first: `--quick` or ask Claude for "top 5 issues only"
- [ ] Don't be overwhelmed by the violation count
- [ ] Focus on one category at a time

### Understanding Output
- [ ] Read the Summary section first
- [ ] Start with Critical Issues (rule violations)
- [ ] Save Style Suggestions for later
- [ ] Use the Recommendations Summary to prioritize

### Applying Fixes
- [ ] Copy the "Suggested fix" text exactly
- [ ] Replace the "Current" text in your lecture
- [ ] Save the file
- [ ] Re-run the checker to verify

### Iterative Improvement
- [ ] Fix major issues first (paragraph structure, capitalization)
- [ ] Re-check after fixes
- [ ] Then address style suggestions
- [ ] Do a final comprehensive check

---

## 🎯 Completion Checklist

You're ready to use the style checker when you can:

- [ ] Run a review (via web or script)
- [ ] Get structured output with violations
- [ ] Understand the violation format
- [ ] Apply a suggested fix to your lecture
- [ ] Re-run to verify the fix worked

---

## 📞 Getting Help

If you're stuck:

1. **Check the troubleshooting sections above** ↑
2. **Review [usage-guide.md](usage-guide.md)** for detailed explanations
3. **Look at [example-interactions.md](example-interactions.md)** for examples
4. **Try the test lecture** (`quantecon-test-lecture.md`) to verify setup

---

## ⏱️ Time Estimates

| Task | Web Interface | Python Script |
|------|---------------|---------------|
| First-time setup | 5 min | 10 min |
| Check one lecture | 2 min | 1 min |
| Review output | 5-10 min | 5-10 min |
| Apply fixes | 15-60 min | 15-60 min |
| Re-check | 2 min | 1 min |
| **Total first session** | **~30-80 min** | **~30-85 min** |

After the first time, subsequent checks take just 2-3 minutes.

---

## 💰 Cost Estimates

| Lecture Size | Lines | Web (Free Tier) | API Cost |
|--------------|-------|-----------------|----------|
| Small | 500 | Usually free | $0.01-0.03 |
| Medium | 1500 | Usually free | $0.03-0.08 |
| Large | 3000 | May require paid | $0.08-0.15 |
| Very Large | 5000+ | Requires paid | $0.15-0.25 |

Web interface may have daily limits on free tier.

---

**Ready to start?** ✅

Pick your method:
- **Quick test**: Use Option 1 (Web Interface) with `quantecon-test-lecture.md`
- **Production use**: Set up Option 2 (Python Script)
- **No account**: Use Option 3 (Copy-Paste)

Good luck! 🚀
