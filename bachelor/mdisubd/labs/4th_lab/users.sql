create or replace function create_or_update_user(
    user_id in int,
    new_group_id in int,
    new_username in nvarchar2,
    new_password in nvarchar2,
    new_first_name in nvarchar2,
    new_middle_name in nvarchar2,
    new_last_name in nvarchar2,
    new_email in nvarchar2,
    new_phone in nvarchar2
)
return int
as
    old_user_id int;
    new_user_id int;
    user_count int;

    user_already_exists exception;
    pragma exception_init(user_already_exists, -20001);
begin
    select count(id) into user_count from users where username = new_username;
    if user_count > 0 and user_id is null then
        raise_application_error(-20001, 'User with specified username already exist');
    end if;

    select id into old_user_id from users where id=user_id;
    update users set
        group_id = new_group_id,
        username = new_username,
        password = new_password,
        first_name = new_first_name,
        middle_name = new_middle_name,
        last_name = new_last_name,
        email = new_email,
        phone = new_phone
    where id = old_user_id;
    return old_user_id;

exception
    when no_data_found then
        insert into users(
            id, group_id, username, password,
            first_name, middle_name, last_name,
            email, phone
        )
        values (
            null, new_group_id, new_username, new_password,
            new_first_name, new_middle_name, new_last_name,
            new_email, new_phone
        );
        select max(id) into new_user_id from users;
        log_info('User with name ' || new_username || ' created');
        return new_user_id;
end;


create or replace function create_or_update_landlord(
    landlord_id in int,
    user_id in int,
    new_username in nvarchar2,
    new_password in nvarchar2,
    new_first_name in nvarchar2,
    new_middle_name in nvarchar2,
    new_last_name in nvarchar2,
    new_email in nvarchar2,
    new_phone in nvarchar2,
    new_organization_name in nvarchar2,
    new_description in nvarchar2
)
return int
as
    landlords_group_id int;
    new_user_id int;
    old_landlord_id int;
    new_landlord_id int;
begin
    select id into landlords_group_id from user_groups where name='landlords';
    new_user_id := create_or_update_user(
        user_id, landlords_group_id, new_username,
        new_password, new_first_name, new_middle_name,
        new_last_name, new_email, new_phone
    );
    select id into old_landlord_id from landlords where id=landlord_id;
    update landlords set
        user_id = new_user_id,
        organization_name = new_organization_name,
        description = new_description
    where id = old_landlord_id;
    return old_landlord_id;

exception
    when no_data_found then
        insert into landlords(
            id, user_id,
            organization_name, description
        )
        values (
            null, new_user_id,
            new_organization_name, new_description
        );
        select max(id) into new_landlord_id from landlords;
        log_info('Landlord with name ' || new_username || ' created');
        return new_landlord_id;
end;


create or replace function create_or_update_tenant(
    tenant_id in int,
    user_id in int,
    new_username in nvarchar2,
    new_password in nvarchar2,
    new_first_name in nvarchar2,
    new_middle_name in nvarchar2,
    new_last_name in nvarchar2,
    new_email in nvarchar2,
    new_phone in nvarchar2,
    new_requisites in nvarchar2
)
return int
as
    tenants_group_id int;
    new_user_id int;
    old_tenant_id int;
    new_tenant_id int;
begin
    select id into tenants_group_id from user_groups where name='tenants';
    new_user_id := create_or_update_user(
        user_id, tenants_group_id, new_username,
        new_password, new_first_name, new_middle_name,
        new_last_name, new_email, new_phone
    );
    select id into old_tenant_id from tenants where id=tenant_id;
    update tenants set
        user_id = new_user_id,
        reqisites = new_requisites
    where id = old_tenant_id;
    return old_tenant_id;

exception
    when no_data_found then
        insert into tenants(
            id, user_id, reqisites
        )
        values (
            null, new_user_id, new_requisites
        );
        select max(id) into new_tenant_id from tenants;
        log_info('Tenant with name ' || new_username || ' created');
        return new_tenant_id;
end;


create or replace procedure delete_user(
    deleted_user_id in int
)
as
begin
    delete from landlords where user_id = deleted_user_id;
    delete from tenants where user_id = deleted_user_id;
    delete from users where id = deleted_user_id;
end;


create or replace procedure delete_landlord(
    deleted_landlord_id in int
)
as
    deleted_user_id int;
begin
    select user_id into deleted_user_id from landlords where id = deleted_landlord_id;
    delete from landlords where id = deleted_landlord_id;
    delete from users where id = deleted_user_id;
end;


create or replace procedure delete_tenant(
    deleted_tenant_id in int
)
as
    deleted_user_id int;
begin
    select user_id into deleted_user_id from tenants where id = deleted_tenant_id;
    delete from tenants where id = deleted_tenant_id;
    delete from users where id = deleted_user_id;
end;