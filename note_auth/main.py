from note import create_app  # we can import create_app from "note" because note folder is a python package so we can import the create_app function as it is in the __init__.py file 


app = create_app()


# only if we run this file app.run is going to be run on debug mode(which mean any time we make changes it is going to rerun our server) 
if __name__ == '__main__':
    app.run(debug=True)