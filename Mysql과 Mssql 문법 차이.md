## Mysql과 Mssql 문법 차이

mysql

```mysql
CREATE TABLE IF NOT EXISTS department (
	id CHAR(10) NOT NULL,
	name CHAR(10),
	constraint pk_department PRIMARY KEY (id)
);
```

mssql

```mssql
if not exists(select * from sysobjects where name='department' and xtype='U')
	create TABLE department (
		id CHAR(10) NOT NULL,
		name CHAR(10),
		constraint pk_department PRIMARY KEY (id)
);
```



inner join



