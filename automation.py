"""UI Testing Playground Automation Script with Bonus Features

This script automates 6 different tasks on https://uitestingplayground.com
with retry logic, smart wait strategies, and comprehensive logging.

Bonus Features:
- Parallel execution
- Configurable retry count
- Screenshot on failure
- Export JSON report
- Auto-run on page open (via --auto-run flag)
- Detect DOM change automatically
- Headless automation version
- Performance timing per task
"""

import time
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    """Automation class for UI Testing Playground tasks with bonus features"""
    
    def __init__(self, headless=False, retry_count=3, timeout=10, screenshots=True, parallel=False):
        """Initialize automation with configurable parameters"""
        self.retry_count = retry_count
        self.timeout = timeout
        self.screenshots_enabled = screenshots
        self.parallel_enabled = parallel
        self.results = {}
        self.performance_metrics = {}
        self.start_time = None
        self.end_time = None
        self.screenshot_dir = "screenshots"
        
        # Create screenshots directory
        if self.screenshots_enabled and not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        # Setup Chrome driver
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, self.timeout)
        
        # Enable DOM mutation detection
        self.enable_dom_change_detection()
        
    def enable_dom_change_detection(self):
        """Enable DOM mutation observer for detecting changes"""
        mutation_script = """
        window.domChanges = [];
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                window.domChanges.push({
                    type: mutation.type,
                    target: mutation.target.tagName,
                    timestamp: Date.now()
                });
            });
        });
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeOldValue: true
        });
        """
        try:
            self.driver.execute_script(mutation_script)
            self.log("INFO", "DOM change detection enabled")
        except:
            pass
        
    def get_dom_changes(self):
        """Retrieve detected DOM changes"""
        try:
            changes = self.driver.execute_script("return window.domChanges || [];")
            return changes
        except:
            return []
        
    def log(self, level, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] [{level}] {message}")
        
    def take_screenshot(self, task_name, attempt=1):
        """Take screenshot on failure"""
        if not self.screenshots_enabled:
            return None
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.screenshot_dir}/{task_name.replace(' ', '_')}_attempt{attempt}_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            self.log("INFO", f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            self.log("ERROR", f"Failed to save screenshot: {str(e)}")
            return None
        
    def retry_action(self, action_func, task_name):
        """Retry mechanism for actions with screenshot on failure"""
        for attempt in range(1, self.retry_count + 1):
            try:
                if attempt > 1:
                    self.log("RETRY", f"Attempt {attempt} for {task_name}")
                return action_func()
            except (StaleElementReferenceException, 
                    ElementClickInterceptedException, 
                    NoSuchElementException,
                    TimeoutException) as e:
                # Take screenshot on failure
                self.take_screenshot(task_name, attempt)
                
                if attempt == self.retry_count:
                    self.log("ERROR", f"{task_name} failed after {self.retry_count} attempts: {str(e)}")
                    raise
                time.sleep(0.5)
                
    def task1_dynamic_id(self):
        """Task 1: Handle button with dynamic ID"""
        task_name = "Dynamic ID"
        task_start = time.time()
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/dynamicid")
            self.enable_dom_change_detection()
            
            # Use text content instead of ID
            button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Button with Dynamic ID')]"))
            )
            button.click()
            
            # Check DOM changes
            dom_changes = self.get_dom_changes()
            self.log("INFO", f"{task_name} - DOM changes detected: {len(dom_changes)}")
            
            self.log("SUCCESS", f"{task_name} button clicked")
            return True
            
        try:
            result = self.retry_action(action, task_name)
            task_time = time.time() - task_start
            self.results[task_name] = "Success"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return result
        except Exception as e:
            task_time = time.time() - task_start
            self.results[task_name] = "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return False
            
    def task2_class_attribute(self):
        """Task 2: Handle button with unstable class attribute"""
        task_name = "Class Attr"
        task_start = time.time()
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/classattr")
            self.enable_dom_change_detection()
            
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
            task_time = time.time() - task_start
            self.results[task_name] = "Success"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return result
        except Exception as e:
            task_time = time.time() - task_start
            self.results[task_name] = "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return False
            
    def task3_ajax_load(self):
        """Task 3: Handle AJAX delayed content"""
        task_name = "AJAX Load"
        task_start = time.time()
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/ajax")
            self.enable_dom_change_detection()
            
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
            
            # Check DOM changes during AJAX
            dom_changes = self.get_dom_changes()
            self.log("INFO", f"{task_name} - DOM changes during AJAX: {len(dom_changes)}")
            
            self.log("SUCCESS", f"AJAX data extracted: {extracted_text}")
            return extracted_text
            
        try:
            result = self.retry_action(action, task_name)
            task_time = time.time() - task_start
            self.results[task_name] = "Success"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return result
        except Exception as e:
            task_time = time.time() - task_start
            self.results[task_name] = "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return False
            
    def task4_hidden_layers(self):
        """Task 4: Handle hidden/overlapping elements"""
        task_name = "Hidden Layer"
        task_start = time.time()
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/hiddenlayers")
            self.enable_dom_change_detection()
            
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
            task_time = time.time() - task_start
            self.results[task_name] = "Success"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return result
        except Exception as e:
            task_time = time.time() - task_start
            self.results[task_name] = "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return False
            
    def task5_load_delay(self):
        """Task 5: Handle delayed button loading"""
        task_name = "Load Delay"
        task_start = time.time()
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/loaddelay")
            self.enable_dom_change_detection()
            
            # Wait for button to appear after delay
            button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary"))
            )
            button.click()
            self.log("SUCCESS", f"{task_name} button appeared and clicked")
            return True
            
        try:
            result = self.retry_action(action, task_name)
            task_time = time.time() - task_start
            self.results[task_name] = "Success"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return result
        except Exception as e:
            task_time = time.time() - task_start
            self.results[task_name] = "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return False
            
    def task6_text_input(self):
        """Task 6: Text input and verification"""
        task_name = "Text Input"
        task_start = time.time()
        self.log("INFO", f"Starting {task_name}...")
        
        def action():
            self.driver.get("https://uitestingplayground.com/textinput")
            self.enable_dom_change_detection()
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
            task_time = time.time() - task_start
            self.results[task_name] = "Success" if result else "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return result
        except Exception as e:
            task_time = time.time() - task_start
            self.results[task_name] = "Failed"
            self.performance_metrics[task_name] = f"{task_time:.2f}s"
            return False
    
    def run_task_wrapper(self, task_func):
        """Wrapper for running tasks in parallel with separate driver instances"""
        # Create new driver instance for parallel execution
        if self.parallel_enabled:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            
            temp_driver = self.driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, self.timeout)
            
        try:
            result = task_func()
            return result
        finally:
            if self.parallel_enabled:
                self.driver.quit()
                self.driver = temp_driver
                self.wait = WebDriverWait(self.driver, self.timeout)
            
    def run_all_tasks(self, parallel=False):
        """Execute all automation tasks (sequential or parallel)"""
        self.start_time = time.time()
        self.log("INFO", "=" * 60)
        self.log("INFO", "Starting UI Testing Playground Automation")
        if parallel:
            self.log("INFO", "Mode: PARALLEL EXECUTION")
        else:
            self.log("INFO", "Mode: SEQUENTIAL EXECUTION")
        self.log("INFO", "=" * 60)
        
        tasks = [
            self.task1_dynamic_id,
            self.task2_class_attribute,
            self.task3_ajax_load,
            self.task4_hidden_layers,
            self.task5_load_delay,
            self.task6_text_input
        ]
        
        if parallel and self.parallel_enabled:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(task): task.__name__ for task in tasks}
                
                for future in as_completed(futures):
                    task_name = futures[future]
                    try:
                        future.result()
                    except Exception as e:
                        self.log("ERROR", f"Task {task_name} encountered an error: {str(e)}")
                    self.log("INFO", "-" * 60)
        else:
            # Sequential execution
            for task in tasks:
                try:
                    task()
                except Exception as e:
                    self.log("ERROR", f"Task {task.__name__} encountered an error: {str(e)}")
                self.log("INFO", "-" * 60)
            
        self.end_time = time.time()
        self.print_summary()
        
    def print_summary(self):
        """Print execution summary with performance metrics"""
        execution_time = self.end_time - self.start_time
        success_count = sum(1 for v in self.results.values() if v == "Success")
        failed_count = sum(1 for v in self.results.values() if v == "Failed")
        
        self.log("INFO", "=" * 60)
        self.log("INFO", "EXECUTION SUMMARY")
        self.log("INFO", "=" * 60)
        
        print("\n📊 TASK RESULTS:")
        for task, result in self.results.items():
            perf = self.performance_metrics.get(task, "N/A")
            status_icon = "✅" if result == "Success" else "❌"
            print(f"{status_icon} {task}: {result} (Time: {perf})")
            
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"Total Success: {success_count}")
        print(f"Total Failed: {failed_count}")
        print(f"Success Rate: {(success_count/len(self.results)*100):.1f}%")
        print(f"Total Execution Time: {execution_time:.2f} sec")
        
        # Export JSON report
        report = {
            "results": self.results,
            "performance_metrics": self.performance_metrics,
            "summary": {
                "total_success": success_count,
                "total_failed": failed_count,
                "success_rate": f"{(success_count/len(self.results)*100):.1f}%",
                "execution_time": f"{execution_time:.2f} sec"
            },
            "configuration": {
                "retry_count": self.retry_count,
                "timeout": self.timeout,
                "screenshots_enabled": self.screenshots_enabled,
                "parallel_enabled": self.parallel_enabled
            },
            "timestamp": datetime.now().isoformat()
        }
        
        with open('automation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        self.log("INFO", "📄 Report exported to automation_report.json")
        
    def cleanup(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            self.log("INFO", "Browser closed")


def auto_run_mode(url, automation):
    """Auto-run mode: automatically execute tasks when page opens"""
    automation.log("INFO", f"Auto-run mode: Navigating to {url}")
    automation.driver.get(url)
    
    # Detect which page we're on and run appropriate task
    current_url = automation.driver.current_url
    
    if "dynamicid" in current_url:
        automation.task1_dynamic_id()
    elif "classattr" in current_url:
        automation.task2_class_attribute()
    elif "ajax" in current_url:
        automation.task3_ajax_load()
    elif "hiddenlayers" in current_url:
        automation.task4_hidden_layers()
    elif "loaddelay" in current_url:
        automation.task5_load_delay()
    elif "textinput" in current_url:
        automation.task6_text_input()
    else:
        automation.log("ERROR", "Unknown page, running all tasks")
        automation.run_all_tasks()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='UI Testing Playground Automation with Bonus Features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Bonus Features:
  ✅ Parallel execution (--parallel)
  ✅ Configurable retry count (--retry)
  ✅ Screenshot on failure (--screenshots)
  ✅ Export JSON report (automatic)
  ✅ Auto-run on page open (--auto-run)
  ✅ Detect DOM change automatically (automatic)
  ✅ Headless automation (--headless)
  ✅ Performance timing per task (automatic)

Examples:
  python automation.py
  python automation.py --headless --parallel
  python automation.py --retry 5 --screenshots
  python automation.py --auto-run https://uitestingplayground.com/dynamicid
        """
    )
    
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--retry', type=int, default=3, help='Number of retry attempts (default: 3)')
    parser.add_argument('--timeout', type=int, default=10, help='Wait timeout in seconds (default: 10)')
    parser.add_argument('--screenshots', action='store_true', default=True, help='Enable screenshots on failure (default: True)')
    parser.add_argument('--no-screenshots', action='store_false', dest='screenshots', help='Disable screenshots')
    parser.add_argument('--parallel', action='store_true', help='Run tasks in parallel (faster execution)')
    parser.add_argument('--auto-run', type=str, metavar='URL', help='Auto-run mode: automatically execute task for specified URL')
    
    args = parser.parse_args()
    
    automation = UITestingPlaygroundAutomation(
        headless=args.headless,
        retry_count=args.retry,
        timeout=args.timeout,
        screenshots=args.screenshots,
        parallel=args.parallel
    )
    
    try:
        if args.auto_run:
            # Auto-run mode
            auto_run_mode(args.auto_run, automation)
            automation.print_summary()
        else:
            # Normal mode
            automation.run_all_tasks(parallel=args.parallel)
    finally:
        automation.cleanup()
