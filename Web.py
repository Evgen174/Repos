import urllib
import hashlib
import tornado.ioloop
import tornado.httpclient
import tornado.web

from python_mysql_dbconfig import getConnection

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class ShowMyLink(BaseHandler):# pylint: disable=W0223
    @tornado.web.authenticated
    async def get(self):
        post_data = {'User': self.current_user}
        body = urllib.parse.urlencode(post_data)
        http = tornado.httpclient.AsyncHTTPClient()
        response = await http.fetch("http://localhost:7777/api/links",
                                    method='POST',
                                    headers=None,
                                    body=body)
        json = tornado.escape.json_decode(response.body)
        items = json['data']
        self.render("Templates/MyLink.html", items=items)




class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("Templates/Start.html", title="My title")

    @tornado.web.authenticated
    async def post(self):
        post_data = {
            'User': self.current_user,
            'Link': self.get_argument("Link")
        }
        body = urllib.parse.urlencode(post_data)
        http = tornado.httpclient.AsyncHTTPClient()
        response = await http.fetch("http://localhost:7777/api/slink",
                                    method='POST',
                                    headers=None,
                                    body=body)
        json = tornado.escape.json_decode(response.body)
        self.write("http://localhost:8888/" + json['data']['ShortLink'])



class GoLinq(BaseHandler):
    @tornado.web.authenticated
    async def get(self, ShortLink):
        http = tornado.httpclient.AsyncHTTPClient()
        h = "http://localhost:7777/api/getlink?ShortLink=" + ShortLink
        response = await http.fetch(h)
        json = tornado.escape.json_decode(response.body)
        self.redirect(json['data']['Link'])



class LoginHandler(BaseHandler):

    def get(self):
        self.render("Templates/Login.html")


    def post(self):
        conn = getConnection()
        password = self.get_argument("password")
        hash = hashlib.md5()
        hash.update(password.encode('utf-8'))
        hash = hash.hexdigest()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE name = %s AND password = %s;",
                    (self.get_argument("username"), hash))
        cur.close()
        conn.close()
        if cur.rowcount != 0:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/")
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

