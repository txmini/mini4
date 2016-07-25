# -*- coding: UTF-8 -*-
import tornado.httpserver 
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import MySQLdb
import json
import datetime,time

FORMAT = "%Y%m%d-%H%M%S"

from tornado.options import define, options, url_escape
define("port", default = 8002, help = "run on the given port", type = int)

def datetimeToString(dt):
    return dt.strftime(FORMAT)

def stringToDatetime(str):
    return datetime.datetime.strptime(str, FORMAT)

def incDatetime(dt):
    return dt + datetime.timedelta(days = 1)


class Upload(tornado.web.RequestHandler):
	def get(self):
		conn = MySQLdb.connect(host = '5792ed8746c3f.gz.cdb.myqcloud.com', port = 13885, 
            user = 'root', passwd = 'miniapp1', db = 'Yingji')
		qq_id = self.get_arguments("qq_id")
		picurl = self.get_arguments("picurl")
		lat = self.get_arguments("lat")
		lng = self.get_arguments("lng")
		location = self.get_argument("location").encode('utf-8')
		text = self.get_argument("text").encode('utf-8')
		datetime = self.get_arguments("datetime")
		username = self.get_argument("username").encode('utf-8')
		cur = conn.cursor()
		sql = "INSERT INTO message VALUES (%s,%s,%s,%s,%s,%s,0,%s,%s);"
		print qq_id[0]
		print picurl[0]
		print location[0]
		cur.execute(sql,[qq_id[0],picurl[0],lat[0],lng[0],location,stringToDatetime(datetime[0]),text,username])
		conn.commit()
		cur.close()
		conn.close()

#拉取当前位置的信息
class GetLocalInfo(tornado.web.RequestHandler):  
	def get(self):
		conn = MySQLdb.connect(
		host = '5792ed8746c3f.gz.cdb.myqcloud.com', port = 13885, 
		user = 'root', passwd = 'miniapp1', db = 'Yingji')
		lat = self.get_arguments("lat")
		lng = self.get_arguments("lng")
		cur = conn.cursor()
		sql = "select * from message where inDistance(lat,lng,%s,%s,5000)=1 order by datetime limit 8;"
		dbresult = cur.execute(sql,[lat[0],lng[0]])
		list = []
		res = {}
		info = cur.fetchmany(dbresult)
		#info.sort(lambda x,y:cmp(x[1],y[1]))
		for ii in info:
			tmp = {}
			tmp['qq_id'] = ii[0]
			tmp["pic_url"] = ii[1]
			tmp["location"] = ii[4]
			tmp["text"] = ii[7]
			tmp['datetime'] = datetimeToString(ii[5])
			tmp['username'] = ii[8]
			list.append(tmp)
		#info.sort(lambda x,y:cmp(x[1],y[1]))
		res["status"] = 1
		res["data"] = list
		jsonstr = json.dumps(res, ensure_ascii = False)
		list = []
		res = {}
		self.write(jsonstr)
		cur.close()
		conn.close()

#拉取个人所有的历史信息GetMyHistory
class GetMyHistory(tornado.web.RequestHandler):
	def get(self):
		conn = MySQLdb.connect(
            host = '5792ed8746c3f.gz.cdb.myqcloud.com', port = 13885, 
            user = 'root', passwd = 'miniapp1', db = 'Yingji')
		qq_id = self.get_arguments("qq_id")
		cur = conn.cursor()
		sql = "select * from message where qq_id = %s order by datetime limit 5;"
		dbresult = cur.execute(sql,[qq_id[0]])
		list = []
		res = {}
		info = cur.fetchmany(dbresult)
        #info.sort(lambda x,y:cmp(x[1],y[1]))
		for ii in info:
			tmp = {}
			tmp['qq_id'] = ii[0]
			tmp["pic_url"] = ii[1]
			tmp["location"] = ii[4]
			tmp["text"] = ii[7]
			tmp['datetime'] = datetimeToString(ii[5])
			tmp['username'] = ii[8]
			list.append(tmp)
        #info.sort(lambda x,y:cmp(x[1],y[1]))
		res["status"] = 1
		res["data"] = list
		jsonstr = json.dumps(res, ensure_ascii = False)
		list = []
		res = {}
		self.write(jsonstr)
		cur.close()
		conn.close()
#拉取个人在这个位置的信息
class GetPersonInfo(tornado.web.RequestHandler):
	def get(self):
		conn = MySQLdb.connect(
			host = '5792ed8746c3f.gz.cdb.myqcloud.com', port = 13885, 
            user = 'root', passwd = 'miniapp1', db = 'Yingji')
		qq_id = self.get_arguments("qq_id")
		lat = self.get_arguments("lat")
		lng = self.get_arguments("lng")
		cur = conn.cursor()
		sql = "select * from message where qq_id = %s and inDistance(lat,lng,%s,%s,5000)=1 order by datetime limit 5;"
		dbresult = cur.execute(sql,[qq_id[0],lat[0],lng[0]])
		list = []
		res = {}
		info = cur.fetchmany(dbresult)
        #info.sort(lambda x,y:cmp(x[1],y[1]))
		for ii in info:
			tmp = {}
			tmp['qq_id'] = ii[0]
			tmp["pic_url"] = ii[1]
			tmp["location"] = ii[4]
			tmp["text"] = ii[7]
			tmp['datetime'] = datetimeToString(ii[5])
			tmp['username'] = ii[8]
			list.append(tmp)
        #info.sort(lambda x,y:cmp(x[1],y[1]))
		res["status"] = 1
		res["data"] = list
		jsonstr = json.dumps(res, ensure_ascii = False)
		list = []
		res = {}
		self.write(jsonstr)
		cur.close()
		conn.close()
#删除个人制定的信息
class DeletePersonInfo(tornado.web.RequestHandler):
	def get(self):
		conn = MySQLdb.connect(
			host = '5792ed8746c3f.gz.cdb.myqcloud.com', port = 13885, 
			user = 'root', passwd = 'miniapp1', db = 'Yingji')
		cur = conn.cursor()
		picurl = self.get_arguments("picurl")
		sql = "delete from message where pic_url = %s;" 
		cur.execute(sql,[picurl[0]])
		conn.commit()
		cur.close()
		conn.close()


'''

'''
class fake(tornado.web.RequestHandler):
	def get(self):
		respon = {'status':1,
			'date':[{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'},{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'},{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'},{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'},{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'},{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'},{'picurl':'www.baidu.com/1.jpg','longitude':1.000000,'latitude':2.000000,
			'textinfo':'aaaaaabbbbbbbbbbbccccccccccc','time':'2016年7月24日'}]}
		respon_json = tornado.escape.json_encode(respon)
		self.write(respon_json)
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(handlers=[(r"/upload/", Upload),
											(r"/fake/",fake),
												(r"/getlocalinfo/", GetLocalInfo),
												(r"/getmyhistory/", GetMyHistory),
												(r"/getlocalpersoninfo/", GetPersonInfo),
												(r"/deletepersoninfo/", DeletePersonInfo)])
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
