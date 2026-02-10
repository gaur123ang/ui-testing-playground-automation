"""UI Testing Playground Automation Script

This script automates 6 different tasks on https://uitestingplayground.com
with retry logic, smart wait strategies, and comprehensive logging.
"""

import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)
from selenium.webdriver.chrome.options import Options


class UITestingPlaygroundAutomation:
    """Automation class for UI Testing Playground tasks"""
    
    def __init__(self, headless=False, retry_count=3, timeout=10):
        """Initialize automation with configurable parameters"""
        self.retry_count = retry_count
        self.timeout = timeout
        self.results = {}
        self.start_time = None
        self.end_time = None
        
        # Setup Chrome driver
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, self.timeout)
        
    def log(self, level, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")
        
    def retry_action(self, action_func, task_name):
        """Retry mechanism for actions"""
        for attempt in range(1, self.retry_count + 1):
            try:
                if attempt > 1:
                    self.log("RETRY", f"Attempt {attempt} for {task_name}")
                return action_func()
            except (StaleElementReferenceException, 
                    ElementClickInterceptedException, 
                    NoSuchElementException,
                    TimeoutException) as e:
                if attempt == self.retry_count:
                    self.log("ERROR", f"{task_name} failed after {self.retry_count} attempts: {str(e)}")
                    raise
                time.sleep(0.5)
                
    def task1_dynamic_id(self):
        """Task 1: Handle button with dynamic ID"""
        task_name = "Dynamic ID"
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/dynamicid")
            # Use text content instead of ID
            button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Button with Dynamic ID')]"))
            )
            button.click()
            self.log("SUCCESS", f"{task_name} button clicked")
            return True
            
        try:
            result = self.retry_action(action, task_name)
            self.results[task_name] = "Success"
            return result
        except Exception as e:
            self.results[task_name] = "Failed"
            return False
            
    def task2_class_attribute(self):
        """Task 2: Handle button with unstable class attribute"""
        task_name = "Class Attr"
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/classattr")
            # Use contains for class match to handle changing classes
            button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(concat(' ', normalize-space(@class), ' '), ' btn-primary ')]"))
            )
            button.click()
            # Handle alert
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                self.log("SUCCESS", f"{task_name} button clicked and alert handled")
            except:
                self.log("SUCCESS", f"{task_name} button clicked")
            return True
            
        try:
            result = self.retry_action(action, task_name)
            self.results[task_name] = "Success"
            return result
        except Exception as e:
            self.results[task_name] = "Failed"
            return False
            
    def task3_ajax_load(self):
        """Task 3: Handle AJAX delayed content"""
        task_name = "AJAX Load"
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/ajax")
            # Click AJAX trigger button
            button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "ajaxButton"))
            )
            button.click()
            self.log("INFO", "AJAX button clicked, waiting for content...")
            
            # Wait for AJAX content to load (with extended timeout)
            content = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#content p.bg-success"))
            )
            extracted_text = content.text
            self.log("SUCCESS", f"AJAX data extracted: {extracted_text}")
            return extracted_text
            
        try:
            result = self.retry_action(action, task_name)
            self.results[task_name] = "Success"
            return result
        except Exception as e:
            self.results[task_name] = "Failed"
            return False
            
    def task4_hidden_layers(self):
        """Task 4: Handle hidden/overlapping elements"""
        task_name = "Hidden Layer"
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/hiddenlayers")
            # Click the green button
            button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "greenButton"))
            )
            button.click()
            self.log("SUCCESS", f"{task_name} - First click successful")
            
            # Try to click again (this should fail due to overlapping layer)
            try:
                time.sleep(0.5)  # Brief wait for layer to appear
                button.click()
                self.log("SUCCESS", f"{task_name} - Second click successful (unexpected)")
            except ElementClickInterceptedException:
                self.log("INFO", f"{task_name} - Second click blocked as expected by overlapping layer")
            
            return True
            
        try:
            result = self.retry_action(action, task_name)
            self.results[task_name] = "Success"
            return result
        except Exception as e:
            self.results[task_name] = "Failed"
            return False
            
    def task5_load_delay(self):
        """Task 5: Handle delayed button loading"""
        task_name = "Load Delay"
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/loaddelay")
            # Wait for button to appear after delay
            button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
            )
            button.click()
            self.log("SUCCESS", f"{task_name} button appeared and clicked")
            return True
            
        try:
            result = self.retry_action(action, task_name)
            self.results[task_name] = "Success"
            return result
        except Exception as e:
            self.results[task_name] = "Failed"
            return False
            
    def task6_text_input(self):
        """Task 6: Text input and verification"""
        task_name = "Text Input"
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/textinput")
            test_text = "Automation Test"
            
            # Enter text in input field
            input_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "newButtonName"))
            )
            input_field.clear()
            input_field.send_keys(test_text)
            self.log("INFO", f"Entered text: {test_text}")
            
            # Click update button
            button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "updatingButton"))
            )
            button.click()
            
            # Verify button text changed
            updated_text = button.text
            if updated_text == test_text:
                self.log("SUCCESS", f"{task_name} - Button text updated to: {updated_text}")
                return True
            else:
                self.log("ERROR", f"{task_name} - Button text mismatch: expected '{test_text}', got '{updated_text}'")
                return False
                
        try:
            result = self.retry_action(action, task_name)
            self.results[task_name] = "Success" if result else "Failed"
            return result
        except Exception as e:
            self.results[task_name] = "Failed"
            return False
            
    def run_all_tasks(self):
        """Execute all automation tasks"""
        self.start_time = time.time()
        self.log("INFO", "=" * 60)
        self.log("INFO", "Starting UI Testing Playground Automation")
        self.log("INFO", "=" * 60)
        
        tasks = [
            self.task1_dynamic_id,
            self.task2_class_attribute,
            self.task3_ajax_load,
            self.task4_hidden_layers,
            self.task5_load_delay,
            self.task6_text_input
        ]
        
        for task in tasks:
            try:
                task()
            except Exception as e:
                self.log("ERROR", f"Task {task.__name__} encountered an error: {str(e)}")
            self.log("INFO", "-" * 60)
            
        self.end_time = time.time()
        self.print_summary()
        
    def print_summary(self):
        """Print execution summary"""
        execution_time = self.end_time - self.start_time
        success_count = sum(1 for v in self.results.values() if v == "Success")
        failed_count = sum(1 for v in self.results.values() if v == "Failed")
        
        self.log("INFO", "=" * 60)
        self.log("INFO", "EXECUTION SUMMARY")
        self.log("INFO", "=" * 60)
        
        for task, result in self.results.items():
            print(f"{task}: {result}")
            
        print(f"\nTotal Success: {success_count}")
        print(f"Total Failed: {failed_count}")
        print(f"Execution Time: {execution_time:.2f} sec")
        
        # Export JSON report
        report = {
            "results": self.results,
            "summary": {
                "total_success": success_count,
                "total_failed": failed_count,
                "execution_time": f"{execution_time:.2f} sec"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open('automation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        self.log("INFO", "Report exported to automation_report.json")
        
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            self.log("INFO", "Browser closed")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='UI Testing Playground Automation')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--retry', type=int, default=3, help='Number of retry attempts (default: 3)')
    parser.add_argument('--timeout', type=int, default=10, help='Wait timeout in seconds (default: 10)')
    
    args = parser.parse_args()
    
    automation = UITestingPlaygroundAutomation(
        headless=args.headless,
        retry_count=args.retry,
        timeout=args.timeout
    )
    
    try:
        automation.run_all_tasks()
    finally:
        automation.cleanup()
