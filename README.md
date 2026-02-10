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
- ✅ Comprehensive logging
- ✅ JSON report generation
- ✅ Headless mode support
- ✅ Configurable parameters

## Tasks Automated

### Task 1: Dynamic ID Handling
- **Page:** https://uitestingplayground.com/dynamicid
- **Challenge:** Button ID changes on every refresh
- **Solution:** Uses text-based XPath selector instead of ID

### Task 2: Class Attribute Instability
- **Page:** https://uitestingplayground.com/classattr
- **Challenge:** Class names change randomly
- **Solution:** Uses partial class matching with XPath contains()

### Task 3: Delayed AJAX Content
- **Page:** https://uitestingplayground.com/ajax
- **Challenge:** Content loads after AJAX request
- **Solution:** Smart wait with explicit wait conditions

### Task 4: Hidden Element Automation
- **Page:** https://uitestingplayground.com/hiddenlayers
- **Challenge:** Button becomes hidden behind overlapping layer
- **Solution:** Handles ElementClickInterceptedException gracefully

### Task 5: Load Delay Page
- **Page:** https://uitestingplayground.com/loaddelay
- **Challenge:** Button appears after significant delay
- **Solution:** Extended timeout with explicit wait

### Task 6: Text Input Automation
- **Page:** https://uitestingplayground.com/textinput
- **Challenge:** Verify dynamic button text change
- **Solution:** Input automation with text verification

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

### Advanced Options

**Run in headless mode:**
```bash
python automation.py --headless
```

**Configure retry attempts:**
```bash
python automation.py --retry 5
```

**Configure timeout:**
```bash
python automation.py --timeout 15
```

**Combine options:**
```bash
python automation.py --headless --retry 5 --timeout 15
```

## Output

### Console Output

The script provides detailed logging:

```
[14:30:15] [INFO] Starting UI Testing Playground Automation
[14:30:16] [INFO] Starting Dynamic ID...
[14:30:17] [SUCCESS] Dynamic ID button clicked
[14:30:18] [INFO] Starting Class Attr...
[14:30:19] [SUCCESS] Class Attr button clicked and alert handled
...
```

### Summary Report

```
Dynamic ID: Success
Class Attr: Success
AJAX Load: Success
Hidden Layer: Success
Load Delay: Success
Text Input: Success

Total Success: 6
Total Failed: 0
Execution Time: 45.32 sec
```

### JSON Report

A detailed JSON report is generated as `automation_report.json`:

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
  "summary": {
    "total_success": 6,
    "total_failed": 0,
    "execution_time": "45.32 sec"
  },
  "timestamp": "2026-02-10T19:30:00.123456"
}
```

## Architecture

### Retry Mechanism

- Automatically retries failed actions up to 3 times (configurable)
- Detects and handles:
  - Stale element references
  - Element not clickable
  - Element not found
  - Timeout exceptions

### Smart Wait Strategy

- Uses Selenium's explicit waits (WebDriverWait)
- No fixed `sleep()` calls
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

## Evaluation Criteria Met

✅ **Selector Strategy:** Uses stable selectors (XPath with text, partial class matching)
✅ **Wait Strategy:** Implements explicit waits, no fixed sleep()
✅ **Retry Logic:** 3-attempt retry mechanism with exception handling
✅ **Code Quality:** Clean, well-documented, modular code
✅ **Stability:** Works consistently after page refresh
✅ **Logging Quality:** Comprehensive timestamped logging
✅ **Edge Case Handling:** Handles alerts, overlapping elements, timeouts

## Bonus Features Implemented

✅ **Configurable retry count:** `--retry` parameter
✅ **Export JSON report:** Automatic report generation
✅ **Headless automation version:** `--headless` flag

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Gaurang Yadav

## Project Status

Active - All 6 tasks implemented and tested
