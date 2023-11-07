import dropbox

app_key = 'b2vd3vijhktznx9'
app_secret = 'jxyl3pynrkdw7xi'

flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
print("1. Go to: " + authorize_url)
print("2. Click 'Allow' (you might have to log in first)")
print("3. Copy the authorization code.")

auth_code = input("Enter the authorization code here: ")
access_token, user_id = flow.finish(auth_code)

dbx = dropbox.Dropbox(access_token)
