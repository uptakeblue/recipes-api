# Author:       Michael Rubin
# Created:      7/22/2023
# Modified:     9/26/2023
#
# Copyright 2023 © Uptakeblue.com, All Rights Reserved
# -----------------------------------------------------------
import pymysql
from pymysql import err

# constants
DATEFORMAT = "%Y-%m-%d"
DATETIMEFORMAT = "%Y-%m-%d %H:%M:%S" 
# 2023-07-18 00:00:00

RESPONSECODE_OK = 200
RESPONSECODE_CREATED = 201
RESPONSECODE_BADREQUEST = 400
RESPONSECODE_UNAUTHRORIZED = 401
RESPONSECODE_NOTFOUND = 404
RESPONSECODE_NOTALLOWED = 405
RESPONSECODE_SERVERERROR = 500

MODULE = "uility"
class Global_Utility:
    settings = None
    __pymysqlConnection = None

    def __init__(self, app_config:list):
        self.settings = app_config
        output = ""
        for k in self.settings:
            output = f"{output}{k}: {self.settings[k]}\n"
        print(output)

    @property
    def pymysqlConnection(self):

        if not self.__pymysqlConnection or not self.__pymysqlConnection.open:
            mysqlEndpoint = self.settings['MYSQL_ENDPOINT']
            mysqlUsername = self.settings['MYSQL_USER']
            mysqlPassword = self.settings['MYSQL_PASSWORD']

            try:
                self.__pymysqlConnection = pymysql.connect(
                    host = mysqlEndpoint,
                    port = 3306,
                    user = mysqlUsername,
                    password = mysqlPassword,
                )
                self.__pymysqlConnection
            except Exception as e:
                raise UptakeblueException(e, f"{MODULE}.pymysqlConnection()")

        return self.__pymysqlConnection

    @pymysqlConnection.setter
    def pymysqlConnection(self, value):
        self.__pymysqlConnection = value

    def CommitDatabaseConnection(self):
        if self.__pymysqlConnection and self.__pymysqlConnection.open:
            self.__pymysqlConnection.commit()
        
    def CloseDatabaseConnection(self):
        try:
            if self.__pymysqlConnection and self.__pymysqlConnection.open:
                self.__pymysqlConnection.close()
                self.__pymysqlConnection = None
        except Exception as e:
            raise UptakeblueException(e, f"{MODULE}.pymysqlConnection()")

    def __del__(self):
        self.CloseDatabaseConnection()


class UptakeblueException(Exception):
    def __init__(self, e: Exception, source, **kwargs) -> None:
        self.ErrorNumber = 0
        self.Description = None
        self.ParamArgs = None
        self.ResponseCode = RESPONSECODE_SERVERERROR
        self.Source = source
        self.InternalException = e
        self.ErrorType = None

        if isinstance(e, UptakeblueException):
            self.ErrorNumber = e.ErrorNumber
            self.Description = e.Description
            self.ParamArgs = e.ParamArgs
            self.ResponseCode = e.ResponseCode
            self.Source = e.Source
            self.InternalException = e.InternalException
            self.ErrorType = e.ErrorType
            self.PrependSource(source)
        else:
            if "paramargs" in kwargs:
                self.ParamArgs = kwargs['paramargs']
            newTuple = (self.Source,) + e.args
            
            super().__init__(*newTuple)
            
            self.ErrorType = str(e.__class__).split(" ")[1].replace("'","").replace(">","")
            
            if isinstance(e, err.OperationalError):
                if e.args[0] > 10000:
                    self.ResponseCode = e.args[0] % 10000
                else:
                    self.ErrorNumber = e.args[0]
                if len(e.args) > 1:
                    self.Description = e.args[1]
            else:
                if isinstance(e.args[0], int):
                    self.ErrNumber = e.args[0]
            
            reflection = dir(e)
            if not self.Description:
                if  "description" in reflection:
                    self.Description = e.description
                else:
                    self.Description = str(e)
            if not self.ResponseCode and "code" in reflection:
                self.ResponseCode = e.code

            
            
                

    @property
    def Message(self) -> dict:
        message={
            "errType": self.ErrorType,
            "errNumber": self.ErrorNumber,
            "source": self.Source,
        }
        if self.Description:
            message['description'] = self.Description
        if self.ParamArgs:
            message['paramargs'] = self.ParamArgs
    
        return message
    

    def PrependSource(self, source):
        if not self.Source:
            self.Source = source
        else:
            self.Source = f"{source}, {self.Source}"

    def __repr__(self) -> str:
        return str(self.Message)

    