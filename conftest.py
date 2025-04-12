import pytest
import logging
from selenium import webdriver
import os
from dotenv import load_dotenv
from datetime import datetime
from multiprocessing import current_process
# Load .env for LambdaTest credentials
load_dotenv()


LT_USERNAME = os.getenv("LT_USERNAME")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")

# Set up logging
def pytest_configure(config):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    process_id = current_process().pid
    log_filename = f"logs/test_log_{now}_{process_id}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filename, mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.info(f"Logging started in process {process_id}")

@pytest.fixture(params=["desktop", "mobile"])
def driver(request):
    device_type = request.param
    test_name = request.node.name

    logging.info(f"==== Starting test: {test_name} on {device_type.upper()} ====")

    if device_type == "desktop":
        capabilities = {
            "build": "Login Test - Desktop",
            "name": test_name,
            "platform": "Windows 11",
            "browserName": "Chrome",
            "version": "latest",
            "selenium_version": "4.0.0"
        }
    else:
        capabilities = {
            "build": "Login Test - Mobile",
            "name": test_name,
            "platformName": "iOS",
            "deviceName": "iPhone 14",
            "platformVersion": "16",
            "browserName": "Safari",
            "realMobile": "true"
        }

    grid_url = f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@hub.lambdatest.com/wd/hub"

    try:
        driver = webdriver.Remote(
            command_executor=grid_url,
            desired_capabilities=capabilities
        )
        driver.get("https://www.saucedemo.com/")
        driver.implicitly_wait(10)
    except Exception as e:
        logging.error(f"Failed to start browser on {device_type.upper()}: {e}")
        raise

    yield driver

    driver.quit()
    logging.info(f"==== Finished test: {test_name} on {device_type.upper()} ====")