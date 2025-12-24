import requests
import pyodbc
import pytest

# 接口基础地址
BASE_URL = "http://localhost:5000"

# SQL Server连接配置（和Actions中容器一致）
SQL_SERVER_CONFIG = {
    "DRIVER": "{ODBC Driver 17 for SQL Server}",
    "SERVER": "localhost,1433",
    "DATABASE": "bill_test_db",
    "UID": "sa",
    "PWD": "StrongPass@123456",
    "TrustServerCertificate": "yes"  # 跳过证书验证（测试环境）
}

# -------------------------- 测试数据初始化/清理 --------------------------
@pytest.fixture(scope="function")
def init_sql_server():
    """每个测试用例执行前初始化账单表，执行后清理"""
    # 1. 连接数据库
    conn = pyodbc.connect(**SQL_SERVER_CONFIG)
    cursor = conn.cursor()

    # 2. 初始化表（若不存在则创建，存在则清空）
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Bill')
        BEGIN
            CREATE TABLE Bill (
                BillId INT IDENTITY(1,1) PRIMARY KEY,
                UserId INT NOT NULL,
                Amount DECIMAL(10,2) NOT NULL,
                BillTime VARCHAR(20) NOT NULL
            )
        END
        ELSE
        BEGIN
            TRUNCATE TABLE Bill;  -- 清空数据（自增ID重置）
        END
    """)
    # 3. 插入测试数据
    cursor.execute("INSERT INTO Bill (UserId, Amount, BillTime) VALUES (1001, 50.00, '2025-12-01')")
    conn.commit()

    yield  # 执行测试用例

    # 4. 测试完成后清理数据
    cursor.execute("TRUNCATE TABLE Bill")
    conn.commit()
    cursor.close()
    conn.close()

# -------------------------- 接口+数据库验证测试 --------------------------
def test_get_bill_success_with_db(init_sql_server):
    """测试拉取账单：接口返回正确 + 数据库数据一致"""
    # 1. 调用拉取账单接口
    url = f"{BASE_URL}/api/bill"
    params = {"userId": 1001, "month": "2025-12"}
    response = requests.get(url, params=params)
    res = response.json()

    # 2. 验证接口返回
    assert response.status_code == 200
    assert res["code"] == 200
    assert res["msg"] == "拉取成功"
    assert len(res["data"]) >= 1
    assert res["data"][0]["amount"] == 50.00

    # 3. 验证SQL Server数据库数据
    conn = pyodbc.connect(**SQL_SERVER_CONFIG)
    cursor = conn.cursor()
    # 查询数据库中用户1001的12月账单
    cursor.execute("""
        SELECT Amount FROM Bill 
        WHERE UserId = ? AND BillTime LIKE ?
    """, (1001, "2025-12%"))
    db_data = cursor.fetchone()

    # 断言数据库数据和接口返回一致
    assert db_data is not None
    assert float(db_data[0]) == 50.00  # 转换为float匹配接口返回

    cursor.close()
    conn.close()

def test_add_bill_success_with_db(init_sql_server):
    """测试新增账单：接口返回成功 + 数据库新增数据"""
    # 1. 调用新增账单接口
    url = f"{BASE_URL}/api/bill"
    data = {"userId": 1001, "amount": 200.00, "time": "2025-12-24"}
    response = requests.post(url, json=data)
    res = response.json()

    # 2. 验证接口返回
    assert response.status_code == 200
    assert res["code"] == 200
    assert res["msg"] == "新增账单成功"

    # 3. 验证数据库新增数据
    conn = pyodbc.connect(**SQL_SERVER_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Amount, BillTime FROM Bill 
        WHERE BillId = ?
    """, (res["data"]["billId"],))
    db_data = cursor.fetchone()

    assert db_data is not None
    assert float(db_data[0]) == 200.00
    assert db_data[1] == "2025-12-24"

    cursor.close()
    conn.close()