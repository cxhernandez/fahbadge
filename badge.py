#!/usr/bin/python

from rule import *
from PIL import Image
import MySQLdb as mysql

class Badge(object): 
    
    @property
    def id(self):
        """
        id of the badge
        
        Returns
        -------
        id : long
        """
        return self._id
        
    @id.setter
    def id(self,value):
        """
        Sets id of the badge
        """
        self._id = value
    
    @property
    def name(self):
        """
        Name of the badge
        
        Returns
        -------
        name : string
        """
        return self._name
        
    @name.setter
    def name(self,value):
        """
        Sets name of the badge
        """
        self._name = "'" + value + "'"
        
    @property
    def requirements(self):
        """
        Requirements to attain badge
        
        Returns
        -------
        requirements : Rule Object
        """
        return self._requirements
        
    @requirements.setter
    def requirements(self,value):
        """
        Sets requirements for the badge
        """
        self._requirements = value
        
    @property
    def description(self):
        """
        Description of the badge
        
        Returns
        -------
        description : string
        """
        return self._description
        
    @description.setter
    def description(self,value):
        """
        Sets description of the badge
        """
        self._description = "'" + value + "'"
        
    @property
    def logo(self):
        """
        Logo of badge
        
        Returns
        -------
        logo : PIL Object
        """
        return self._logo
        
    @logo.setter
    def logo(self,value):
        """
        Sets logo of the badge
        """
        self._logo = Image.open(value).
        
    def _assign_id(self):
        """
        Generates a unique id for the badge
        
        Returns
        -------
        unique_id : long
        """
        self._db.query('SELECT id FROM badges ORDER BY id DESC LIMIT 1')
        q = self._db.store_result().fetch_row(how=1,maxrows=0)
        if not q:
            return 0L
        return q[0]['id']+1
        
    def __init__ (self, name, requirements, id = None, description = None, logo = None):
        
        self._db = mysql.connect(user='root',db='fah')
        
        self.name = name
        self.requirements = requirements
        
        if description is None:
            description = ""
        self.description = description
        
        if logo is None:
            logo = "./logos/example.png"
        # self.logo = logo
        
        if id is None:
            id = self._assign_id()
        self.id = id
        
    def save(self):
        """
        Saves the badge to MySQL table
        """
        cursor = self._db.cursor()
        badge = dict(self.__dict__.items() + self.__dict__.items())
        columns = badge.keys()
        columns.remove('_db')
        columns.remove('_requirements')
        cmd = 'INSERT INTO badges (' + ', '.join(columns).replace('_','') + ') VALUES (' + ', '.join(['%s'] * len(columns)) + ')'
        try:
            cursor.execute(cmd % tuple([badge[i] for i in columns]))
            self._db.commit()
        except:
            self._db.rollback()
        cursor.close()
        
    def qualify(self, profile):
        """
        Does a given user profile qualify for this badge?
        
        Returns
        -------
        qualify : boolean
        """
        req = self._requirements.__dict__
        prof = profile.__dict__
        for i in req.keys():
            if isinstance(req[i],int):
                if prof[i] < req[i]:
                    return False;
            elif isinstance(req[i],str):
                if req[i] is not 'any':
                    if prof[i] is not req[i]:
                        return False
        return True