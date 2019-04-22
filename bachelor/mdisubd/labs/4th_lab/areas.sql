create or replace function create_or_update_location(
    location_id in int,
    new_country in nvarchar2,
    new_region in nvarchar2,
    new_city in nvarchar2,
    new_street in nvarchar2,
    new_house_number in nvarchar2
)
return int
as
    old_location_id int;
    new_location_id int;
begin
    select id into old_location_id from locations where id=location_id;
    update locations set
        country = new_country,
        region = new_region,
        city = new_city,
        street = new_street,
        house_number = new_house_number
    where id = old_location_id;
    return old_location_id;

exception
    when no_data_found then
        insert into locations(
            id, country, region,
            city, street, house_number
        )
        values (
            null, new_country, new_region,
            new_city, new_street, new_house_number
        );
        select max(id) into new_location_id from locations;
        return new_location_id;
end;


create or replace function create_or_update_shopping_mall(
    shopping_mall_id in int,
    new_location_id in int,
    new_name in nvarchar2,
    new_description in nvarchar2,
    new_floors_number in int,
    new_parking_size in int
)
return int
as
    old_shopping_mall_id int;
    new_shopping_mall_id int;
begin
    select id into old_shopping_mall_id
    from shopping_malls
    where id=shopping_mall_id;

    update shopping_malls set
        location_id = new_location_id,
        name = new_name,
        description = new_description,
        floors_number = new_floors_number,
        parking_size = new_parking_size
    where id = old_shopping_mall_id;
    return old_shopping_mall_id;

exception
    when no_data_found then
        insert into shopping_malls(
            id, location_id, name, description,
            floors_number, parking_size
        )
        values (
            null, new_location_id, new_name, new_description,
            new_floors_number, new_parking_size
        );
        select max(id) into new_shopping_mall_id from shopping_malls;
        return new_shopping_mall_id;
end;


create or replace function create_or_update_shopping_area(
    shopping_area_id in int,
    new_landlord_id in int,
    new_shopping_mall_id in int,
    new_price_id in int,
    new_area in float,
    new_description in nvarchar2
)
return int
as
    old_shopping_area_id int;
    new_shopping_area_id int;
begin
    select id into old_shopping_area_id
    from shopping_areas
    where id=shopping_area_id;

    update shopping_areas set
        landlord_id = new_landlord_id,
        shopping_mall_id = new_shopping_mall_id,
        price_id = new_price_id,
        area = new_area,
        description = new_description
    where id = old_shopping_area_id;

    return old_shopping_area_id;

exception
    when no_data_found then
        insert into shopping_areas(
            id, landlord_id, shopping_mall_id, price_id,
            area, description
        )
        values (
            null, new_landlord_id, new_shopping_mall_id, new_price_id,
            new_area, new_description
        );
        select max(id) into new_shopping_area_id from shopping_areas;
        return new_shopping_area_id;
end;


create or replace function create_or_update_price(
    price_id in int,
    new_price in float
)
return int
as
    old_price_id int;
    new_price_id int;
begin
    select id into old_price_id
    from prices
    where id=price_id;

    update prices set
        price = new_price
    where id = old_price_id;

    return old_price_id;

exception
    when no_data_found then
        insert into prices(
            id, price
        )
        values (
            null, new_price
        );
        select max(id) into new_price_id from prices;
        return new_price_id;
end;


create or replace procedure delete_shopping_mall(
    mall_id in int
)
as
begin
    delete from shopping_malls where id = mall_id;
end;


create or replace procedure delete_shopping_area(
    area_id in int
)
as
begin
    delete from shopping_areas where id = area_id;
end;