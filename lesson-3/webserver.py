from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

engine             = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession          = sessionmaker(bind = engine)
session            = DBSession()


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
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br/>"
                    output += "<a href ='/restaurants/%s/edit'>Edit </a> " % restaurant.id
                    output += "<br/>"
                    output += "<a href ='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "<br/>"
                    output += "<br/><br/>"

                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants/new"):
              self.send_response(200)
              self.send_header('Content-type', 'text/html')
              self.end_headers()
              output = ""
              output += "<html><body>"
              output += "<h1>Create a New Restaurant</h1>"
              output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Enter a new restaurant name:</h2><input name="newRestaurantName" type="text" ><input type="submit" value="Create"></form>'''
              output += "</body></html>"
              self.wfile.write(output)
              print output
              return

            if self.path.endswith("/edit"):
              restaurantID = self.path.split("/")[2]
              restaurant   = session.query(Restaurant).filter_by(id = restaurantID).one()

              if restaurant:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>"
                output += restaurant.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantID
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % restaurant.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
              restaurantID = self.path.split("/")[2]
              restaurant   = session.query(Restaurant).filter_by(id = restaurantID).one()

              if restaurant:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Sure you want to delete %s?" % restaurant.name
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantID
                output += "<input type = 'submit' value = 'Delete'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
          if self.path.endswith("/delete"):
            restaurantID = self.path.split("/")[2]
            restaurant   = session.query(Restaurant).filter_by(id = restaurantID).one()

            if restaurant:
              session.delete(restaurant)
              session.commit()

              self.send_response(301)
              self.send_header('Content-type', 'text/html')
              self.send_header('Location', '/restaurants')
              self.end_headers()

          if self.path.endswith("/edit"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                restaurantID   = self.path.split("/")[2]

                restaurant     = session.query(Restaurant).filter_by(id = restaurantID).one()

                if restaurant != []:
                  restaurant.name = messagecontent[0]
                  session.add(restaurant)
                  session.commit()

                  self.send_response(301)
                  self.send_header('Content-type', 'text/html')
                  self.send_header('Location', '/restaurants')
                  self.end_headers()

          if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
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
