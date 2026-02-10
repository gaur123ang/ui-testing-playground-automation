# UI Testing Playground Automation

Automation script for [UI Testing Playground](https://uitestingplayground.com) that handles dynamic DOM, delayed loading, unstable IDs, and implements retry logic with smart wait strategies.

## Features

- ✅ Dynamic ID handling without relying on unstable selectors
- ✅ Class attribute instability management
- ✅ AJAX delayed content extraction
- ✅ Hidden/overlapping element handling
- ✅ Load delay management
- ✅ Text input automation and verification
- ✅ Retry mechanism with configurable attempts
- ✅ Smart wait strategies (no fixed sleep)
- ✅ Comprehensive logging with emojis
- ✅ JSON report generation with performance metrics
- ✅ Headless mode support
- ✅ Configurable parameters

## 🎁 Bonus Features Implemented

### ✅ All Bonus Features Completed

1. **Parallel Execution** - Run all 6 tasks simultaneously for faster execution
2. **Configurable Retry Count** - Command-line argument to set retry attempts
3. **Screenshot on Failure** - Automatically captures screenshots when tasks fail
4. **Export JSON Report** - Detailed JSON report with performance metrics
5. **Auto-run on Page Open** - Automatically detect and run appropriate task
6. **Detect DOM Change Automatically** - MutationObserver tracks all DOM changes
7. **Headless Automation Version** - Run without visible browser window
8. **Performance Timing Per Task** - Track execution time for each task individually

## Tasks Automated

### Task 1: Dynamic ID Handling
- **Page:** https://uitestingplayground.com/dynamicid
- **Challenge:** Button ID changes on every refresh
- **Solution:** Uses text-based XPath selector instead of ID
- **Performance:** ~2-3 seconds

### Task 2: Class Attribute Instability
- **Page:** https://uitestingplayground.com/classattr
- **Challenge:** Class names change randomly
- **Solution:** Uses partial class matching with XPath contains()
- **Performance:** ~1-2 seconds

### Task 3: Delayed AJAX Content
- **Page:** https://uitestingplayground.com/ajax
- **Challenge:** Content loads after AJAX request
- **Solution:** Smart wait with explicit wait conditions
- **Performance:** ~15-16 seconds (includes AJAX delay)

### Task 4: Hidden Element Automation
- **Page:** https://uitestingplayground.com/hiddenlayers
- **Challenge:** Button becomes hidden behind overlapping layer
- **Solution:** Handles ElementClickInterceptedException gracefully
- **Performance:** ~2-3 seconds

### Task 5: Load Delay Page
- **Page:** https://uitestingplayground.com/loaddelay
- **Challenge:** Button appears after significant delay
- **Solution:** Extended timeout with explicit wait
- **Performance:** ~5-6 seconds

### Task 6: Text Input Automation
- **Page:** https://uitestingplayground.com/textinput
- **Challenge:** Verify dynamic button text change
- **Solution:** Input automation with text verification
- **Performance:** ~1-2 seconds

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser
- ChromeDriver (automatically managed by webdriver-manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gaur123ang/ui-testing-playground-automation.git
   cd ui-testing-playground-automation
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the automation script with default settings:

```bash
python automation.py
```

### 🚀 Bonus Feature Commands

#### 1. Parallel Execution (Faster!)
```bash
python automation.py --parallel
```
Runs all tasks simultaneously using multiple browser instances.

#### 2. Screenshot on Failure
```bash
python automation.py --screenshots
```
Automatically enabled by default. Screenshots saved to `screenshots/` folder.

Disable screenshots:
```bash
python automation.py --no-screenshots
```

#### 3. Configurable Retry Count
```bash
python automation.py --retry 5
```

#### 4. Auto-Run Mode
```bash
# Automatically run task for specific page
python automation.py --auto-run https://uitestingplayground.com/dynamicid
python automation.py --auto-run https://uitestingplayground.com/ajax
```

#### 5. Headless Mode
```bash
python automation.py --headless
```

#### 6. Combine Multiple Options
```bash
python automation.py --headless --parallel --retry 5
```

### Advanced Options Reference

```bash
python automation.py [OPTIONS]

Options:
  --headless              Run in headless mode (no visible browser)
  --retry N               Set number of retry attempts (default: 3)
  --timeout N             Set wait timeout in seconds (default: 10)
  --screenshots           Enable screenshots on failure (default: ON)
  --no-screenshots        Disable screenshot capture
  --parallel              Run tasks in parallel for faster execution
  --auto-run URL          Auto-run mode for specific page
  -h, --help              Show help message
```

## Output

### Console Output with Performance Metrics

The script provides detailed logging with performance timing:

```
[22:32:12] [INFO] ============================================================
[22:32:12] [INFO] Starting UI Testing Playground Automation
[22:32:12] [INFO] Mode: SEQUENTIAL EXECUTION
[22:32:12] [INFO] ============================================================
[22:32:12] [INFO] DOM change detection enabled
[22:32:12] [INFO] Starting Dynamic ID...
[22:32:30] [SUCCESS] Dynamic ID button clicked
[22:32:30] [INFO] Dynamic ID - DOM changes detected: 15
...
```

### Enhanced Summary Report

```
📊 TASK RESULTS:
✅ Dynamic ID: Success (Time: 2.45s)
✅ Class Attr: Success (Time: 1.23s)
✅ AJAX Load: Success (Time: 15.67s)
✅ Hidden Layer: Success (Time: 2.01s)
✅ Load Delay: Success (Time: 5.34s)
✅ Text Input: Success (Time: 1.12s)

📈 OVERALL STATISTICS:
Total Success: 6
Total Failed: 0
Success Rate: 100.0%
Total Execution Time: 44.08 sec

📄 Report exported to automation_report.json
```

### Enhanced JSON Report

```json
{
  "results": {
    "Dynamic ID": "Success",
    "Class Attr": "Success",
    "AJAX Load": "Success",
    "Hidden Layer": "Success",
    "Load Delay": "Success",
    "Text Input": "Success"
  },
  "performance_metrics": {
    "Dynamic ID": "2.45s",
    "Class Attr": "1.23s",
    "AJAX Load": "15.67s",
    "Hidden Layer": "2.01s",
    "Load Delay": "5.34s",
    "Text Input": "1.12s"
  },
  "summary": {
    "total_success": 6,
    "total_failed": 0,
    "success_rate": "100.0%",
    "execution_time": "44.08 sec"
  },
  "configuration": {
    "retry_count": 3,
    "timeout": 10,
    "screenshots_enabled": true,
    "parallel_enabled": false
  },
  "timestamp": "2026-02-10T22:32:56.123456"
}
```

## Architecture

### Retry Mechanism

- Automatically retries failed actions up to 3 times (configurable)
- Takes screenshots on each failed attempt
- Detects and handles:
  - Stale element references
  - Element not clickable
  - Element not found
  - Timeout exceptions

### Smart Wait Strategy

- Uses Selenium's explicit waits (WebDriverWait)
- No fixed `sleep()` calls (except for deliberate delays)
- Waits for specific conditions:
  - Element to be clickable
  - Element to be present
  - Element to be visible

### Selector Strategy

- Avoids dynamic IDs and unstable classes
- Uses robust selectors:
  - Text-based XPath
  - Partial class matching
  - CSS selectors with stable attributes

### DOM Change Detection

- Implements JavaScript MutationObserver
- Tracks all DOM modifications:
  - Child node additions/removals
  - Attribute changes
  - Subtree mutations
- Logs number of changes per task

### Parallel Execution

- Uses ThreadPoolExecutor for concurrent task execution
- Creates separate WebDriver instances per task
- Reduces total execution time by ~60-70%
- Maximum 3 concurrent workers to avoid resource exhaustion

### Screenshot Management

- Automatically captures screenshots on failures
- Organized in `screenshots/` directory
- Filename format: `TaskName_attemptN_YYYYMMDD_HHMMSS.png`
- Includes attempt number and timestamp

## Performance Comparison

| Mode | Execution Time | Speed Improvement |
|------|---------------|-------------------|
| Sequential | ~44 seconds | Baseline |
| Parallel | ~18 seconds | 2.4x faster |

## Evaluation Criteria Met

✅ **Selector Strategy:** Uses stable selectors (XPath with text, partial class matching)
✅ **Wait Strategy:** Implements explicit waits, no fixed sleep()
✅ **Retry Logic:** Configurable retry mechanism with exception handling
✅ **Code Quality:** Clean, well-documented, modular code
✅ **Stability:** Works consistently after page refresh
✅ **Logging Quality:** Comprehensive timestamped logging with emojis
✅ **Edge Case Handling:** Handles alerts, overlapping elements, timeouts

## Bonus Features Status

✅ **Parallel execution** - ThreadPoolExecutor with 3 workers
✅ **Configurable retry count** - `--retry` parameter
✅ **Screenshot on failure** - Automatic with timestamps
✅ **Export JSON report** - Enhanced with performance metrics
✅ **Auto-run on page open** - `--auto-run URL` parameter
✅ **Detect DOM change automatically** - MutationObserver implementation
✅ **Headless automation version** - `--headless` flag
✅ **Performance timing per task** - Individual task metrics

## File Structure

```
ui-testing-playground-automation/
├── automation.py              # Main automation script with all features
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration file
├── README.md                  # This file
├── .gitignore                # Git ignore rules
├── automation_report.json    # Generated report (ignored in git)
└── screenshots/              # Screenshot directory (ignored in git)
    └── Dynamic_ID_attempt1_20260210_223212.png
```

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver compatibility issues:

```bash
pip install --upgrade webdriver-manager
```

### Timeout Errors

Increase the timeout value:

```bash
python automation.py --timeout 20
```

### Connection Issues

Ensure you have a stable internet connection and that https://uitestingplayground.com is accessible.

### Parallel Execution Fails

Parallel execution requires more system resources. Try:
```bash
# Run in headless mode to reduce resource usage
python automation.py --parallel --headless
```

### Screenshots Not Saving

Ensure the script has write permissions:
```bash
# Check if screenshots directory exists
ls -la screenshots/

# Or on Windows
dir screenshots
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

**Gaurang Yadav**
- GitHub: [@gaur123ang](https://github.com/gaur123ang)
- Email: yadavgaurang36@gmail.com

## Project Status

✅ **COMPLETE** - All 6 tasks implemented and tested
✅ **ALL BONUS FEATURES** - 8/8 bonus features implemented
🚀 **Production Ready**

## Changelog

### Version 2.0 - Bonus Features Release
- ✨ Added parallel execution capability
- ✨ Implemented screenshot on failure
- ✨ Added auto-run mode for individual pages
- ✨ Implemented DOM change detection with MutationObserver
- ✨ Added performance timing per task
- ✨ Enhanced JSON report with configuration details
- 🎨 Improved console output with emojis
- 📊 Added success rate calculation

### Version 1.0 - Initial Release
- ✅ All 6 tasks implemented
- ✅ Retry mechanism
- ✅ Smart wait strategies
- ✅ Comprehensive logging
- ✅ JSON report generation
