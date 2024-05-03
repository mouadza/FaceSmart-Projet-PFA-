import sqlite3

conn = sqlite3.connect('gestion_des_employes.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Code VARCHAR(30),
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    Age INTEGER,
    DepartmentID INTEGER,
    PositionID VARCHAR(30),
    Image BLOB,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS WorkSchedule (
    ScheduleID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeCode VARCHAR(20),
    WorkDate DATE,
    StartTime TIME,
    EndTime TIME,
    DayOff INTEGER,
    OvertimeHours DECIMAL(5, 2),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments (
    DepartmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    DepartmentName VARCHAR(30),
    Description VARCHAR(30),
    DepartmentHead INTEGER,
    FOREIGN KEY (DepartmentHead) REFERENCES Employees(EmployeeID)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Positions (
    PositionID INTEGER PRIMARY KEY AUTOINCREMENT,
    PositionName VARCHAR(30),
    Description VARCHAR(30),
    SalaryLevel DECIMAL(10, 2)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Performances (
    PerformanceID INTEGER PRIMARY KEY AUTOINCREMENT,
    EmployeeID INTEGER,
    EvaluationDate DATE,
    PerformanceRating INTEGER,
    AchievedGoals VARCHAR(30),
    Rewards VARCHAR(30),
    Penalties VARCHAR(30),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Managers (
    ManagerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    DepartmentID INTEGER,
    Email VARCHAR(30),
    Password VARCHAR(30),
    Role VARCHAR(30)
);
''')
conn.commit()
conn.close()
conn = sqlite3.connect('gestion_des_employes.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Tasks (
                    ID INTEGER PRIMARY KEY,
                    EmployeeCode VARCHAR(20),
                    ProjectID INTEGER,
                    TaskDescription VARCHAR(20),
                    Status VARCHAR(20) DEFAULT 'To-Do',
                    FOREIGN KEY(EmployeeCode) REFERENCES Employees(Code),,,,
                    FOREIGN KEY(ProjectID) REFERENCES Projects(ID)
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Projects (
                    ID INTEGER PRIMARY KEY,
                    ProjectName TEXT,
                    DepartmentID INTEGER,
                    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
                )''')

conn.commit()
conn.close()
