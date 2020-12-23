import mysql.connector
from mysql.connector import Error
def doSQL(order, sqlStatement, data):
    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = mysql.connector.connect(
            host='140.119.19.73',          # 主機名稱
            port='9306',
            database='TG06', # 資料庫名稱
            user='TG06',        # 帳號
            password='i8p3q6')  # 密碼

        # 查詢資料庫
        cursor = connection.cursor()
        if(order==0):
            cursor.execute(sqlStatement)
        # 列出查詢的資料'
            records = cursor.fetchall()
            return records
            # for (Course_id, Course_name) in cursor:
            #     print("Course_id: %s, Course_name: %s" % (Course_id, Course_name))
        # order ==1 -> insert data into db
        else:
            cursor.execute(sqlStatement,data)
            connection.commit()
            return 'succeed'

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

def getWarnPlaceInRange(lat1, long1, lat2, long2):
   statement = f"SELECT DeptNm, BranchNm, Address, Contact FROM Location WHERE Longitude > {long1} AND Longitude < {long2} AND Latitude > {la1} AND Latitude < {la2};"
   res = doSQL(0, statement, None)
   return res