from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FormPageObject:

    def __init__(self, driver: webdriver):
        self.driver = driver

    def waite_until_clickable_button(self):
        """
        画面の読み込みが終わるまで待機
        """
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit-button")))

    def set_date_and_term(self, date, term):
        """
        宿泊日と日数を設定する
        """
        date_pick = self.driver.find_element(By.ID, "date")
        date_pick.clear()
        date_pick.send_keys(date)
        date_pick.send_keys(Keys.TAB)
        self.driver.find_element(By.ID, "term").send_keys(term)

    def set_headcount(self, headcount):
        """
        人数を入力する
        """
        head_count = self.driver.find_element(By.ID, "head-count")
        head_count.clear()
        head_count.send_keys(headcount)

    def select_plan(self, breakf: bool, early: bool, sight: bool):
        """
        プランを選択

        Args:
            breakf (bool): 朝食
            early (bool): 昼からチェックイン
            sight (bool): お得な観光プラン
        """
        break_fast = self.driver.find_element(By.ID, "breakfast")
        if break_fast.is_selected() != breakf:
            break_fast.click()

        early_checkin = self.driver.find_element(By.ID, "early-check-in")
        if early_checkin.is_selected() != early:
            early_checkin.click()

        sight_seeing = self.driver.find_element(By.ID, "sightseeing")
        if sight_seeing.is_selected() != sight:
            sight_seeing.click()

    def input_name(self, username):
        """
        名前を入力する
        """
        name = self.driver.find_element(By.ID, "username")
        name.clear()
        name.send_keys(username)

    def select_contact(self, value):
        """
        確認のご連絡を選択
        """
        dropdown = Select(self.driver.find_element(By.ID, "contact"))
        dropdown.select_by_value(value)

    def click_next(self):
        """
        予約内容を確認するボタンをクリック
        """
        self.driver.find_element(By.ID, "submit-button").click()
