# python配下自動でimport 
from selenium import webdriver
from selenium.webdriver.support.select import Select
import json
import time

username = "これユーザ名"
password = "これパスワード"

def lambda_handler(event, context):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--single-process")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=880x996")
        options.add_argument("--no-sandbox")
        options.add_argument("--homedir=/tmp")
        options.binary_location = "/opt/headless-chromium"
        
        #ブラウザの定義
        browser = webdriver.Chrome(
            "/opt/chromedriver",
            options=options
        )
        target_url = "https://lib02.tmd.ac.jp/webclass/login.php?id=065f1a02539273f1861a18045591bbf7&page=1"
        browser.get(target_url)
        username = browser.find_element_by_id("username")
        password = browser.find_element_by_id("password")
        username.send_keys(username)
        password.send_keys(password)
        login_button = browser.find_element_by_id("LoginBtn")
        time.sleep(0.5)
        login_button.click()
        #一覧まで開けた
        
        
        #<FRAME>というのを使っていてそのままでは動かないので、FRAMEのsrcを取得し、新たに開く
        frame = browser.find_elements_by_tag_name('FRAME')[1]
        src = frame.get_attribute("src")
        browser.get(src)
        start_button = browser.find_elements_by_name("next")[0]
        time.sleep(0.2)
        start_button.click()
        
        #もう一度FRAME
        frame = browser.find_elements_by_tag_name('FRAME')[2]
        src = frame.get_attribute("src")
        time.sleep(0.2)
        browser.get(src)
        
        #もし特記すべきことがなければ選択の自動化
        if 'n' == 'n':
            # 1.接触確認アプリ（COCOA）にて「陽性者との接触を確認」し、本日現時点での結果を下記より選び報告ください。
            dropdown = browser.find_element_by_name("dropdown__1[]")
            select = Select(dropdown)
            select.select_by_index(1)
        
            #ここらへんがなくなった
        
            # 5. 体温を選んでください。
            dropdown = browser.find_element_by_name("dropdown__2[]")
            select = Select(dropdown)
            select.select_by_index(1)
        
            # ↑ここまでdropdownの選択方式、ここからradio box
            # 設問 3体温測定前12時間以内に以下の薬剤を内服しましたか？
            element = browser.find_element_by_id("3_1")
            element.click()
        
            # 4. 以下の症状がある場合は、該当するものを選んでください。（複数選択できます）
            element = browser.find_element_by_id("4_1")
            element.click()
        
            # 5. 出席停止基準を満たしますか？次の1〜3のうち、該当するものを選んでください。（3の場合には速やかに教務係に連絡し、自宅療養してください）
            element = browser.find_element_by_id("5_1")
            element.click()
            
            #送信ボタンを押す(寸止めなし)
            element = browser.find_element_by_id("GradeBtn")
            time.sleep(3)
            element.click() 
            browser.quit() 
            print("でけた")
        return {
            'statusCode': 200,
            'body': json.dumps('Completed webclass!')
        }
    except:
        return {
            'statusCode': 500,
            'body': json.dumps('Fuuk')
        }