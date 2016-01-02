from puppies import app
app.run(debug=True, host = "0.0.0.0", port = 5001)

# # Why did we need this if argument again???
# if __name__ == "__main__":
#     app.secret_key = "ZUPA_SECRET_KEY!!!"
#     app.debug = True
#     app.run(host = "0.0.0.0", port = 5001)
