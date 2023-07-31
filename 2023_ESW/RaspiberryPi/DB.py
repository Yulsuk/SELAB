import pymysql

db = pymysql.connect(host='220.69.240.29', port=3306, user='rasp', passwd='selab', db='greenhouse', charset='utf8')
curs = db.cursor()

def ReadControlValue():
	sql = 'SELECT * FROM apptorasp_controlvalue'
	curs.execute(sql)
	result = curs.fetchall()
	
	return result

def SendTempAndHumToDB(temp, hum):
	sql = 'INSERT INTO rasptoapp_tempandhum (temperature, humidity) VALUES (%s, %s)'
	curs.execute(sql, (temp,hum))
	db.commit()
	#db.close()
