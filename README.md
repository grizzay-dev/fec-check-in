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
- uuid==1.30
- waitress==2.0.0
- Werkzeug==2.0.1

*[app.py](https://github.com/grizzay-dev/fec-check-in/blob/main/app.py) contains main application code.*

*[user.py](https://github.com/grizzay-dev/fec-check-in/blob/main/user.py) contains a collection of helper methods.*

### Database & Static Folder
#### Data: `data/data.db`
User and audit log information is stored in data.db sqlite database (documenation: [SQLite](https://github.com/sqlitebrowser/sqlitebrowser/wiki)).

Database file can be interacted with using [DB Browser for SQLite](https://sqlitebrowser.org/dl/)

Create statements for required tables below:
`user` table:
```sql
CREATE TABLE "user" (
	"id"	TEXT NOT NULL UNIQUE,
	"email"	TEXT,
	"fname"	TEXT,
	"lname"	TEXT,
	"lastmod"	TEXT,
	"status"	TEXT DEFAULT 'OUT',
	"comment"	TEXT,
	PRIMARY KEY("id")
)
```

`auditlog` table:
```sql
CREATE TABLE "auditlog" (
	"id"	INTEGER NOT NULL UNIQUE,
	"timestamp"	TEXT,
	"change"	TEXT,
	"prev"	TEXT,
	"new"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
```

`sqlite_sequence` table (should be automatically created after `auditlog` table):
```sql
CREATE TABLE sqlite_sequence(name,seq)
```

#### Upload Folder: `static/images/users`
Folder contains user profile pictures. These are updated via the 'edit profile' page for each user. Files are named as per the users unique id `<id>.png` and must be a `.png` filetype.


## Routes
### HOME - `http://hostname/`
Returns the Checkin Board home page which displays all users and their current status.

### CREATE PROFILE - `http://hostname/create`
Returns the new profile form which is used to create a new user.

### EDIT PROFILE - `http://hostname/id/<id>`
Returns the 'edit profile' page for a specific user, `<id>`.

### DELETE PROFILE - `http://hostname/delete/<id>`
Route used to delete a specific user, `<id>`. Once a user is deleted the record is permentantly removed from the `user` table. The action and deleted record are record in the `auditlog` table. This route only accepts POST requests and can be accessed via the 'edit profile' page (`/id/<id>`)

### UPDATE STATUS - `http://hostname/update-status/<id>`
This route is used to update user status by individual users (non-administrators). A unique address for each user will need to be provided so that they can make changes to their status. Unique user addresses are available on 'edit profile' page for each user.

### ADMINISTRATION - `http://hostname/admin`
This route is used to view and administer all users. From this page you can create, edit or delete existing users.

### AUDIT LOGS - `http://hostname/admin/logs`
This route displays the audit logs stored in the `auditlog` table within the database. All changes/updates to users are recorded in the `auditlog` table. Each log record has a unique, incremented `id` and logs are requests in descending order (most recent first). The number of logs displayed is defined in `app.py` via the variable `MAX_LOG_DISPLAY_LEN`, (*default = 51*).