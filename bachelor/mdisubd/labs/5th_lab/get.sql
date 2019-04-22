create or replace function get_free_areas(mall_id in int)
return sys_refcursor
as
    free_areas sys_refcursor;
begin
    open free_areas for
        select *
        from
            shopping_areas
        where
            shopping_mall_id=mall_id and
            id not in (select shopping_area_id from rented_shopping_areas);
    return free_areas;
end;


create or replace function get_shopping_malls
return sys_refcursor
as
    shopping_malls sys_refcursor;
begin
    open shopping_malls for
        select *
        from shopping_malls;
    return shopping_malls;
end;


create or replace function get_rent_contracts(t_id in int)
return sys_refcursor
as
    rent_contracts sys_refcursor;
begin
    open rent_contracts for
        select *
        from rent_contracts
        where tenant_id = t_id;
    return rent_contracts;
end;


create or replace function get_rented_areas(t_id in int)
return sys_refcursor
as
    rented_areas sys_refcursor;
begin
    open rented_areas for
        select *
        from shopping_areas
        where id in (
            select shopping_area_id
            from rent_contracts
            where tenant_id = t_id
        );
    return rented_areas;
end;



create or replace function get_areas(l_id in int)
return sys_refcursor
as
    areas sys_refcursor;
begin
    open areas for
        select *
        from shopping_areas
        where landlord_id = l_id;
    return areas;
end;


create or replace function get_tenant_rent_contracts(t_id in int)
return sys_refcursor
as
    contracts sys_refcursor;
begin
    open contracts for
        select rent_contracts.id,
               rent_contracts.code,
               rent_contracts.start_date,
               rent_contracts.end_date,
               rent_contracts.price,
               rent_contracts.additional_payment,
               rent_contracts.discount,
               rent_contracts.checking_account,
               rent_contracts.requirements,
               landlords.id,
               users.first_name,
               users.last_name,
               users.email,
               users.phone,
               shopping_areas.id,
               shopping_areas.description
        from rent_contracts, landlords, users, shopping_areas
        where rent_contracts.tenant_id = t_id and
              landlords.id = rent_contracts.landlord_id and
              landlords.user_id = users.id and
              rent_contracts.shopping_area_id = shopping_areas.id;
    return contracts;
end;


create or replace function get_landlord_rent_contracts(l_id in int)
return sys_refcursor
as
    contracts sys_refcursor;
begin
    open contracts for
        select rent_contracts.id,
               rent_contracts.code,
               rent_contracts.start_date,
               rent_contracts.end_date,
               rent_contracts.price,
               rent_contracts.additional_payment,
               rent_contracts.discount,
               rent_contracts.checking_account,
               rent_contracts.requirements,
               tenants.id,
               users.first_name,
               users.last_name,
               users.email,
               users.phone,
               shopping_areas.id,
               shopping_areas.description,
               is_active_rent_contract(rent_contracts.id) as is_active
        from rent_contracts, tenants, users, shopping_areas
        where rent_contracts.landlord_id = l_id and
              tenants.id = rent_contracts.landlord_id and
              tenants.user_id = users.id and
              rent_contracts.shopping_area_id = shopping_areas.id;
    return contracts;
end;


create or replace function get_payments(contract_id in int)
return sys_refcursor
as
    pays sys_refcursor;
begin
    open pays for
        select *
        from payments
        where rent_contract_id=contract_id;
    return pays;
end;


create or replace function get_rent_contract(l_id in int, c_id in int)
return sys_refcursor
as
    contract sys_refcursor;
begin
    open contract for
        select *
        from rent_contracts
        where landlord_id=l_id and id=c_id;
    return contract;
end;


select * from rent_contracts;

create or replace function get_users
return sys_refcursor
as
    u sys_refcursor;
begin
    open u for
        select *
        from users;
    return u;
end;


create or replace function get_location(
    location_id in int
)
return sys_refcursor
as
    l sys_refcursor;
begin
    open l for
        select *
        from locations
        where id = location_id;
    return l;
end;


create or replace function get_shopping_mall(
    mall_id in int
)
return sys_refcursor
as
    sm sys_refcursor;
begin
    open sm for
        select *
        from shopping_malls
        where id = mall_id;
    return sm;
end;


create or replace function get_shopping_areas(
    mall_id in int
)
return sys_refcursor
as
    sa sys_refcursor;
