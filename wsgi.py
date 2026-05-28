from internal.factory import new_wsgi

app = new_wsgi()

if __name__ == '__main__':
    app.run()
