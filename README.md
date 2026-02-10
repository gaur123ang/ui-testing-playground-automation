# UI Testing Playground Automation

Automation script for [UI Testing Playground](https://uitestingplayground.com) that handles dynamic DOM, delayed loading, unstable IDs, and implements retry logic with smart wait strategies.


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
