create table users(user_id integer primary key, email string, phone integer, username string);
create table alerts(alert_id integer primary key, user_id integer, section_id integer, active boolean);
