create or replace function create_or_update_contract(
    rent_contract_id in int,
    new_tenant_id in int,
    new_landlord_id in int,
    new_shopping_area_id int,
    new_code in int,
    new_start_date in date,
    new_end_date in date,
    new_price in float,
    new_additional_payment in float,
    new_discount in float,
    new_checking_account in nvarchar2,
    new_requirements in nvarchar2
)
return int
as
    old_rent_contract_id int;
    new_rent_contract_id int;
begin
    select id into old_rent_contract_id
    from rent_contracts
    where id=rent_contract_id;

    update rent_contracts set
        tenant_id = new_tenant_id,
        landlord_id = new_landlord_id,
        shopping_area_id = new_shopping_area_id,
        code = new_code,
        start_date = new_start_date,
        end_date = new_end_date,
        price = new_price,
        additional_payment = new_additional_payment,
        discount = new_discount,
        checking_account = new_checking_account,
        requirements = new_requirements
    where id = old_rent_contract_id;

    return old_rent_contract_id;

exception
    when no_data_found then
        insert into rent_contracts(
            id, tenant_id, landlord_id, shopping_area_id, code,
            start_date, end_date, price, additional_payment, discount,
            checking_account, requirements
        )
        values (
            null, new_tenant_id, new_landlord_id, new_shopping_area_id, new_code,
            new_start_date, new_end_date, new_price, new_additional_payment, new_discount,
            new_checking_account, new_requirements
        );
        select max(id) into new_rent_contract_id from rent_contracts;
        return new_rent_contract_id;
end;


create or replace function delete_rent_contract(
    l_id in int,
    contract_id in int
)
return int
as
    rents_count int;
    contract int;
begin
    select count(*) into rents_count
    from rented_shopping_areas
    where rent_contract_id = contract_id;

    if rents_count > 0 then
        return -2;
    end if;

    select id into contract
    from rent_contracts
    where id = contract_id and landlord_id = l_id;

    delete from payments where rent_contract_id = contract_id;
    delete from rent_contracts where id = contract_id;
    return 0;

exception
    when no_data_found then
        return -1;
end;


create or replace function is_active_rent_contract(
    contract_id in int
)
return int
as
    rents_count int;
begin
    select count(*) into rents_count
    from rented_shopping_areas
    where rent_contract_id = contract_id;

    return rents_count;
end;


create or replace function start_rent(
    l_id in int,
    contract_id in int
)
return int
as
    area_id int;
begin
    select shopping_area_id into area_id
    from rent_contracts
    where id = contract_id and landlord_id = l_id;

    insert into rented_shopping_areas(
        rent_contract_id, shopping_area_id
    )
    values (
        contract_id, area_id
    );
    return 0;

exception
    when no_data_found then
        return -1;
end;


create or replace function end_rent(
    l_id in int,
    contract_id in int
)
return int
as
    area_id int;
begin
    select shopping_area_id into area_id
    from rent_contracts
    where id = contract_id and landlord_id = l_id;

    delete from rented_shopping_areas
    where rent_contract_id = contract_id and
          shopping_area_id = area_id;
    return 0;

exception
    when no_data_found then
        return -1;
end;


create or replace function create_payment(
    payment_id in int,
    rent_contract_id in int,
    payment_amount in int
)
return int
as
    new_payment_id int;
begin
    insert into payments(
        id, rent_contract_id, amount, receipt_date
    )
    values (
        null, rent_contract_id, payment_amount, sysdate
    );
    select max(id) into new_payment_id from rent_contracts;
    return new_payment_id;
end;


create or replace procedure create_rent_request(
    new_tenant_id in int,
    new_shopping_area_id in int,
    new_description in varchar2
)
as
begin
    insert into rent_requests(
        tenant_id, shopping_area_id, description
    )
    values (
        new_tenant_id, new_shopping_area_id, new_description
    );
end;


create or replace function delete_rent_request(
    t_id in int,
    a_id in int
)
return int
as
    rr int;
begin
    select tenant_id into rr from rent_contracts where tenant_id = t_id and shopping_area_id = a_id;
    delete from rent_requests where tenant_id = t_id and shopping_area_id = a_id;
    return 0;

exception
    when no_data_found then
        return -1;
end;
