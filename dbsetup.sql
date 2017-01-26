SET check_function_bodies = false;
-- ddl-end --

-- object: rest | type: SCHEMA --
 DROP SCHEMA rest CASCADE;
CREATE SCHEMA rest;
-- ddl-end --

SET search_path TO pg_catalog,public,rest;
-- ddl-end --

-- object: rest.person_pk_seq | type: SEQUENCE --
-- DROP SEQUENCE rest.person_pk_seq;
CREATE SEQUENCE rest.person_pk_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --

-- object: rest.cable_pk_seq | type: SEQUENCE --
-- DROP SEQUENCE rest.cable_pk_seq;
CREATE SEQUENCE rest.cable_pk_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --


-- object: rest.request_pk_seq | type: SEQUENCE --
-- DROP SEQUENCE rest.request_pk_seq;
CREATE SEQUENCE rest.request_pk_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --


-- object: rest.log_pk_seq | type: SEQUENCE --
-- DROP SEQUENCE rest.log_pk_seq;
CREATE SEQUENCE rest.log_pk_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --


-- ddl-end --
-- object: rest.login_pk_seq | type: SEQUENCE --
-- DROP SEQUENCE rest.login_pk_seq;
CREATE SEQUENCE rest.login_pk_seq
	INCREMENT BY 1
	MINVALUE 0
	MAXVALUE 2147483647
	START WITH 1
	CACHE 1
	NO CYCLE
	OWNED BY NONE;
-- ddl-end --


-- object: rest.Person | type: TABLE --
-- DROP TABLE rest.Person;
CREATE TABLE rest.Person(
	Id 			bigint NOT NULL DEFAULT nextval('rest.person_pk_seq'::regclass),
	FirstName 	text,
	LastName 	text,
	CONSTRAINT 	pk_person_id PRIMARY KEY (Id)

);
-- ddl-end --

-- object: rest.Log | type: TABLE --
-- DROP TABLE rest.Log;
CREATE TABLE rest.Log(
	Id 				bigint NOT NULL DEFAULT nextval('rest.log_pk_seq'::regclass),
	userid 			text,
	action 			text,
	ip			text,
	browser			text,
	time			date,
	comment 		text,
	CONSTRAINT 		pk_log_id PRIMARY KEY (Id)
);
-- ddl-end --

-- object: rest.request | type: TABLE --
-- DROP TABLE rest.request;
CREATE TABLE rest.request(
	Id 				bigint NOT NULL DEFAULT nextval('rest.request_pk_seq'::regclass),
	requestorId    bigint,
	requestType 	text,
	status			text,
	comment 		text,
	CONSTRAINT pk_request_id PRIMARY KEY (Id)
);
-- ddl-end --


-- object: rest.node | type: TABLE --
-- DROP TABLE rest.node;
CREATE TABLE rest.node(
	Id              bigint NOT NULL DEFAULT nextval('rest.request_pk_seq'::regclass),
	gisId 		    bigint,
	owner 		    text,
	nodetype		    text,
	material 	    text,
	speed		    text,
	technology 	    text,
	installdate		date,
	declaredate		date,
	status	    	    text,
	comment		    text,
	CONSTRAINT 	    pk_cable_id PRIMARY KEY (Id),
	CONSTRAINT 	    unique_gis_id UNIQUE (gisId)
);
-- ddl-end --

-- object: rest.Login | type: TABLE --
-- DROP TABLE rest.Login;
CREATE TABLE rest.Login(
	Id 			bigint NOT NULL DEFAULT nextval('rest.login_pk_seq'::regclass),
	PersonId    bigint NOT NULL,
	Email       text,
	Password 	text NOT NULL,
	CONSTRAINT 	unique_email UNIQUE (Email),
	CONSTRAINT	pk_login_id PRIMARY KEY (Id)

);
-- ddl-end --
-- object: Person_fk | type: CONSTRAINT --
-- ALTER TABLE rest.Login DROP CONSTRAINT Person_fk;
ALTER TABLE rest.Login ADD CONSTRAINT Person_fk FOREIGN KEY (PersonId)
REFERENCES rest.Person (Id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: Id | type: CONSTRAINT --
-- ALTER TABLE rest.Login  DROP CONSTRAINT Id;
ALTER TABLE rest.Login ADD CONSTRAINT Id UNIQUE (PersonId);
-- ddl-end --



-- ALTER TABLE rest.login  DROP CONSTRAINT person_id_fk;
ALTER TABLE rest.login ADD CONSTRAINT person_id_fk FOREIGN KEY (PersonId)
REFERENCES rest.person (Id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --



