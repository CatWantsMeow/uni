create or replace function authenticate(
    tok nvarchar2
)
return int
as
    temp nvarchar2(200);
    now timestamp;
    last_auth_time timestamp;
    g_id int;
    u_id int;
begin
    select user_id into u_id from auth where token = tok;

--     select current_timestamp into now from dual;
--     select last_auth into last_auth_time from auth where user_id = u_id and token = tok;
--     if last_auth_time < (now - interval '20' minute) then
--         logout(u_id);
--         return -2;
--     end if;

    update auth set last_auth=now where user_id = u_id and token = tok;
    select group_id into g_id from users where id=u_id;
    return g_id;

exception
    when no_data_found then
        return -1;
end;


create or replace function login(
    name in nvarchar2,
    pass in nvarchar2,
    tok in nvarchar2
)
return int
as
    u_id int;
begin
    select id into u_id from users where username = name and password = pass;
    delete from auth where user_id = u_id;
    insert into auth values (u_id, tok, null);
    commit;
    return u_id;

exception
    when no_data_found then
        log_error('Incorrect login or password: ' || name || ', ' || pass);
        return -1;
end;

select * from auth;
delete from auth;


create or replace procedure logout(
    tok in nvarchar2
)
as
begin
    delete from auth where token = tok;
    commit;
end;


create or replace procedure create_groups
as
    groups_cursor sys_refcursor;
    g_id int;
    g_name varchar2(50);
    g_exists int;

    privileges_cursor sys_refcursor;
    p_name varchar2(200);
    p_table_name varchar2(200);

begin
    open groups_cursor for select id, name from user_groups;
    loop
        fetch groups_cursor into g_id, g_name;
        exit when groups_cursor%notfound;

        g_name := upper(g_name);
        select count(username) into g_exists from all_users where username = g_name;
        if g_exists > 0 then
            execute immediate 'drop user ' || g_name;
        end if;
        execute immediate 'create user ' || g_name || ' identified by ' || g_name || ' profile default';
        execute immediate 'grant create session to ' || g_name;

        open privileges_cursor for select name, table_name from group_privileges where group_id = g_id;
        loop
            fetch privileges_cursor into p_name, p_table_name;
            exit when privileges_cursor%notfound;
            execute immediate 'grant ' || p_name || ' on ' || p_table_name || ' to ' || g_name;
        end loop;
    end loop;
end;


create or replace function can_execute(
    user_tok in varchar2,
    function_name in varchar2
)
return int
as
    u_id int;
    g_id int;
    temp int;
begin
    select user_id into u_id from auth where token = user_tok;
    select group_id into g_id from users where id = u_id;

    select id into temp
    from group_privileges
    where group_id = g_id and table_name = function_name;
    return 1;

exception
    when no_data_found then
        return 0;
end;