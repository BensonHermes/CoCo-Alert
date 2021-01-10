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
        elif order == 1:
            cursor.execute(sqlStatement,data)
            connection.commit()
            return 'succeed'
        # order == 2 -> update data
        else:
            print('Update')
            cursor.execute(sqlStatement)
            connection.commit()
            return 'succeed'

    except Error as e:
        print("資料庫連接失敗：", e)
        raise

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("資料庫連線已關閉")

def getWarnPlaceInRange(lat1, long1, lat2, long2):
   statement = f"SELECT DeptNm, BranchNm, Address, Contact FROM Location WHERE Longitude > {long1} AND Longitude < {long2} AND Latitude > {lat1} AND Latitude < {lat2};"
   res = doSQL(0, statement, None)
   return res

def exist(user_id):
    statement = f'SELECT User_token FROM User WHERE User_token = "{user_id}"'
    res = doSQL(0, statement, None)
    if res == []:
        return False
    return True

def query(user_id):
    statement = f'SELECT * FROM User WHERE User_token = "{user_id}"'
    return doSQL(0, statement, None)

def newUser(user_id):
    # User_name, User_token, Home_la, Home_long, Address, Contact_name, Contact_token
    data = ("", user_id, "0", "0", "", "", "")
    try:
        doSQL(1, "INSERT INTO User VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
    except:
        raise
    return

def getUserInfo(user_id):
    # return [("chouyun", "政大", "Hsin")]
    return doSQL(0, f"SELECT User_name, Address, Contact_name FROM User WHERE User_token = '{user_id}'", None)

def getContactInfo(user_id):
    # return [("Hsin", "U0ed3d02a2d6e794697b114d7977d48aa")]
    return doSQL(0, f"SELECT Contact_name, Contact_token FROM User WHERE User_token = '{user_id}'", None)

def getHomeInfo(user_id):
    # return [("政大", 24.9861694, 121.5749262)]
    return doSQL(0, f"SELECT Address, Home_la, Home_long FROM User WHERE User_token = '{user_id}'", None)

def setUserName(user_id, name):
    used = doSQL(0, f"SELECT User_token FROM User WHERE User_name = '{name}'", None)
    if used != [] and used[0][0] != user_id:
        return False
    doSQL(2, f"UPDATE User SET User_name = '{name}' WHERE User_token = '{user_id}'", None)
    return True

def checkUserName(user_id, name):
    used = doSQL(0, f"SELECT User_token FROM User WHERE User_name = '{name}'", None)
    if used != [] and used[0][0] != user_id:
        return False
    return True

def setHome(user_id, address, lat, long):
    doSQL(2, f"UPDATE User SET Address = '{address}', Home_la = '{lat}', Home_long = '{long}' WHERE User_token = '{user_id}'", None)
    return

def setContact(user_id, contact_name):
    token = doSQL(0, f"SELECT User_token FROM User WHERE User_name = '{contact_name}'", None)
    if token == []:
        return (False, token)
    token = token[0][0]
    doSQL(2, f"UPDATE User SET Contact_name = '{contact_name}', Contact_token = '{token}' WHERE User_token = '{user_id}'", None)
    return (True, token)

def checkContact(user_id, contact_name):
    token = doSQL(0, f"SELECT User_token FROM User WHERE User_name = '{contact_name}'", None)
    if token == []:
        return (False, token)
    return (True, token[0][0])

def setAll(user_id, BISM):
    statement = f"UPDATE User Set User_name = '{BISM.info.name}', \
        Address = '{BISM.info.home_address}', \
        Home_la = '{BISM.info.home_la}', \
        Home_long = '{BISM.info.home_long}, '\
        Contact_name = '{BISM.info.contact_name}', \
        Contact_token = '{BISM.info.contact_token}' WHERE User_token = '{user_id}'"
    doSQL(2, statement, None)
    BISM.info.need_update = False