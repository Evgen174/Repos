import pymysql.cursors



def getConnection():

    connection = pymysql.connect(host='localhost',
                                 user='user',
                                 passwd='1qaz@WSX',
                                 db='link_short')
    return connection