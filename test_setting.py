import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- Configuration ---
BASE_URL = "https://the-wild-oasis-omega-one.vercel.app/"
VALID_EMAIL = "usman@example.com"
VALID_PASSWORD = "fakefake"


class TestUpdateSettingsForm:
    """
    Test suite for the Update Settings Form.
    Uses user-like navigation (clicks) instead of direct URL access.
    """

    def setup_method(self, method):
        """
        Initializes the WebDriver, performs a login, and then CLICKS
        to navigate to the settings page.
        """
        # 1. Initialize WebDriver and perform Login
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        print("\n--- Performing Login ---")
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "email").send_keys(VALID_EMAIL)
        self.driver.find_element(By.ID, "password").send_keys(VALID_PASSWORD)
        self.driver.find_element(By.CSS_SELECTOR, '#root > main > form > div:nth-child(3) > button').click()

        try:
            # 2. Wait for login to complete and dashboard to load
            WebDriverWait(self.driver, 10).until(EC.url_contains("dashboard"))
            print("Login successful.")
        except TimeoutException:
            self.driver.quit()
            pytest.fail("Login failed. Could not proceed.")

        # 3. THE FIX: Navigate by clicking the settings link, not using driver.get()
        print("Navigating to settings page by clicking the link...")
        try:
            # IMPORTANT: You may need to change this selector to match your app.
            # Common examples: a[href='/settings'], button containing 'Settings', etc.
            settings_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[1]/aside/nav/ul/li[5]/a'))
            )
            settings_link.click()

            # 4. Wait for the settings page to be fully loaded
            # We confirm this by waiting for one of the form fields to be visible.
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "min-nights"))
            )
            print("Successfully navigated to the settings page.")

        except TimeoutException:
            self.driver.quit()
            pytest.fail("Could not find or click the settings link, or the settings page did not load.")

    def teardown_method(self, method):
        """Closes the WebDriver after each test."""
        self.driver.quit()

    def _update_field_and_check_for_alert(self, field_id: str, new_value: str):
        """Helper function to update a field and check for an alert."""
        try:
            field = self.driver.find_element(By.ID, field_id)
            field.clear()
            field.send_keys(new_value)
            self.driver.find_element(By.TAG_NAME, "body").click()
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())

            print(f"SUCCESS: An alert was detected after updating '{field_id}'.")
            alert = self.driver.switch_to.alert
            alert.accept()
            assert True

        except NoSuchElementException:
            pytest.fail(f"Test setup failed: element '{field_id}' not found on the settings page.")
        except TimeoutException:
            pytest.fail(f"Update for '{field_id}' did not trigger a success alert.")
        except Exception as e:
            pytest.fail(f"An unexpected error occurred for '{field_id}': {e}")

    def test_update_min_nights(self):
        """Tests updating the 'Minimum nights/booking' field."""
        print("--- Running Test: Update Minimum Nights ---")
        self._update_field_and_check_for_alert("min-nights", "5")

    def test_update_max_nights(self):
        """Tests updating the 'Maximum nights/booking' field."""
        print("--- Running Test: Update Maximum Nights ---")
        self._update_field_and_check_for_alert("max-nights", "100")

    def test_update_max_guests(self):
        """Tests updating the 'Maximum guests/booking' field."""
        print("--- Running Test: Update Maximum Guests ---")
        self._update_field_and_check_for_alert("max-guests", "20")

    def test_update_breakfast_price(self):
        """Tests updating the 'Breakfast price' field."""
        print("--- Running Test: Update Breakfast Price ---")
        self._update_field_and_check_for_alert("breakfast-price", "30")