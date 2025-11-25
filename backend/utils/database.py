import pymysql
import os

# 配置数据库连接参数
instance_ip = '*.*.*.*' # 替换为实例的IP地址
instance_port = 3306
database_name = 'my_db_test'

conn = None
try:
    # 认证用的用户名和密码直接写到代码中有很大的安全风险，建议在配置文件或者环境变量中存放(密码应密文存放，使用时解密)，确保安全。
    # 本示例以用户名和密码保存在环境变量中为例，运行本示例前请先在本地环境中设置环境变量(环境变量名称请根据自身情况进行设置)
    #EXAMPLE_USERNAME_ENV和EXAMPLE_PASSWORD_ENV。

    username = os.getenv('EXAMPLE_USERNAME_ENV')
    password = os.getenv('EXAMPLE_PASSWORD_ENV')

    # 建立数据库连接
    conn = pymysql.connect(
        host=instance_ip,
        port=instance_port,
        user=username,
        password=password,
        database=database_name,
    )

    print("Database connected")

    with conn.cursor() as cursor:
        # 执行查询
        sql = "SELECT * FROM mytable WHERE columnfoo = 500"
        cursor.execute(sql)

        # 获取并打印结果
        results = cursor.fetchall()
        for row in results:
            print(row)

finally:
    # 关闭数据库连接
    if conn and conn.open:
        conn.close()
        print("Database connection closed")