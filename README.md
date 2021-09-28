# FEC Check-In Board
This repository  is for the [FEC Check-in Board](https://github.com/grizzay-dev/fec-check-in).

## General Information

### Application Dependencies:
- click==8.0.1
- colorama==0.4.4
- Flask==2.0.1
- imutils==0.5.4
- itsdangerous==2.0.1
- Jinja2==3.0.1
- MarkupSafe==2.0.1
- numpy==1.21.1
- opencv-python==4.5.3.56
- uuid==1.30
- waitress==2.0.0
- Werkzeug==2.0.1

*[user.py](https://github.com/grizzay-dev/fec-check-in/blob/main/user.py) contains a collection of helper methods.*

### Static Files
#### Data: `data/user.json`
User information is stored in data.json, example structure below:
```json
{
    "f5f29334-bdd7-4c14-8b02-92faf4961228": {
        "email": "example.user@email.com",
        "fName": "Example",
        "lName": "User",
        "lastmod": "01/01/1990, 18:00:00",
        "status": "OUT"
    },
    "e10e4823-9822-4f01-ab47-5ae20f4e5492": {...}
}
  
```
The `data.json` contains a collection of UIDs with correspond user data.
#### Upload Folder: `static/images/users`
contains user profile pictures. These are updated via the 'edit profile' page for each user.


## Routes
### HOME - `http://hostname/`
Returns the Checkin Board home page which displays all users and their current status.

### CREATE PROFILE - `http://hostname/create`
Returns the new profile form which is used to create a new user.

### EDIT PROFILE - `http://hostname/id/<id>`
Returns the 'edit profile' page for a specific user, `<id>`.

### DELETE PROFILE - `http://hostname/delete/<id>`
Route used to delete a specific user, `<id>`. Once a user is deleted the `data.json` file is overwritten and the user cannot be recovered. This route only accepts POST requests and can be accessed via the 'edit profile' page (`/id/<id>`)

### UPDATE STATUS - `http://hostname/update-status/<id>`
This route is used to update user status by individual users (non-administrators). A unique address for each user will need to be provided so that they can make changes to their status. Unique user addresses are available on 'edit profile' page for each user.

### ADMINISTRATION - `http://hostname/admin`
This route is used to view and administer all users. From this page you can create, edit or delete existing users.

### AUDIT LOGS - `http://hostname/admin/logs`
This route displays the audit logs saved in the file `audit.log`. All changes made to `data.json` are recorded here. The number of logs displayed is defined in `app.py` via the variable `MAX_LOG_DISPLAY_LEN`, (*default = 51*).