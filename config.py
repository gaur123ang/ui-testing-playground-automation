"""Configuration file for automation parameters"""

# Browser Configuration
HEADLESS = False
BROWSER_TIMEOUT = 10

# Retry Configuration
RETRY_COUNT = 3
RETRY_DELAY = 0.5  # seconds

# Task URLs
URLs = {
    'dynamic_id': 'https://uitestingplayground.com/dynamicid',
    'class_attr': 'https://uitestingplayground.com/classattr',
    'ajax': 'https://uitestingplayground.com/ajax',
    'hidden_layers': 'https://uitestingplayground.com/hiddenlayers',
    'load_delay': 'https://uitestingplayground.com/loaddelay',
    'text_input': 'https://uitestingplayground.com/textinput'
}

# Test Data
TEST_TEXT_INPUT = "Automation Test"

# Report Configuration
REPORT_FILENAME = "automation_report.json"
SCREENSHOT_DIR = "screenshots"
