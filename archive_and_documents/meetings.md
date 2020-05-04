# Meetings notes

## Meeting 1.
* **DATE: February 21st, 2020**
* **ASSISTANTS: Mika Oja**

### 10 Minutes
We went trough our plans of the project with Mika.

### Action points

Mika said that the plan was okay. Only thing that we needed to do was change the  http request from put to post in API uses.


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE: February 24th, 2020**
* **ASSISTANTS: Mika Oja**

### 20 Minutes
In this meeting we went trough our database design and implementation.

### Action points
In this meeting we got some feedback:
In the database we had to change birthdate and time to date from string. We had to change foreign keys that had set_null to include nullable = true. Also those columns that had ondelete = "SET NULL" we had to add 'nullable = True'. We also had to add a small piece of code, from excercise 1 to enable foreign keys for SQLite in our code.


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE: March 18, 2020**
* **ASSISTANTS: Mika Oja**

### 20 Minutes
In this meeting we discussed about RESTful API design. The focus was on the design and on our own questions about the design and implementation.

### Action points
Meeting 3 muistiinpanot ja kysymykset

In this meeting we discussed with Mika a lot about questions we had about design and implementation. Questions such as how game and games should be implemented.
In the meeting we reached to a following solution:
match should be transferred to  "api/games/game/match". Also what was discussed during this meeting was that we should implement two participants ("participant" and "participant2").

In addition to this discussion we had noticed during the meeting thigs such as that we had unnecesary items and that we should implement date with format rather than using a pattern, also
we had a sort by issue but this was a thing that was not required to fix.

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE:**
* **ASSISTANTS:**

Arrow between matches and game to diagram               Maybe?

Comment code/document gamescorebuilder                  Maybe?

where we took code                                                Done

we have extra work from def init_db_command()               Lisää APPENDID.EXtra workkiin maininta yms

ADD DOCUMENTATION! README!

Returns, exceptions, etc comment these                          Done for resources

test_get, test_post -> comment these resource_test.py            Done

show coverage when testing

player db table called maybe twice?

imports to resource init_py (imports we do multiple times)

check changes done

email if we cant get it working

meeting before final meeting, where test and implementation is done

Total meeting length 40 min

we try to create model table multiple times, test error might be caused.

implement one client,cmd interface is OK for client


-Diagrammi updated?
-Don't need blueprint, can use flask_restful
-not same as exercise 3
-commenting the code!
-sources
-error -> create all in init, problem is that we are trying to create a table that has already been created
-@click.command("init-db") add to documentation as extra work
-error e-mail to mika or ivan
-one option is to remove physical database somethingsomething?
-documentation (again)
-testing looks correct
-documentation (again, but for tests)
-coverage super important
-json.dupms(valid) why, stange? in tests -> not correct content type

Jouni shows
-problem is * import, creating table again when it's already there
-put all imports from ? to init, so when you call resourses it should be ok, from game.py match.py
-then its matter of stack trace, accessing models.py and from where
-check from previous commits when test was working before
-called models.py multiple times

try to have tests running

implement 1 client that calls 2(or 4) resourses, call, modify and remove resource

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

