import mysql.connector
import flask
import creds
from mysql.connector import Error
from sql import create_connection                 
from sql import execute_query
from sql import execute_read_query
from flask import jsonify
from flask import request

## create a connection to mysql ##

myCreds = creds.Creds()             
                                    
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

app = flask.Flask(__name__)     
app.config["DEBUG"] = True    

#********* Program will be running on http://127.0.0.1:5000 *********#

######################################### CRUD MEMBER ######################################################

## CREATE a new member ##
@app.route('/api/addmember', methods=['POST'])     # Test this address http://127.0.0.1:5000/api/addmember 
def add_member():
    cursor = conn.cursor(dictionary=True) 

    request_data = request.get_json()           
    newfistname = request_data['firstname']     
    newlastname = request_data['lastname']
    newdetail = request_data['details']
    newtitle = request_data['title']
    newlevel = request_data['level']
    
    query = "INSERT INTO member(firstname,lastname,details,title,level) VALUES (%s,%s,%s,%s,%s)" 
    cursor.execute(query, (newfistname, newlastname,newdetail,newtitle,newlevel))
    conn.commit()  

    return 'SUCCESS'

## UPDATE a member ##
@app.route('/api/updatemember', methods=['PUT'])           # Test this address http://127.0.0.1:5000/api/updatemember 
def update_member():

    request_data = request.get_json()                
    memberid = request_data['id']       

    # Find if the id exist in the member table
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM member WHERE id = %s" 
    cursor.execute(query, (memberid,))                                                  
    member = cursor.fetchone()   

    # If member list return empty, no member was found with the ID provided
    if not member:
        statement = f'Member {memberid} does not exist, please review'
        return jsonify(statement)

    # Only the variables added to the postman input will be updated, the rest will stay the same on MySQL
    # However, ID must be entered
    firstname = request_data.get('firstname', member['firstname'])
    lastname = request_data.get('lastname', member['lastname'])
    details = request_data.get('details', member['details'])
    title = request_data.get('title', member['title'])
    level = request_data.get('level', member['level'])

    query = "UPDATE member SET firstname = %s, lastname = %s, details = %s, title = %s, level = %s WHERE id = %s"
    cursor.execute(query, (firstname, lastname, details, title, level, memberid))
    conn.commit()
                                                                                                                                   
    return 'SUCCESS'

## READ/SHOW the members##
@app.route('/api/members', methods=['GET'])                   # Test this address http://127.0.0.1:5000/api/members
def show_members():

    query = "SELECT * FROM member"                              
    membertable = execute_read_query(conn, query)

    return jsonify(membertable)

## DELETE a member ##
@app.route('/api/deletemember', methods=['DELETE'])           # Test this address http://127.0.0.1:5000/api/deletemember 
def delete_member():

    request_data = request.get_json()                
    memberid = request_data['id']       

    # Find if the id exist in the member table
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM member WHERE id = %s" 
    cursor.execute(query, (memberid,))                                                  
    member = cursor.fetchone()   

    # If member list return empty, no member was found with the ID provided
    if not member:
        statement = f'Member {memberid} does not exist, please review'
        return jsonify(statement)

    query = "DELETE FROM member WHERE id = %s"
    cursor.execute(query, (memberid,))
    conn.commit()
                                                                                                                                   
    return 'SUCCESS'

######################################### CRUD EVENT ######################################################

## CREATE a new event ##
@app.route('/api/addevent', methods=['POST'])     # Test this address http://127.0.0.1:5000/api/addevent 
def add_event():
    cursor = conn.cursor(dictionary=True) 

    request_data = request.get_json()           
    neweventname = request_data['name']     
    neweventcapacity = request_data['capacity']
    neweventlevel = request_data['level']
    neeventdate = request_data['date']                         # UNIQUE date (SQL) gives a duplica entry error - ASSIGMENT RULE
    
    query = "INSERT INTO event(name,capacity,level,date) VALUES (%s,%s,%s,%s)" 
    cursor.execute(query, (neweventname, neweventcapacity,neweventlevel,neeventdate))
    conn.commit()  

    return 'SUCCESS'

