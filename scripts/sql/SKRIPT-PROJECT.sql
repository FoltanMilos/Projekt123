ALTER TRIGGER id_data_autoinc DISABLE;
ALTER TRIGGER id_model_autoinc DISABLE;
ALTER TRIGGER id_result_autoinc DISABLE;
ALTER TRIGGER id_user_autoinc DISABLE;
ALTER TRIGGER one_active_model DISABLE;
--drops
drop table proj_data;
drop table proj_model;
drop table proj_result;
drop table proj_user;
--drop seq
drop sequence seq_id_user;
drop sequence seq_id_model;
drop sequence seq_id_data;
drop sequence seq_id_result;
--nahadzovanie tabuliek znovu
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
    r_matrix_a integer NOT null,
    r_matrix_b integer NOT null,
    r_matrix_c integer NOT null,
    r_matrix_d integer NOT null,
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
--TRIG
create or replace trigger id_data_autoinc
before insert on proj_data
for each row
begin
:new.d_id:=seq_id_data.nextval;
end;
/
create sequence seq_id_data start with 1 increment by 1;

SELECT D_ID, M_ID, D_NAME, D_PATH, D_PATH_TYPE
FROM PROJ_DATA;


-- user inserts
insert into proj_user(u_id,u_name,u_password,u_note,u_privileges,u_active) values(1,'admin','admin','na testovanie, nech je superuser','F','N');
insert into proj_user(u_id,u_name,u_password,u_note,u_privileges,u_active) values(2,'milos','heso','iny bezny uzivatel','L','N');
COMMIT;
-- result insert
insert into proj_result(r_id,R_MATRIX_A,R_MATRIX_B,R_MATRIX_C,R_MATRIX_D,R_SAMPLES_COUNT) values(1,10,5,15,25,100);
-- model insert
insert into proj_model(m_id,u_id,r_id,m_weights_path,m_structure_path,M_TYPE) 
values(0,1,1,'C:\SKOLA\7.Semester\Projekt 1\SarinaKristaTi\Projekt123\saved_model\cnn\model.h5','C:\SKOLA\7.Semester\Projekt 1\SarinaKristaTi\Projekt123\saved_model\cnn\model.json','CNN');
--data insert
insert into proj_data(d_id,m_id,d_name,d_path,d_path_type)
values(0,0,'data(10015)','C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\train\\','R');
insert into proj_data(d_id,m_id,d_name,d_path,d_path_type)
values(1,0,'data(10015)','C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\test\\','T');
insert into proj_data(d_id,m_id,d_name,d_path,d_path_type)
values(2,0,'data(10015)','C:\\SKOLA\\7.Semester\\Projekt 1\\SarinaKristaTi\\Projekt123\\dataset\\cnn\\validation\\','V');













