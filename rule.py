#!/usr/bin/python

class Rule(object):

    @property
    def points(self):
        """
        Return point requirement
        
        Returns
        -------
        points : int
        """
        return self._points
        
    @points.setter
    def points(self, value):
        """
        Sets point requirement
        """
        self._points = value
        
    @property
    def platform(self):
        """
        Return platform requirement
        
        Returns
        -------
        platform : string
        """
        return
        return self._platform
        
    @platform.setter
    def platform(self, value):
        """
        Sets platform requirement
        """
        self._platform = "'" + value + "'"
        
    @property
    def project(self):
        """
        Return project requirement
        
        Returns
        -------
        platform : string
        """
        return self._project
        
    @project.setter
    def project(self, value):
        """
        Sets project requirement
        """
        self._project = "'" + value + "'"
        
    def __init__ (self, points = None, platform = None, project = None):
        
        if points is None:
            points = 0
        if platform is None:
            platform = 'any'
        if project is None:
            project = 'any'
            
        self.points = points
        self.platform = platform
        self.project = project