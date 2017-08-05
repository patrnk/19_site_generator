from livereload import Server

def make_site():
    pass


if __name__ == '__main__':
    server = Server()
    server.watch('templates/', make_site)
    server.serve(root='website/')
