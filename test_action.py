from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class TestHotelPlanisphere(object):
    def setup_method(self):
        self.driver = webdriver.Chrome("./driver/chromedriver.exe")
        self.driver.maximize_window()

    def test_change_all_params(self):
        driver = self.driver
        driver.get("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0")

        # 画面の読み込みが終わるまで待機
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit-button"))
        )

        # 当日日付以前を設定すると予約できないこと
        # 前日を確認する
        d_today = datetime.today()
        d_yesterday = d_today + timedelta(days=-1)

        # 日付を入力する
        textbox = driver.find_element(By.ID, "date")
        textbox.clear()
        textbox.send_keys(d_yesterday.strftime("%Y/%m/%d"))

        # "宿泊数"に1を入力する
        textbox = driver.find_element(By.ID, "term")
        textbox.clear()
        textbox.send_keys("1")

        # "人数"に1を入力する
        textbox = driver.find_element(By.ID, "head-count")
        textbox.clear()
        textbox.send_keys("1")

        # サイト内の"お得な観光プラン"を選択する
        driver.find_element(By.ID, "sightseeing").click()

        # "指名"に名前を入力する
        textbox = driver.find_element(By.ID, "username")
        textbox.clear()
        textbox.send_keys("test1")

        # "希望しない"を選択する
        dropdown = Select(driver.find_element(By.ID, "contact"))
        dropdown.select_by_value("no")

        # 予約内容を確認するボタンをクリック
        driver.find_element(By.ID, "submit-button").click()

        # スクリーンショット取得（1）
        driver.save_screenshot("./ScreenShot/01_test_date_check.png")

        # 期待値チェック
        assert (
            driver.find_element(By.CSS_SELECTOR, "#date ~ div").text
            == "翌日以降の日付を入力してください。"
        ), "当日以前の日付を設定することができないこと"

        # 名前が空の状態では予約できないこと
        # 前日を確認する
        d_today = datetime.today()
        d_tomorrow = d_today + timedelta(days=+1)

        # 日付を入力する
        textbox = driver.find_element(By.ID, "date")
        textbox.clear()
        textbox.send_keys(d_tomorrow.strftime("%Y/%m/%d"))

        # "宿泊数"に1を入力する
        textbox = driver.find_element(By.ID, "term")
        textbox.clear()
        textbox.send_keys("1")

        # "人数"に1を入力する
        textbox = driver.find_element(By.ID, "head-count")
        textbox.clear()
        textbox.send_keys("1")

        # サイト内の"お得な観光プラン"を選択する
        driver.find_element(By.ID, "sightseeing").click()

        # "氏名"を空欄にする
        textbox = driver.find_element(By.ID, "username")
        textbox.clear()
        textbox.send_keys()

        # "希望しない"を選択する
        dropdown = Select(driver.find_element(By.ID, "contact"))
        dropdown.select_by_value("no")

        # 予約内容を確認するボタンをクリック
        driver.find_element(By.ID, "submit-button").click()

        # スクリーンショット取得（2）
        driver.save_screenshot("./ScreenShot/02_noname.png")

        # 確認
        assert (
            driver.find_element(By.CSS_SELECTOR, "#username ~ div").text
            == "このフィールドを入力してください。"
        ), "名前が空欄では予約ができないこと"

        # 3か月以上先の日付では予約できないこと
        # 前日を確認する
        d_today = datetime.today()
        d_threemonth = d_today + timedelta(days=+91)

        # 日付を入力する
        textbox = driver.find_element(By.ID, "date")
        textbox.clear()
        textbox.send_keys(d_threemonth.strftime("%Y/%m/%d"))

        # "宿泊数"に1を入力する
        textbox = driver.find_element(By.ID, "term")
        textbox.clear()
        textbox.send_keys("1")

        # "人数"に1を入力する
        textbox = driver.find_element(By.ID, "head-count")
        textbox.clear()
        textbox.send_keys("1")

        # サイト内の"お得な観光プラン"を選択する
        driver.find_element(By.ID, "sightseeing").click()

        # "指名"に名前を入力する
        textbox = driver.find_element(By.ID, "username")
        textbox.clear()
        textbox.send_keys("ベリ一郎")

        # "希望しない"を選択する
        dropdown = Select(driver.find_element(By.ID, "contact"))
        dropdown.select_by_value("no")

        # 予約内容を確認するボタンをクリック
        driver.find_element(By.ID, "submit-button").click()

        # スクリーンショット取得（3）
        driver.save_screenshot("./ScreenShot/03_test_three_month_later.png")

        # 確認
        assert (
            driver.find_element(By.CSS_SELECTOR, "#date ~ div").text
            == "3ヶ月以内の日付を入力してください。"
        ), "3か月以上先の日程では予約ができないこと"

    def teardown_method(self):
        self.driver.quit()