begin
    open sa for
        select *
        from shopping_areas
        where shopping_mall_id = mall_id;
    return sa;
end;


create or replace function get_group_name(
    g_id in int
)
return varchar2
as
    g_name varchar2(200);
begin
    select name into g_name from user_groups where id = g_id;
    return g_name;
end;


create or replace function get_locations
return sys_refcursor
as
    ls sys_refcursor;
begin
    open ls for
        select *
        from locations;
    return ls;
end;


create or replace function get_landlords
return sys_refcursor
as
    lds sys_refcursor;
begin
    open lds for
        select *
        from landlords, users
        where landlords.user_id = users.id;
    return lds;
end;


create or replace function get_landlord(
    landlord_id in int
)
return sys_refcursor
as
    l sys_refcursor;
begin
    open l for
        select *
        from landlords, users
        where landlords.id = landlord_id and
              landlords.user_id = users.id;
    return l;
end;


create or replace function get_prices
return sys_refcursor
as
    ps sys_refcursor;
begin
    open ps for
        select *
        from prices;
    return ps;
end;


create or replace function get_shopping_area(
    area_id in int
)
return sys_refcursor
as
    sa sys_refcursor;
begin
    open sa for
        select *
        from shopping_areas
        where id = area_id;
    return sa;
end;


create or replace function get_price(
    price_id in int
)
return sys_refcursor
as
    p sys_refcursor;
begin
    open p for
        select *
        from prices
        where id = price_id;
    return p;
end;


create or replace function get_rent_request(
    t_id in int,
    sa_id in int
)
return sys_refcursor
as
    rr sys_refcursor;
begin
    open rr for
        select *
        from rent_requests
        where tenant_id = t_id and
              shopping_area_id = sa_id;
    return rr;
end;


create or replace function get_rent_requests(
    t_id in int
)
return sys_refcursor
as
    rr sys_refcursor;
begin
    open rr for
        select shopping_areas.id,
               shopping_areas.description,
               rent_requests.description
        from rent_requests, shopping_areas
        where tenant_id = t_id and
              rent_requests.shopping_area_id = shopping_areas.id;
    return rr;
end;


create or replace function get_landlord_rent_requests(
    l_id in int
)
return sys_refcursor
as
    rr sys_refcursor;
begin
    open rr for
        select tenants.id,
               users.first_name,
               users.last_name,
               users.email,
               users.phone,
               shopping_areas.id,
               shopping_areas.description,
               rent_requests.description
        from rent_requests, tenants, shopping_areas, users
        where shopping_area_id in (
            select id
            from shopping_areas
            where landlord_id = l_id
        )
        and
            rent_requests.shopping_area_id = shopping_areas.id and
            rent_requests.tenant_id = tenants.id and
            tenants.user_id = users.id;
    return rr;
end;


create or replace function get_tenant_id(
    tok in varchar2
)
return int
as
    t_id int;
begin
    select tenants.id into t_id
    from auth, users, tenants
    where auth.token = tok and
          auth.user_id = users.id and
          tenants.user_id = users.id;
    return t_id;
exception
    when no_data_found then
    return -1;
end;


create or replace function get_landlord_id(
    tok in varchar2
)
return int
as
    l_id int;
begin
    select landlords.id into l_id
    from auth, users, landlords
    where auth.token = tok and
          auth.user_id = users.id and
          landlords.user_id = users.id;
    return l_id;
exception
    when no_data_found then
    return -1;
end;



create or replace function get_tenant_rent_contracts(
    t_id in int
)
return sys_refcursor
as
    rc sys_refcursor;
begin
    open rc for
        select *
        from rent_contracts
        where tenant_id = t_id;
    return rc;
end;


create or replace function get_shopping_area(
    area_id in int
)
return sys_refcursor
as
    a sys_refcursor;
begin
    open a for
        select *
        from shopping_areas
        where id = area_id;
    return a;
end;


create or replace function get_landlord_info(
    landlord_id in int
)
return sys_refcursor
as
    l sys_refcursor;
begin
    open l for
        select users.first_name, users.last_name, landlords.organization_name
        from landlords, users
        where landlords.id = landlord_id and
              users.id = landlords.user_id;
    return l;
end;


create or replace function inc(
    num in out int
)
return int
as
begin
    num := num + 1;
    return num;
END;