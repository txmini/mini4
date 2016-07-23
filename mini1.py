import tornado.httpserver 
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escepe

for tornado.options import define, options
define("port", default = 8000, help = "run on the given port", type = int)

#成功返回0，失败返回-1
def writeDB(uid, picurl, localinfo, text, daytime):
#读取当前位置的数据库
def readLocalDB(localinfo, page):
#读取用户历史
def readHistoryDB(uid, page):
#读取用户所在位置历史
def readLocalPersonDB(uid, localinfo, page):


#写入数据库，包括uid，位置，图片url，时间
class Upload(tornado.web.RequestHandler):
	def get(self):
		picurl = self.get_argumens("pic")
		localinfo = self.get_argumens("localinfo")
		daytime = self.get_argumens("daytime")
		text = self.get_argumens("textinfo")
		uid = self.get_argumens("user")
		if((n = writeDB(uid, picurl, localinfo, text, daytime) == 0)
			respon = {'upload':'sucess'}
		else
			respon = {'upload':'fail'}
		respon_json = tornado.escepe.json_encode(respon)
		self.write(respon_json)

#拉取当前位置的信息
class GetLocalInfo(tornado.web.RequestHandler):  
	def get(self):
		localinfo = self.get_argumens("localinfo")
		uid = self.get_argumens("user")
		page = self.get_argumens("page")
		readLocalDB(localinfo, page)
		respon = 
		respon_json = tornado.escepe.json_encode(respon)
		self.wrtie(respon_json)
#拉取个人所有的历史信息GetMyHistory
class GetMyHistory(tornado.web.RequestHandler):
	def get(self):
		uid = self.get_argumens("user")
		page = self.get_argumens("page")
		readHistoryDB(uid, page)
		respon = 
		respon_json = tornado.escepe.json_encode(respon)
		self.wrtie(respon_json)
#拉取个人在这个位置的信息
class GetPersonInfo(tornado.web.RequestHandler):
	def get(self):
		uid = self.get_argumens("user")
		localinfo = self.get_argumens("localinfo")
		page = self.get_argumens("page")
		readLocalPersonDB(uid, localinfo, page)
		respon = 
		respon_json = tornado.escepe.json_encode(respon)
		self.wrtie(respon_json)
#删除个人制定的信息
class DeletePersonInfo(tornado.web.RequestHandler):
	def get(self):
		picurl = self.get_argumens("pic")
		localinfo = self.get_argumens("localinfo")
		daytime = self.get_argumens("daytime")
		text = self.get_argumens("textinfo")
		uid = self.get_argumens("user")
		self.write()

'''

'''
if __name__ == "__main__":
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handleer = [
			(r"/upload", Upload),
			(r"/getloaclinfo", GetLocalInfo),
			(r"/getmyhistory", GetMyHistory),
			(r"/getlocalpersoninfo", GetPersonInfo),
			(r"/deletepersoninfo", DeletePersonInfo)
		]
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()