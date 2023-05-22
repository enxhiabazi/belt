from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pie:
    db_name = 'belt'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.filling = data['filling']
        self.crust = data['crust']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #READ get pie by id
    @classmethod
    def get_pie_by_id(cls, data):
        query = "SELECT * FROM pies LEFT JOIN users on pies.user_id = users.id WHERE pies.id = %(pie_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return results
    
    #READ get all pies and their makers
    @classmethod
    def get_all(cls):
        query = "SELECT pies.name, pies.id, users.first_name as first_name, COUNT(votes.pie_id) AS count FROM pies LEFT JOIN users on pies.user_id = users.id LEFT JOIN votes on pies.id= votes.pie_id GROUP BY pies.id ORDER BY count DESC;" 
        results = connectToMySQL(cls.db_name).query_db(query)
        # Create an empty list to append our instances of users
        pies = []
        if results:
            for pie in results:
                pies.append(pie)
            return pies
        return pies
    
    #CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO pies (name, filling, crust, user_id) VALUES ( %(name)s, %(filling)s,%(crust)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE pies SET name = %(name)s, filling = %(filling)s, crust = %(crust)s WHERE pies.id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM pies WHERE pies.id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #DELETE all pies
    @classmethod
    def deleteAllPies(cls, data):
        query = "DELETE FROM votes WHERE pie_id = %(pie_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #add vote
    @classmethod
    def addVote(cls, data):
        query = "INSERT INTO votes (pie_id, user_id) VALUES ( %(pie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data) 
     
    #delete vote
    @classmethod
    def unVote(cls, data):
        query = "DELETE FROM votes WHERE pie_id = %(pie_id)s and user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    #Getting the users likes so that we can see if he liked the clicked pie or not(so if it is his list or not)
    @classmethod
    def get_user_likes_id(cls, data):
        query = "SELECT votes.pie_id as id FROM votes WHERE votes.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        nrOfLikes = []
        if results:
            for row in results:
                nrOfLikes.append(row['id'])
            return nrOfLikes
        return nrOfLikes
    
    #READ get user's pies
    @classmethod
    def get_user_pies(cls, data):
        query = "SELECT * FROM pies LEFT JOIN users on pies.user_id = users.id WHERE pies.user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        pies = []
        if results:
            for pie in results:
                pies.append(pie)
            return pies
        return pies
    

    #VALIDATION
    @staticmethod
    def validate_pie(pie):
        is_valid = True
        if len(pie['name']) <3:
            flash('Name should be more than 3 characters!', 'name')
            is_valid= False
        if len(pie['filling']) <3:
            flash('Filling should be more than 3 characters!', 'filling')
            is_valid= False
        if len(pie['crust']) <3:
            flash('Crust should be more than 3 characters!', 'crust')
            is_valid= False
        return is_valid
        