## UPDATE a event ##
@app.route('/api/updatevent', methods=['PUT'])           # Test this address http://127.0.0.1:5000/api/updatevent 
def update_event():

    request_data = request.get_json()                
    eventid = request_data['id']       

    # Find if the id exist in the event table
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM event WHERE id = %s" 
    cursor.execute(query, (eventid,))                                                  
    event = cursor.fetchone()   

    # If event list return empty, no member was found with the ID provided
    if not event:
        statement = f'Event {eventid} does not exist, please review'
        return jsonify(statement)

    # Only the variables added to the postman input will be updated, the rest will stay the same on MySQL
    # However, ID must be entered
    eventname = request_data.get('name', event['name'])
    eventcapacity = request_data.get('capacity', event['capacity'])
    eventlevel = request_data.get('level', event['level'])
    eventdate = request_data.get('date', event['date'])

    query = "UPDATE event SET name = %s, capacity = %s, level = %s, date = %s WHERE id = %s"
    cursor.execute(query, (eventname, eventcapacity, eventlevel, eventdate, eventid))
    conn.commit()
                                                                                                                                   
    return 'SUCCESS'

## DELETE a event ##
@app.route('/api/deleteevent', methods=['DELETE'])           # Test this address http://127.0.0.1:5000/api/deleteevent 
def delete_event():

    request_data = request.get_json()                
    eventid = request_data['id']       

    # Find if the id exist in the event table
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM event WHERE id = %s" 
    cursor.execute(query, (eventid,))                                                  
    event = cursor.fetchone()   

    # If Event list return empty, no event was found with the ID provided
    if not event:
        statement = f'Event {eventid} does not exist, please review'
        return jsonify(statement)

    query = "DELETE FROM event WHERE id = %s"
    cursor.execute(query, (eventid,))
    conn.commit()
                                                                                                                                   
    return 'SUCCESS'

## READ/SHOW the event##
@app.route('/api/events', methods=['GET'])                   # Test this address http://127.0.0.1:5000/api/events
def show_events():

    query = "SELECT * FROM event"                              
    eventtable = execute_read_query(conn, query)

    return jsonify(eventtable)

######################################### CRUD Registration ######################################################

## CREATE a new registration ##
@app.route('/api/addregistration', methods=['POST'])     # Test this address http://127.0.0.1:5000/api/addregistration 
def add_registration():

    cursor = conn.cursor(dictionary=True) 
    request_data = request.get_json()           
    eventid = request_data['event_id']     
    memberid = request_data['member_id']

    # Find if the id exist in the member table
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM member WHERE id = %s" 
    cursor.execute(query, (memberid,))                                                  
    member = cursor.fetchone()   

    # If member list return empty, no member was found with the ID provided
    if not member:
        statement = f'Member {memberid} does not exist, please review'
        return jsonify(statement)
    
    # Find if the id exist in the event table
    cursor = conn.cursor(dictionary=True) 
    query = "SELECT * FROM event WHERE id = %s" 
    cursor.execute(query, (eventid,))                                                  
    event = cursor.fetchone()   

    # If Event list return empty, no event was found with the ID provided
    if not event:
        statement = f'Event {eventid} does not exist, please review'
        return jsonify(statement)
    
    query = "INSERT INTO registration (event_id,member_id) VALUES (%s,%s)" 
    cursor.execute(query, (eventid, memberid))
    conn.commit()  

    return 'SUCCESS'

## READ/SHOW the registration##
@app.route('/api/registrations', methods=['GET'])                   # Test this address http://127.0.0.1:5000/api/registrations
def show_registrations():

    query = "SELECT * FROM registration"                              
    registrationtable = execute_read_query(conn, query)

    return jsonify(registrationtable)

app.run() 