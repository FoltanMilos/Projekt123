--tables skript
create table proj_user (
    u_id integer not null,
    u_name varchar2(50) not null,
    u_password varchar2(50) not null,
    u_active char(1) not null check(u_active in('A','N')),
    u_note varchar(255) null,
    u_privileges char(1) not null check(u_privileges in ('F','N','L')),
    u_priv_note varchar(255),
    CONSTRAINT pk_proj_user PRIMARY KEY (u_id),
    CONSTRAINT uniq_name UNIQUE (u_name)
);
create table proj_result(
    r_id integer not null,
    r_result_matrix varchar2(20),
    r_samples_count integer not null,
    constraint pk_proj_result primary key (r_id)
);
create table proj_model(
    m_id integer not null,
    r_id integer not null,
    u_id integer not null,
    m_active char(1) check (m_active in ('A','N')),
    m_type char(3) not null check(m_type in ('CNN','MLP','GEN')),
    m_weights_path varchar2(255) not null,
    m_structure_path varchar2(255) not null,
    constraint pk_proj_model primary key (m_id),
    constraint fk_model_user foreign key (u_id) references proj_user(u_id),
    constraint fk_model_result foreign key (r_id) references proj_result(r_id)
);
create table proj_data(
    d_id integer not null,
    m_id integer not null,
    d_name varchar2(50) not null,
    d_path varchar2(255) not null,
    d_path_type char(1) not null check(d_path_type in ('R','T','V')),
    constraint pk_proj_data primary key (d_id),
    constraint fk_model_data foreign key (m_id) references proj_model(m_id)
);
--DROP tables
--drop table proj_data;
--drop table proj_model;
--drop table proj_result;
--drop table proj_user;
-- create seq
drop sequence seq_id_user;
drop sequence seq_id_model;
drop sequence seq_id_data;
drop sequence seq_id_result;
create sequence seq_id_user start with 1 increment by 1;
create sequence seq_id_model start with 1 increment by 1;
create sequence seq_id_data start with 1 increment by 1;
create sequence seq_id_result start with 1 increment by 1;
-- create triggers
create or replace trigger id_user_autoinc
before insert on proj_user
for each row 
begin
:new.u_id:=seq_id_user.nextval;
if :new.u_privileges = 'F' THEN :new.u_priv_note:='Full access';
ELSIF :new.u_privileges = 'L' THEN :new.u_priv_note:='Limited access';
ELSIF :new.u_privileges = 'N' THEN :new.u_priv_note:='No access';
ELSE :new.u_priv_note:='--------';
END if;
end;
/
create or replace trigger id_model_autoinc
before insert on proj_model
for each row
begin
:new.m_id:=seq_id_model.nextval;
end;
/
create or replace trigger one_active_model
before insert on proj_model
for each row
begin
if :new.m_active='A' then update proj_model set m_active='N';
end if;
end;
/
create or replace trigger id_data_autoinc
before insert on proj_data
for each row
begin
:new.d_id:=seq_id_data.nextval;
end;
/
create or replace trigger id_result_autoinc
before insert on proj_result
for each row
begin
:new.r_id:=seq_id_result.nextval;
end;
/
-- user inserts
insert into proj_user(u_name,u_password,u_note,u_privileges,u_active) values('admin','admin','na testovanie, nech je superuser','F','N');
insert into proj_user(u_name,u_password,u_note,u_privileges,u_active) values('milos','heso','iny bezny uzivatel','L','N');
-- result insert
insert into proj_result(r_result_matrix) values('5;0;10;0');
-- model insert
insert into proj_model(u_id,r_id,m_weights_path,m_structure_path) 
values(1,1,'C:\SKOLA\7.Semester\Projekt 1\SarinaKristaTi\Projekt123\saved_model\cnn\model.h5','C:\SKOLA\7.Semester\Projekt 1\SarinaKristaTi\Projekt123\saved_model\cnn\model.json');
--data insert
insert into proj_data(m_id,d_name,d_path,d_path_type)
values(2,'data(10015)','C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\train\\','R');
insert into proj_data(m_id,d_name,d_path,d_path_type)
values(2,'data(10015)','C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\test\\','T');
insert into proj_data(m_id,d_name,d_path,d_path_type)
values(2,'data(10015)','C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\validation\\','V');

commit;
--test PART
select * from proj_user;
select * from proj_model;
select * from proj_result;
select * from proj_data;

commit;