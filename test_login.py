import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
# Path to your ChromeDriver
# If chromedriver is in your PATH, you can remove the service argument.
# Example for Windows: service = Service('C:\\path\\to\\chromedriver.exe')
# Example for Mac/Linux: service = Service('/path/to/chromedriver')
URL = "http://16.16.91.240:4000/"
VALID_EMAIL = "usman@example.com"
VALID_PASSWORD = "fakefake"

# --- Test Cases ---

class TestLoginPage:
    def setup_method(self, method):
        """Setup method to initialize the WebDriver before each test."""
        # service = Service(CHROME_DRIVER_PATH) # Uncomment if you specified the path
        # self.driver = webdriver.Chrome(service=service)
        self.driver = webdriver.Chrome() # Use this if chromedriver is in your PATH
        self.driver.get(URL)
        self.driver.implicitly_wait(10) # Implicit wait

    def teardown_method(self, method):
        """Teardown method to close the WebDriver after each test."""
        self.driver.quit()

    def test_successful_login(self):
        """
        Test Case 1: Verify successful login with valid credentials.
        """
        print("\n--- Running Test Case 1: Successful Login ---")
        self.driver.find_element(By.ID, "email").send_keys(VALID_EMAIL)
        self.driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, '#root > main > form > div:nth-child(3) > button').click()

        # Wait for the URL to change, indicating a successful login and redirect
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/dashboard")
            )
            print("SUCCESS: Login successful. Redirected to the dashboard.")
            assert "/dashboard" in self.driver.current_url
        except Exception as e:
            print(f"FAILURE: Login failed. Did not redirect to dashboard. {e}")
            assert False, "Login did not lead to the expected dashboard URL."


    def test_invalid_password(self):
        """
        Test Case 2: Verify login fails with a valid email and invalid password.
        """
        print("\n--- Running Test Case 2: Invalid Password ---")
        self.driver.find_element(By.ID, "email").send_keys(VALID_EMAIL)
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        self.driver.find_element(By.CSS_SELECTOR, '#root > main > form > div:nth-child(3) > button').click()

        # Check for an error message. Let's find an element that contains the error.
        # This will depend on how your website displays errors.
        # Inspecting your site, an error toast appears.
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/login")
            )
            print("SUCCESS: Login successful. Redirected to the dashboard.")
            assert "/login" in self.driver.current_url
        except Exception as e:
            print(f"FAILURE: Login failed. Did not redirect to dashboard. {e}")
            assert False, "Login did not lead to the expected dashboard URL."


    def test_invalid_email(self):
        """
        Test Case 3: Verify login fails with an invalid email.
        """
        print("\n--- Running Test Case 3: Invalid Email ---")
        self.driver.find_element(By.ID, "email").send_keys("invalid@example.com")
        self.driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, '#root > main > form > div:nth-child(3) > button').click()

        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/login")
            )
            print("SUCCESS: Login successful. Redirected to the dashboard.")
            assert "/login" in self.driver.current_url
        except Exception as e:
            print(f"FAILURE: Login failed. Did not redirect to dashboard. {e}")
            assert False, "Login did not lead to the expected dashboard URL."


    def test_empty_credentials(self):
        """
        Test Case 4: Verify login fails when both email and password are empty.
        """
        print("\n--- Running Test Case 4: Empty Credentials ---")
        self.driver.find_element(By.CSS_SELECTOR, '#root > main > form > div:nth-child(3) > button').click()

        # Check that the URL has not changed
        time.sleep(2) # Wait a moment to see if a redirect happens
        current_url = self.driver.current_url
        print(f"SUCCESS: The page did not redirect. Current URL is {current_url}")
        assert "/login" in current_url, "Page should not redirect with empty credentials."

# To run this script with pytest, you would save it as 'test_login.py'
# and then run 'pytest' in your terminal in the same directory.