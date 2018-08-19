import os
import tornado.ioloop
import tornado.web
import pymysql
import string
import random
import re
import datetime

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class ShowMyLink(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #if not self.current_user:
            #self.redirect("/login")
            #return
        cur = conn.cursor()
        cur.execute("SELECT DateCreat, Link, LinkShort, linkscol FROM links WHERE user = '" + tornado.escape.xhtml_escape(self.current_user) + "'")
        cur.close()
        conn.close()
        self.render("Templates/MyLink.html",  cur=cur)

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #if not self.current_user:
            #self.redirect("/login")
            #return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render("Templates/Start.html", title="My title")
        #self.write("Hello, " + name)
    def post(self):
        #if not self.current_user:
            #self.redirect("/login")
            #return

        cur = conn.cursor()
        sql = "SELECT LinkShort FROM links WHERE Link = '" + self.get_argument("Link") + "'"
        cur.execute(sql)
        cur.close()
        conn.close()
        if cur.rowcount == 0:
            reg = re.compile('[^a-zA-Z ]')

            short_link = generator_short_link(6, reg.sub('', self.get_argument("Link")))
            now = str(datetime.datetime.now())

            sql = "Insert into  links (Link, LinkShort, User, DateCreat, linkscol) values ('" + self.get_argument(
                "Link") + "', '" + short_link + "', '" + tornado.escape.xhtml_escape(
                self.current_user) + "', '" + now + "', 0)"
            cur = conn.cursor()
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return
        else:
            self.write("Такая ссылка уже сокращена - " + str(cur._rows[0]))








class GoLinq(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        #if not self.current_user:
            #self.redirect("/login")
            #return

        cur = conn.cursor()
        sql = "SELECT Link  FROM links WHERE LinkShort = '" + id + "'"
        cur.execute(sql)
        cur.close()
        conn.close()

        if cur.rowcount != 0:
            link = cur._rows[0]
            self.redirect(link[0])
        return


class LoginHandler(BaseHandler):

    def get(self):
        self.render("Templates/Login.html")


    def post(self):

        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE name = '" + self.get_argument("username") +"' AND password = '" + self.get_argument("password") + "'")
        cur.close()
        conn.close()

        if cur.rowcount != 0:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/")
            return
        else: self.redirect("/login")





conn = pymysql.connect(host='localhost', port=3306, user='user', passwd='1qaz@WSX', db='link_short')


def generator_short_link(size: object = 6, chars: object = string.ascii_uppercase + string.digits) -> object:
    return ''.join(random.choice(chars) for _ in range(size))

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