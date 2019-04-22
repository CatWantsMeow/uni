create or replace procedure clear_data
as
    type names_array is varray(13) of varchar2(100);
    table_names names_array := names_array(
        'rented_shopping_areas',
        'payments',
        'rent_contracts',
        'shopping_areas',
        'landlords',
        'tenants',
        'auth',
        'users',
        'shopping_malls',
        'locations',
        'group_privileges',
        'user_groups',
        'prices'
    );
    i int;
begin
    for i in 1..table_names.count loop
        execute immediate 'delete from ' || table_names(i);
    end loop;
end;


create or replace procedure init_sequences
as
    type names_array is varray(11) of varchar2(100);

    seq_cursor sys_refcursor;
    seq_name varchar2(200);
    i int;

    seq_names names_array := names_array(
        'user',
        'tenant',
        'landlord',
        'location',
        'payment',
        'price',
        'rent_contract',
        'shopping_area',
        'shopping_mall',
        'user_group',
        'group_privilege'
    );
begin
    open seq_cursor for select sequence_name from user_sequences;
    loop
        fetch seq_cursor into seq_name;
        exit when seq_cursor%notfound;
        execute immediate 'drop sequence ' || seq_name;
    end loop;

    for i in 1..seq_names.count loop
        execute immediate 'create sequence ' || seq_names(i) || '_id_seq';
    end loop;
end;


create or replace procedure init_shopping_malls
as
    location_id int;
    shopping_mall_id int;
    shopping_area_id int;
    landlord_id int;
    price_id int;
begin
    select id into landlord_id
    from (
        select *
        from landlords
        order by dbms_random.value
    )
    where rownum=1;

    location_id := create_or_update_location(
        null, n'Беларусь', n'Минская', n'Минск', n'Гикало', 9
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Pandas',
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        10, 1024
    );

    price_id := create_or_update_price(null, 100);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        200, 'Vivamus ac tristique sapien.'
    );

    price_id := create_or_update_price(null, 150);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        100, 'Curabitur gravida dolor eget neque volutpat, a consequat dolor tincidunt.'
    );

    select id into landlord_id
    from (
        select *
        from landlords
        order by dbms_random.value
    )
    where rownum=1;

    price_id := create_or_update_price(null, 40);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        500, 't vulputate mi dolor, pharetra eleifend ex dignissim vel.'
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Foxes',
        'Nullam posuere semper diam, non scelerisque ex scelerisque ac.',
        5, 1032
    );

    price_id := create_or_update_price(null, 40);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        1500, 'Cras dui ante, rutrum vitae vehicula a, dictum faucibus metus.'
    );

    select id into landlord_id
    from (
        select *
        from landlords
        order by dbms_random.value
    )
    where rownum=1;

    price_id := create_or_update_price(null, 10);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        100, 'Curabitur eget arcu tristique, accumsan dolor non, vulputate justo.'
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Hedgehogs',
        'In quis lacinia quam. Proin tristique ultricies pellentesque.',
        10, 500
    );

    select id into landlord_id
    from (
        select *
        from landlords
        order by dbms_random.value
    )
    where rownum=1;

    price_id := create_or_update_price(null, 20);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        200, 'Quisque condimentum augue dui, vitae vestibulum risus ornare vitae. '
    );

    price_id := create_or_update_price(null, 500);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        130, 'Vestibulum sit amet finibus nisi. Curabitur placerat interdum odio et feugiat.'
    );

    price_id := create_or_update_price(null, 120);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        212, 'Cras dui ante, rutrum vitae vehicula a, dictum faucibus metus.'
    );

    select id into landlord_id
    from (
        select *
        from landlords
        order by dbms_random.value
    )
    where rownum=1;

    location_id := create_or_update_location(
        null, n'Беларусь', n'Минская', n'Минкс', n'П. Бровки', 8
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Eagles',
        'Curabitur mollis volutpat sapien sed ullamcorper.',
        4, 1200
    );

    price_id := create_or_update_price(null, 400);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        100, 'Quisque condimentum augue dui, vitae vestibulum risus ornare vitae.'
    );

    price_id := create_or_update_price(null, 500);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        890, 'Proin at elit sem. Praesent feugiat risus quis ipsum ullamcorper varius.'
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Owls',
        'Cras dui ante, rutrum vitae vehicula a, dictum faucibus metus.',
        5, 1032
    );

    price_id := create_or_update_price(null, 130);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        120, 'Sed at ultricies nisl, a sollicitudin arcu.'
    );

    select id into landlord_id
    from (
        select *
        from landlords
        order by dbms_random.value
    )
    where rownum=1;

    location_id := create_or_update_location(
        null, n'Беларусь', n'Минская', n'Минск', n'Дзержинского', 104
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Whales',
        ' Vestibulum ante ipsum primis in faucibus orci luctus et.',
        5, 23
    );

    price_id := create_or_update_price(null, 30);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        1500, 'Nullam posuere semper diam, non scelerisque ex scelerisque ac.'
    );

    price_id := create_or_update_price(null, 140);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        300, 'Proin at elit sem. Praesent feugiat risus quis ipsum ullamcorper varius.'
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Dolphins',
        'Vestibulum eget vulputate massa, nec posuere ipsum.',
        3, 3423
    );

    price_id := create_or_update_price(null, 90);
    shopping_area_id := create_or_update_shopping_area(
        null, landlord_id, shopping_mall_id, price_id,
        890, ' Praesent feugiat risus quis ipsum ullamcorper varius.'
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Sharks',
        'Duis a nisi et libero malesuada rutrum vitae vel nibh.',
        3, 20
    );

    location_id := create_or_update_location(
        null, n'Беларусь', n'Минская', n'Минск', n'Немига', 5
    );

    shopping_mall_id := create_or_update_shopping_mall(
        null, location_id, 'Cats',
        'Proin at elit sem. Praesent feugiat risus quis ipsum ullamcorper varius.',
        12, 320
    );
