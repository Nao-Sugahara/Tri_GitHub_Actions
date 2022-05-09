from selenium import webdriver
from selenium.webdriver.common.by import By


class ConfirmPageObject:

    def __init__(self, driver: webdriver):
        self.driver = driver

    def get_total_bill(self):
        """
        合計金額を取得する
        """
        return self.driver.find_element_by_id("total-bill").text.strip("合計 ""円（税込み）")