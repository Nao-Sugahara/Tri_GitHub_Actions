import pytest
from selenium import webdriver

from pages import confirm, form
from utilities.read_csv import read_csv_data


class TestDataDriven:

    datalist = read_csv_data("./drivers/")
    print(datalist)

    @classmethod
    def setup_class(cls):
        cls.driver = webdriver.Chrome("./data/reservation.csv")
        cls.driver.maximize_window()

    def setup_method(self):
        self.driver.get("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0")

    @pytest.mark.parametrize(
        "case_no,date_from,days,headcount,breakfast,early_checkin,sightseeing,username,contact,total",datalist,)
    
    def test_reserve_multi(self,case_no,date_from,days,headcount,breakfast,early_checkin,sightseeing,username,contact,total,):
        driver = self.driver

        # 待機する
        form_page = form.FormPageObject(driver)
        form_page.waite_until_clickable_button()

        # 宿泊日を入力
        form_page.set_date_and_term(date_from, days)

        # 人数を入力
        form_page.set_headcount(headcount)

        # プランを選択
        breakf = True if breakfast == "あり" else False
        early = True if early_checkin == "あり" else False
        sight = True if sightseeing == "あり" else False
        form_page.select_plan(breakf, early, sight)

        # お名前を入力
        form_page.input_name(username)

        # 確認のご連絡を選択
        form_page.select_contact(contact)

        # 予約内容を確認するボタンをクリック
        form_page.click_next()

        # スクリーンショットを保存
        driver.save_screenshot("./images/screenshot1.png")

        # 価格が168000円かどうかを確認
        confirm_page = confirm.ConfirmPageObject(self.driver)
        assert confirm_page.get_total_bill() == total, "合計が" + total + "円であること"

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
