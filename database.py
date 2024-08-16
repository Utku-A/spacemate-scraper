import mysql.connector as connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
import config


def db_connect():
    try:
        return connector.connect(**config.db_config)
    except connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            return print("Database user error")
        else:
            return print(err)


def db_insert(sql, values):
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(sql, values)
    connect.commit()


def db_insert_no_values(sql):
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(sql)
    connect.commit()


def db_execute(execute):
    connect = db_connect()
    cursor = connect.cursor()
    cursor.execute(execute)
    data = cursor.fetchall()
    return data


def get_time():
    dates = datetime.utcnow() + timedelta(hours=3) 
    return dates.strftime("%Y-%m-%d %X")


def check_data_link(link):
    data = db_execute(f"SELECT count(*) FROM Spacemate.facebook_marketplace WHERE Link = '{link}';")[0][0]  
    return True if data > 0 else False


def add_search_marketplace_data(location,search_query,title,link,price,currency):
    try:
        if check_data_link(link):
            return print(f"{link} Bu veri zaten kayıtlı")
        
        db_insert("INSERT INTO Spacemate.facebook_marketplace (Search_Location, Search_Qery, Link, Title, Price, Currency, Create_Time) VALUES (%s,%s,%s,%s,%s,%s,%s);",
            (location,search_query,link,title,price,currency,get_time()))
        print(f"{link} Veri eklendi.")
        return True
    except Exception as error:
        print(f"add_search_marketplace_data error: {str(error)}")
        return False


def update_items(link, title, description, maps_X, maps_y):
    db_insert("UPDATE Spacemate.facebook_marketplace SET Detail_Text = %s, Maps_X = %s, MAPS_Y = %s, Update_Time = %s WHERE Link = %s ",
        (description, maps_X, maps_y, get_time(), link))
    return True


def get_items_data_db(link):
    data = db_execute(f"SELECT Currency, Price, Title, Detail_Text, Maps_X, MAPS_Y FROM Spacemate.facebook_marketplace WHERE Link = '{link}' ")[0]
    return {
        "Currency"      : data[0],
        "Price"         : data[1],
        "Title"         : data[2],
        "Detail_Text"   : data[3],
        "Maps_X"        : data[4],
        "MAPS_Y"        : data[5]
    }


def set_items_listing_id_db(link, listing_id):
    db_insert("UPDATE Spacemate.facebook_marketplace SET Listing_ID = %s WHERE Link = %s",(listing_id, link))


def get_page_scanner_job_link_data():
    return db_execute("SELECT Link FROM Spacemate.facebook_marketplace WHERE Listing_ID is null;")