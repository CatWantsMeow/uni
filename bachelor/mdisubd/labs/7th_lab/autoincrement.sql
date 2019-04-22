create or replace trigger on_user_create
before insert on users
for each row
begin
    if :new.id is null then
        select user_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_landlord_create
before insert on landlords
for each row
begin
    if :new.id is null then
        select landlord_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_location_create
before insert on locations
for each row
begin
    if :new.id is null then
        select location_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_shopping_mall_create
before insert on shopping_malls
for each row
begin
    if :new.id is null then
        select shopping_mall_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_shopping_area_create
before insert on shopping_areas
for each row
begin
    if :new.id is null then
        select shopping_area_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_group_privilege_create
before insert on group_privileges
for each row
begin
    if :new.id is null then
        select group_privilege_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_tenant_create
before insert on tenants
for each row
begin
    if :new.id is null then
        select tenant_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_user_group_create
before insert on user_groups
for each row
begin
    if :new.id is null then
        select user_group_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_rent_contract_create
before insert on rent_contracts
for each row
begin
    if :new.id is null then
        select rent_contract_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_price_create
before insert on prices
for each row
begin
    if :new.id is null then
        select price_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_payment_create
before insert on payments
for each row
begin
    if :new.id is null then
        select payment_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_group_privilege_create
before insert on group_privileges
for each row
begin
    if :new.id is null then
        select group_privilege_id_seq.nextval into :new.id from dual;
    end if;
end;


create or replace trigger on_user_group_create
before insert on user_groups
for each row
begin
    if :new.id is null then
        select user_group_id_seq.nextval into :new.id from dual;
    end if;
end;
