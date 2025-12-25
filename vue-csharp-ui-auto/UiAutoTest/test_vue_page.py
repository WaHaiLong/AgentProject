from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pytest
import time

# 1. 前置：校验C#后端接口是否可用（避免因后端问题导致UI测试失败）
def check_csharp_api():
    try:
        # C# 后端测试环境接口地址
        response = requests.get("http://localhost:5000/api/health")
        assert response.status_code == 200, "C# 后端接口不可用！"
        print("C# 后端接口校验通过")
        return True
    except Exception as e:
        print(f"后端接口校验失败：{str(e)}")
        return False

# 2. 配置Chrome无头模式（适配GitHub Actions无界面环境）
def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # 适配Chrome驱动路径
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # 隐式等待
    return driver

# 3. 核心测试用例：Vue登录页面 + C#接口联动
def test_vue_login_with_csharp_api():
    # 先校验后端接口
    assert check_csharp_api(), "后端接口不可用，测试终止"
    
    driver = get_chrome_driver()
    try:
        # 打开Vue前端登录页面
        driver.get("http://localhost:8080/login")
        
        # 等待页面加载完成
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='login-username']"))
        )
        
        # 定位登录表单元素（使用data-testid属性，便于测试）
        username_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='login-username']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='login-password']")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-submit-btn']")
        
        # 输入测试数据（需与C#后端测试账号一致）
        username_input.send_keys("test_user")
        password_input.send_keys("test_pass123")
        login_btn.click()
        
        # 验证登录成功：等待跳转到首页
        WebDriverWait(driver, 15).until(
            EC.url_contains("/home")  # 验证跳转到首页
        )
        
        # 验证页面包含首页内容
        assert "首页" in driver.page_source, "登录后未跳转到首页！"
        print("Vue登录页面 + C#接口联动测试通过")
        
    finally:
        driver.quit()  # 无论测试成败，关闭浏览器

# 4. 测试Vue表单提交功能
def test_vue_form_submit():
    # 先校验后端接口
    assert check_csharp_api(), "后端接口不可用，测试终止"
    
    driver = get_chrome_driver()
    try:
        # 打开Vue前端表单页面
        driver.get("http://localhost:8080/form")
        
        # 等待页面加载完成
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "form-name"))
        )
        
        # 定位表单元素
        input_name = driver.find_element(By.ID, "form-name")
        input_email = driver.find_element(By.ID, "form-email")
        submit_btn = driver.find_element(By.CLASS_NAME, "form-submit-btn")
        
        # 输入表单内容并提交
        input_name.send_keys("测试用户")
        input_email.send_keys("test@example.com")
        submit_btn.click()
        
        # 验证提交后C#返回的结果展示在Vue页面
        result_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='form-result']"))
        )
        
        assert "提交成功" in result_element.text, "表单提交结果不符合预期！"
        print("Vue表单提交 + C#接口联动测试通过")
        
    finally:
        driver.quit()

# 5. 测试Vue页面导航功能
def test_vue_navigation():
    driver = get_chrome_driver()
    try:
        # 打开Vue前端首页
        driver.get("http://localhost:8080/")
        
        # 等待页面加载完成
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        
        # 验证重定向到登录页
        assert "用户登录" in driver.page_source, "页面未正确重定向到登录页"
        
        # 输入登录信息
        username_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='login-username']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[data-testid='login-password']")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-submit-btn']")
        
        username_input.send_keys("test_user")
        password_input.send_keys("test_pass123")
        login_btn.click()
        
        # 等待跳转到首页
        WebDriverWait(driver, 15).until(
            EC.url_contains("/home")
        )
        
        # 验证导航到表单页
        form_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "表单测试页"))
        )
        form_link.click()
        
        # 验证跳转到表单页
        WebDriverWait(driver, 15).until(
            EC.url_contains("/form")
        )
        assert "表单提交测试" in driver.page_source, "导航到表单页失败"
        
        print("Vue页面导航测试通过")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    # 运行测试
    test_vue_login_with_csharp_api()
    test_vue_form_submit()
    test_vue_navigation()
    print("所有UI自动化测试通过！")