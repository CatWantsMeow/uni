create or replace function create_or_update_group(
    group_id in int,
    new_name in nvarchar2,
    new_verbose_name in nvarchar2
)
return int
as
    old_group_id int;
    new_group_id int;
begin
    select id into old_group_id from user_groups where id = group_id;
    update user_groups set
        name = new_name,
        verbose_name = new_verbose_name
    where id = group_id;
    return group_id;

exception
    when no_data_found then
        insert into user_groups (
            id, name, verbose_name
        )
        values (
            null, new_name, new_verbose_name
        );
        select max(id) into new_group_id from user_groups;
        return new_group_id;
end;


create or replace function create_or_update_privilege(
    privilege_id in int,
    new_group_id in int,
    new_name in nvarchar2,
    new_table_name in nvarchar2
)
return int
as
    old_privilege_id int;
    new_privilege_id int;
begin
    select id into old_privilege_id from group_privileges where id = privilege_id;
    update group_privileges set
        group_id = new_group_id,
        name = new_name,
        table_name = new_table_name
    where id = privilege_id;
    return privilege_id;

exception
    when no_data_found then
        insert into group_privileges (
            id, group_id, name, table_name
        )
        values (
            null, new_group_id, new_name, new_table_name
        );
        select max(id) into new_privilege_id from group_privileges;
        return new_privilege_id;
end;