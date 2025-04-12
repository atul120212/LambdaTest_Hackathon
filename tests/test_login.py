import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
# 🔧 Setup WebDriver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Or use Firefox/Edge
    driver.get("https://www.saucedemo.com/")
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# ✅ Valid login test (standard_user)
def test_valid_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    logging.info("Login successful")
    assert "inventory.html" in driver.current_url, "Login failed for valid user."

# Check for empty username error 

def test_blank_username_password(driver):
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CLASS_NAME, "error-message-container").text
    logging.info(f"Error message: {error}")
    assert "Epic sadface" in error or "Username is required" in error, "Error message not displayed correctly"
    assert "Password is required" in error or "Epic sadface" in error, "Error message not displayed correctly"
    assert "Username is required" in error
              



# ❌ Invalid login test (wrong password)
def test_invalid_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CLASS_NAME, "error-message-container").text
    logging.info(f"Error message: {error}")
    assert "Epic sadface" in error or "Username and password do not match" in error, "Error message not displayed correctly"
    #assert "Username and password do not match" in error or "Epic sadface" in error, "Error message not displayed correctly"
    assert "Username and password do not match" in error or "Epic sadface" in error

# 🚫 Locked out user test
def test_locked_out_user(driver):
    driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    error = driver.find_element(By.CLASS_NAME, "error-message-container").text
    logging.info(f"Error message: {error}")
    assert "Epic sadface" in error or "locked out" in error, "Error message not displayed correctly"

    assert "locked out" in error.lower()

# 🛡️ SQL Injection test (should fail to login)
def test_sql_injection_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("' OR '1'='1")
    driver.find_element(By.ID, "password").send_keys("' OR '1'='1")
    driver.find_element(By.ID, "login-button").click()
    logging.info("Attempting SQL injection login")
    assert "inventory.html" not in driver.current_url, "SQL injection succeeded (should fail)"


#🧬 XSS Injection Test
def test_xss_injection(driver):
    driver.find_element(By.ID, "user-name").send_keys("<script>alert('xss')</script>")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    logging.info("Attempting XSS injection login")
    assert "inventory.html" not in driver.current_url


#🔁 Repeated Failed Login (Brute Force Simulation)

@pytest.mark.parametrize("i", range(5))
def test_multiple_failed_logins(driver, i):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys(f"wrong_pass{i}")
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CLASS_NAME, "error-message-container").text
    logging.info(f"Error message: {error}")
    assert "Epic sadface" in error

#HTML Injection Test

def test_html_injection(driver):
    driver.find_element(By.ID, "user-name").send_keys("<b>user</b>")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    logging.info("Attempting HTML injection login")
    assert "inventory.html" not in driver.current_url

#JavaScript URI Injection

def test_javascript_uri_injection(driver):
    driver.find_element(By.ID, "user-name").send_keys("javascript:alert('Hacked')")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    logging.info("Attempting JavaScript URI injection login")
    assert "inventory.html" not in driver.current_url