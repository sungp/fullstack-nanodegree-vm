from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, cgitb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
               
                restaurants = session.query(Restaurant).all()

                output = ""
                output = "<a href = 'restaurants/new'> Make a New Restaruant </a></br>"
                output += "<html><body>"
                for restaurant in restaurants:
                  output += "</br></br>{}</br>".format(restaurant.name)
                  output += "<a href = 'restaurants/%d/edit'>Edit</a> </br>" % restaurant.id
                  output += "<a href = '#'>Delete</a>"

                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text"  placeholder = 'New Restaurant Name'><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return                 
            
            if self.path.endswith("/edit"):
                restid = self.path.split('/')[2]
                rest_update = session.query(Restaurant).filter_by(id = int(restid)).first()
                print "updating " + rest_update.name
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>%s</h1>" % rest_update.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/edit'><input name="rename" type="text"  placeholder = '{}'><input type="submit" value="Rename"> </form>'''.format(restid, rest_update.name)
                output += "</body></html>"
                self.wfile.write(output)
                print output


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
          if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            output = ""
            if ctype == 'multipart/form-data':
              fields = cgi.parse_multipart(self.rfile, pdict)
              messagecontent = fields.get('newRestaurantName')
              print "new restaurant to be created: %s" % messagecontent[0]
              newRestaurant = Restaurant(name = messagecontent[0])
              session.add(newRestaurant)
              session.commit()

              self.send_response(301)
              self.send_header('Content-type', 'text/html')
              self.send_header('Location', '/restaurants')
              self.end_headers()
          
          if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            restid = self.path.split('/')[2]
            rest_update = session.query(Restaurant).filter_by(id = int(restid)).first()
            print "restaurant to be updated: %s" % rest_update.name
            output = ""
            if ctype == 'multipart/form-data':
              fields = cgi.parse_multipart(self.rfile, pdict)
              messagecontent = fields.get('rename')
              print fields 
              print "restaurant to be updated:from {} to {}".format(rest_update.name, messagecontent[0])
              rest_update.name = messagecontent[0]
              session.add(rest_update)
              session.commit()

              self.send_response(301)
              self.send_header('Content-type', 'text/html')
              self.send_header('Location', '/restaurants')
              self.end_headers()

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
