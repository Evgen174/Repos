import os
import tornado.ioloop
import tornado.httpclient
import tornado.web
import pymysql
import string
import random
import re
import datetime
import hashlib

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class ShowMyLink(BaseHandler):
    @tornado.web.authenticated

    async def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        h = "http://localhost:7777/api/links/?User=" + tornado.escape.xhtml_escape(self.current_user)
        response = await http.fetch(h)
        json = tornado.escape.json_decode(response.body)
        items = json['data']
        self.render("Templates/MyLink.html", items = items)




class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("Templates/Start.html", title="My title")

    async def post(self):

        http = tornado.httpclient.AsyncHTTPClient()
        h = "http://localhost:7777/api/slink/"+tornado.escape.xhtml_escape(self.current_user)+"?Link="+self.get_argument("Link")
        response = await http.fetch(h)
        json = tornado.escape.json_decode(response.body)
        self.write("http://localhost:8888/" + json['data']['ShortLink'])



class GoLinq(BaseHandler):
    @tornado.web.authenticated

    async def get(self, ShortLink):
        http = tornado.httpclient.AsyncHTTPClient()
        h = "http://localhost:7777/api/slink/?ShortLink=" + ShortLink
        response = await http.fetch(h)
        json = tornado.escape.json_decode(response.body)
        self.redirect(json['data']['Link'])



class LoginHandler(BaseHandler):

    def get(self):
        self.render("Templates/Login.html")


    def post(self):
        
        p = self.get_argument("password")
        hash = hashlib.md5()
        hash.update(p.encode('utf-8'))
        h = hash.hexdigest()
        conn = pymysql.connect(host='localhost', port=3306, user='user', passwd='1qaz@WSX', db='link_short')
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE name = '" + self.get_argument("username") +"' AND password = '" + h + "'")
        cur.close()
        conn.close()

        if cur.rowcount != 0:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/")
            return
        else: self.redirect("/login")




settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
    (r"/MyLink", ShowMyLink),
    (r"/([A-z]+)", GoLinq),
], **settings)



if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start().n().Loop.current().start()
