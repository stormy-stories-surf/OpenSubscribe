import mysql.connector

class SQLWrapper:
    def __init__(self, configFileName = "config/config.json"):
        with open(configFileName) as json_file:
            data = json.load(json_file)
            self.sqlHost = data["SQL_HOST"]
            self.sqlDatabase = data["SQL_DATABASE"]
            sendMailsData = data["SEND_MAILS"]
            self.sendMailsSqlUser = sendMailsData["SQL_USER"]
            self.sendMailsSqlPW = sendMailsData["SQL_PASSWORD"]
        self.databaseConnected = False

    def connect(self):
        try:
            self.mysqlConnector = mysql.connector.connect(
                host=self.sqlHost,
                user=self.sendMailsSqlUser,
                passwd=self.sendMailsSqlPW,
                database=self.sqlDatabase
            )
            self.databaseConnected = True

        except Error as error:
            print(error)

    def close(self):
        if self.databaseConnected:
            try:
                self.mysqlConnector.close()
                self.databaseConnected = False
            except Error as error:
                print(error)

    def getStatementTypeFromSQLQuery(self, sqlQuery_):
        statementType = sqlQuery_.partition(' ')[0]
        statementType = statementType.upper()
        allowedStatements = ["SELECT", "INSERT", "UPDATE"]
        if not statementType in allowedStatements :
            print("Error the given sql-query '{}' does not include any of the know sql-statement types. "
                  "Please use one of the following statements as the first word of your sql-query : {}!".format(sqlQuery_, allowedStatements))

        return statementType

    def executeSQLStatement(self, sqlQuery_, sqlValues_):
        statementType = self.getStatementTypeFromSQLQuery(sqlQuery_)

        if not self.databaseConnected:
            self.connect()

        if statementType == "INSERT":
            primaryKeyValue = ""
        elif statementType == "SELECT":
            result = ""

        try:
            mysqlCursor = self.mysqlConnector.cursor()
            mysqlCursor.execute(sqlQuery_, sqlValues_)

            if statementType == "INSERT":
                self.mysqlConnector.commit()
                primaryKeyValue = mysqlCursor.lastrowid
            if statementType == "UPDATE":
                self.mysqlConnector.commit()
            elif statementType == "SELECT":
                result = mysqlCursor.fetchall()

        except Error as error:
            print(error)

        finally:
            mysqlCursor.close()
            if statementType == "SELECT":
                return result
            elif statementType == "INSERT":
                return primaryKeyValue

    def insert(self, sqlQuery_, sqlValues_):
        primaryKeyValue = self.executeSQLStatement(sqlQuery_, sqlValues_)
        print("Successfully inserted query {} with values {}".format(sqlQuery_, sqlValues_))
        return primaryKeyValue

    def select(self, sqlQuery_, sqlValues_):
        return self.executeSQLStatement(sqlQuery_, sqlValues_)

    def update(self, sqlQuery_, sqlValues_):
        self.executeSQLStatement(sqlQuery_, sqlValues_)
        print("Successfully updated query {} with values {}".format(sqlQuery_, sqlValues_))

    def __del__(self):
        self.close()
