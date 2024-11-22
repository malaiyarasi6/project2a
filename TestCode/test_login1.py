import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from TestData.data import TestSelectors
from TestData.data import TestData

class TestOrangeHRM:
    @pytest.fixture(scope="module")
    def driver(self):
        """Fixture to initialize and quit WebDriver."""
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()

    def login_as_admin(self, driver, username=TestData.username, password=TestData.password):
        """Helper function to log in as Admin."""
        try:
            driver.get(TestData.url)
            wait=WebDriverWait(driver, 10)
            
            wait.until(EC.presence_of_element_located((By.NAME, "Username"))).send_keys(username)
            wait.until(EC.presence_of_element_located((By.NAME, "Password"))).send_keys(password)
            wait.until(EC.element_to_be_clickable((By.NAME, "btnLogin"))).click()

            
            wait.until(EC.url_changes("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index"))
        except TimeoutException:
            print("Login fields not found or login timed out.")

    def test_forget_password(self, driver):
        """Test Case 1: Launch URL and Click Forgot Password."""
        driver.get(TestData.url)
        try:
            forgot_password = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Forgot your password?"))
            )
            forgot_password.click()
            assert "resetPassword" in driver.current_url, "Forgot Password page did not load correctly."
        except TimeoutException:
            print("Forgot Password link not found or timed out.")

    def test_validate_admin_menus(self, driver):
        """Test Case 2: Validate Menu Options on Admin Page."""
        self.login_as_admin(driver)
        try:
            menu_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='mainMenuFirstLevelUnorderedList']/li"))
            )
            displayed_menus = [menu.text for menu in menu_elements]
            
            for menu in TestData.expected_menus:
                assert menu in displayed_menus, f"{menu} menu option is missing!"
        except TimeoutException:
            print("Main menu options not found or timed out.")

    def test_validate_admin_submenus(self, driver):
        """Test Case 3: Validate Submenus Under Admin."""
        self.login_as_admin(driver)
        try:
            driver.find_element(By.ID, "menu_admin_viewAdminModule").click()
            
            submenu_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='menu']/ul/li/a"))
            )
            displayed_submenus = [submenu.text for submenu in submenu_elements]
            print(displayed_submenus)
            
            for submenu in TestData.expected_submenus:
                assert submenu in displayed_submenus, f"{submenu} submenu option is missing!"
        except TimeoutException:
            print("Admin submenu options not found or timed out.")
