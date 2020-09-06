#dictionary for abbreviated dataset
dictionaryShort = { "age": 0,
		#"job"; - CHAR - ad(M)in, (B)lue-collar, (E)ntrepreneur, (H)ousemaid, (M)anagement, (R)etired, sel(F)-employed, ser(V)ices, (S)tudent, (T)echnician, (U)nemplyed, unknown(?)
		"job": {"admin.": 'M', "blue-collar": 'B', "entrepreneur": 'E', "housemaid": 'H', "management": 'M', "retired": 'R', 
			"self-employed": 'F', "services": 'V', "student": 'S', "technician": 'T', "unemployed": 'U', "unknown": '?'},
		#"marital"; - CHAR -  (D)ivorced, (M)arried, (S)ingle, unknown(?)
		"marital": {"divorced": 'D', "married": 'M', "single": 'S', "unknown": '?'},
		#"education"; - CHAR - (P)rimary, (S)econdary, (T)ertiary, unknown(?)
		"education": {"primary": "P", "secondary": 'S', "tertiary": 'T', "unknown": '?'},
		#"default"; - CHAR - (Y)es, (N)o, unknown(?)
		"default": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"balance"; -  INTEGER
		"balance": 2,
		#"housing"; -  CHAR - (Y)es, (N)o, unknown(?)
		"housing": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"loan"; - CHAR - (Y)es, (N)o, unknown(?)
		"loan":  {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"contact"; - CHAR - (C)ell, (T)elephone, (U)nknown ?
		"contact": {"cellular": 'C', "telephone": 'T', "unknown": '?'},
		#"day"; - TINYINT 
		"day": 0, 
		#"month"; TINYINT - (1-12) <-> (jan-dec)
		"month": {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12},
		#"duration"; - SMALLINT
		"duration": 1,
		#"campaign"; - TINYINT
		"campaign": 0,
		#"pdays"; - SMALLINT
		"pdays": 1,
		#"previous"; - SMALLINT
		"previous": 1,
		#"poutcome"; - CHAR - (S)uccess, (F)ailure, (O)ther, unknown(?)
		"poutcome": {"success": 'S', "failure": 'F', "other": 'O', "unknown": '?'},
		#"y"' - CHAR - (Y)es, (N)o
		"y": {"yes": 'Y', "no": 'N'}}

#This descibes the datatypes/mappings for the data which 
#includes additional fields, and some other differences
#tinyint - 0, smallint - 1, int - 2, float - -1 
#['age; - TINYINT
dictionaryAdditional = { "age": 0,
		#"job"; - CHAR - ad(M)in, (B)lue-collar, (E)ntrepreneur, (H)ousemaid, (M)anagement, (R)etired, sel(F)-employed, ser(V)ices, (S)tudent, (T)echnician, (U)nemplyed, unknown(?)
		"job": {"admin.": 'M', "blue-collar": 'B', "entrepreneur": 'E', "housemaid": 'H', "management": 'M', "retired": 'R', 
			"self-employed": 'F', "services": 'V', "student": 'S', "technician": 'T', "unemployed": 'U', "unknown": '?'},
		#"marital"; - CHAR -  (D)ivorced, (M)arried, (S)ingle, unknown(?)
		"marital": {"divorced": 'D', "married": 'M', "single": 'S', "unknown": '?'},
		#"education"; - CHAR - basic.(4)y, basic.(6)y, basic.(9)y, pro(F)essional.course, (H)igh.school, (U)niversity, (I)lliterate, unknown(?)
		"education": {"basic.4y": '4', "basic.6y": '6', "basic.9y": '9', "professional.course": 'F', "high.school": 'H', 
			"university.degree": 'U', "illiterate": 'I', "unknown": '?'},
		#"default"; - CHAR - (Y)es, (N)o, unknown(?)
		"default": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"housing"; -  CHAR - (Y)es, (N)o, unknown(?)
		"housing": {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"loan"; - CHAR - (Y)es, (N)o, unknown(?)
		"loan":  {"yes": 'Y', "no": 'N', "unknown": '?'},
		#"contact"; - CHAR - (C)ell, (T)elephone, (U)nknown ?
		"contact": {"cellular": 'C', "telephone": 'T', "unknown": '?'},
		#"month"; TINYINT - (1-12) <-> (jan-dec)
		"month": {"jan":1, "feb":2, "mar":3, "apr":4, "may":5, "jun":6, "jul":7, "aug":8, "sep":9, "oct":10, "nov":11, "dec":12},
		#"day_of_week"; - TINYINT 
		"day_of_week": {"mon":1, "tue":2, "wed":3, "thu":4, "fri":5, "sat":6, "sun":7},
		#"duration"; - SMALLINT
		"duration": 1,
		#"campaign"; - TINYINT
		"campaign": 0,

		#NO BALANCE IN THE "ADDITIONAL" DATASET
		#"balance"; -  INTEGER
		#"balance": 2,

		#"pdays"; - SMALLINT
		"pdays": 1,
		#"previous"; - SMALLINT
		"previous": 1,
		#"poutcome"; - CHAR - (S)uccess, (F)ailure, (O)ther, unknown(?), (N)onexistent
		"poutcome": {"success": 'S', "failure": 'F', "other": 'O', "unknown": '?', "nonexistent":'N'},
		#emp.var.rate DECIMAL(3,1)
		"emp.var.rate": -1,
		#cons.price.idx DECIMAL(6,3)
		"cons.price.idx": -1,
		#cons.conf.idx DECIMAL(4,1)
		"cons.conf.idx": -1,
		#euribor3m DECIMAL(5,3)
		"euribor3m": -1,
		#nr.employed DECIMAL(6,1)
		"nr.employed": -1,
		#"y"' - CHAR - (Y)es, (N)o
		"y": {"yes": 'Y', "no": 'N'}}
#This descibes the datatypes/mappings for SQL
#tinyint - 0, smallint-1, int-2
#['age; - TINYINT

#   age job marital education default  balance housing loan contact  day  month  duration  campaign  pdays  previous poutcome  y
insertQueryShort = """INSERT INTO people ( age, job, maritial, education, 
isDefault, balance, housing,
loan, contact, day, month,
duration, campaign, pdays,
previous, poutcome, y )
VALUES ( %s, %s, %s, %s, 
				%s, %s, %s, 
				%s, %s, %s, %s, 
				%s, %s, %s, 
				%s, %s, %s  )"""





#['age', 'job', 'marital', 'education', 'default', 'housing', 'loan', 'contact', 'month', 'day_of_week', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed', 'y']

createQueryAdditional = """ CREATE TABLE IF NOT EXISTS people_additional (
id INT AUTO_INCREMENT,
age TINYINT,
job CHAR(1),
maritial CHAR(1),
education CHAR(1),
isDefault CHAR(1),
housing CHAR(1),
loan CHAR(1),
contact CHAR(1),
day TINYINT,
month TINYINT,
duration SMALLINT,
campaign TINYINT,
pdays SMALLINT,
previous SMALLINT,
poutcome CHAR(1),
emp_var_rate DECIMAL(3,1),
cons_price_idx DECIMAL(6,3),
cons_conf_idx DECIMAL(4,1),
euribor3m DECIMAL(5,3),
nr_employed DECIMAL(6,1),
y CHAR(1),
PRIMARY KEY (id)) ENGINE = InnoDB
"""

insertQueryAdditional = """INSERT INTO people_additional ( age, job, maritial, education, 
isDefault, housing,
loan, contact, day, month,
duration, campaign, pdays,
previous, poutcome, emp_var_rate, cons_price_idx, cons_conf_idx, euribor3m,
nr_employed, y )

VALUES ( %s, %s, %s, %s, 
%s, %s,  
%s, %s, %s, %s, 
%s, %s, %s, 
%s, %s, %s, 
%s, %s, %s, 
%s, %s  )"""

createQueryShort = """ CREATE TABLE IF NOT EXISTS people (
id INT AUTO_INCREMENT,
age TINYINT,
job CHAR(1),
maritial CHAR(1),
education CHAR(1),
isDefault CHAR(1),
balance INT,
housing CHAR(1),
loan CHAR(1),
contact CHAR(1),
day TINYINT,
month TINYINT,
duration SMALLINT,
campaign TINYINT,
pdays SMALLINT,
previous SMALLINT,
poutcome CHAR(1),
y CHAR(1),
PRIMARY KEY (id)) ENGINE = InnoDB
"""