end;


create or replace procedure init_groups
as
    type names_array is varray(40) of varchar2(30);
    admins_functions names_array := names_array(
        'get_areas',
        'get_free_areas',
        'get_payments',
        'get_rent_contracts',
        'get_rent_contract',
        'get_rented_areas',
        'get_shopping_malls',
        'get_users',
        'login',
        'logout',
        'authenticate',
        'create_or_update_shopping_mall',
        'delete_shopping_mall',
        'create_or_update_shopping_area',
        'delete_shopping_area'
    );
    landlords_functions names_array := names_array(
        'get_areas',
        'get_free_areas',
        'get_payments',
        'get_rent_contracts',
        'get_rent_contract',
        'get_rented_areas',
        'get_shopping_malls',
        'get_users',
        'get_landlord_rent_requests',
        'get_landlord_rent_contracts',
        'delete_rent_contract',
        'delete_rent_request',
        'is_active_rent_contract',
        'create_or_update_contract',
        'start_rent',
        'end_rent',
        'create_payment',
        'start_rent',
        'end_rent',
        'login',
        'logout',
        'authenticate'
    );
    tenants_functions names_array := names_array(
        'create_rent_request',
        'delete_rent_request',
        'get_rent_request',
        'get_rent_requests',
        'get_tenant_rent_contracts',
        'get_shopping_area',
        'get_landlord_info'
    );

    privilege_id int;
    group_id int;
begin
    group_id := create_or_update_group(null, 'admins', n'Администраторы');
    for i in 1..admins_functions.count loop
        privilege_id := create_or_update_privilege(null, group_id, 'execute', admins_functions(i));
    end loop;

    group_id := create_or_update_group(null, 'landlords', n'Арендодатели');
    for i in 1..landlords_functions.count loop
        privilege_id := create_or_update_privilege(null, group_id, 'execute', landlords_functions(i));
    end loop;

    group_id := create_or_update_group(null, 'tenants', n'Арендаторы');
    for i in 1..tenants_functions.count loop
        privilege_id := create_or_update_privilege(null, group_id, 'execute', tenants_functions(i));
    end loop;

    create_groups();
end;


create or replace procedure init_users
as
    user_id int;
    location_id int;
    admins_group_id int;
begin
    select id into admins_group_id from user_groups where name = 'admins';

    user_id := create_or_update_user(
        null, admins_group_id, 'admin', 'admin', 'Ярош', 'Георгий', 'Иванович',
        'cat.wants.meow@gmail.com', '+375293327730'
    );

    user_id := create_or_update_user(
        null, admins_group_id, 'jack', 'jack123', 'Jack', 'Build', 'House',
        'jack.build.house@gmail.com', '+13221312312'
    );

    user_id := create_or_update_landlord(
        null, null, 'john', 'john123', 'John', 'Jack', 'Jonson',
        'john.jonson@gmail.com', '+43423423432',
        'Pur-pur-pur', 'Some words about John'
    );

    user_id := create_or_update_landlord(
        null, null, 'will', 'will123', 'Will', 'Bill', 'William',
        'will.bill@gmail.com', '+4242342342',
        'Kudah-kudah', 'Some words about Will'
    );

    user_id := create_or_update_tenant(
        null, null, 'charlie', 'charlie123', 'Charlie', 'James', 'Smith',
        'charlie.smith@gmail.com', '+4324243242',
        'Requisites from Charlie Smith'
    );

    user_id := create_or_update_tenant(
        null, null, 'james', 'james123', 'James', 'Robert', 'Wilson',
        'james.wilson@gmail.com', '+432432432',
        'Requisites from James Wilson'
    );

    user_id := create_or_update_tenant(
        null, null, 'sherlock', 'sherlock123', 'Sherlock', 'James', 'Holmes',
        'sherlock.holmes@gmail.com', '+42342342',
        'Requisites from Sherlock'
    );
end;


create or replace procedure init_rent_contracts
as
    landlord_id int;
    tenant_id int;
    shopping_area_cursor sys_refcursor;
    area_id int;
    rent_contract_id int;
    payment_id int;
    price_amount float;
    code int := 0;
begin
    open shopping_area_cursor for select id, landlord_id from shopping_areas where id < 5;
    loop
        fetch shopping_area_cursor into area_id, landlord_id;
        exit when shopping_area_cursor%notfound;

        select id into tenant_id
        from (
            select *
            from tenants
            order by dbms_random.value
        )
        where rownum = 1;

        select price into price_amount
        from prices
        where id in (
            select price_id
            from shopping_areas
            where id = area_id
        );

        create_rent_request(
            tenant_id, area_id, 'Some request'
        );

        rent_contract_id := create_or_update_contract(
            null, tenant_id, landlord_id, area_id, inc(code),
            to_date('2016/04/30', 'yyyy/mm/dd'),
            to_date('2016/06/30', 'yyyy/mm/dd'),
            price_amount, 0, 0, '43242332',
            'Mauris cursus dui mi, in maximus nisi tempus sit amet.
             Curabitur mollis volutpat sapien sed ullamcorper.
             Vestibulum sit amet finibus nisi. Curabitur placerat.'
        );

        payment_id := create_payment(null, rent_contract_id, 20);
        payment_id := create_payment(null, rent_contract_id, 40);
        rent_contract_id := start_rent(landlord_id, rent_contract_id);
    end loop;
end;


declare
begin
    clear_data();
    init_sequences();
    init_groups();
    init_users();
    init_shopping_malls();
    init_rent_contracts();
end;