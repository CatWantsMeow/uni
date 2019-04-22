alter session set current_schema = meow;


create table user_groups
(
    id           int           not null,
    name         nvarchar2(50) not null,
    verbose_name nvarchar2(100) null,

    constraint user_group_pk primary key (id)
);


create table group_privileges
(
    id         int not null,
    name       nvarchar2(200) not null,
    group_id   int not null,
    table_name nvarchar2(200) not null,

    constraint group_privilege_pk primary key (id),
    constraint privilege_group_fk foreign key (group_id) references user_groups (id)
);


create table users
(
    id          int            not null,
    username    nvarchar2(200) not null,
    password    nvarchar2(200) not null,
    first_name  nvarchar2(100) not null,
    middle_name nvarchar2(100) null,
    last_name   nvarchar2(100) not null,
    email       nvarchar2(200) not null,
    phone       nvarchar2(30)  not null,
    group_id    int            not null,

    constraint user_id_pk primary key (id),
    constraint user_login_unique unique (username),
    constraint user_user_group_fk foreign key (group_id) references user_groups (id)
);


create table auth
(
    user_id   int       not null,
    token     nvarchar2(200) not null,
    last_auth timestamp null,

    constraint authentication_token_unique unique (token),
    constraint authenticated_user_id_pk primary key (user_id),
    constraint authenticated_user_id_fk foreign key (user_id) references users (id)
);


create table locations
(
    id           int            not null,
    country      nvarchar2(100) not null,
    region       nvarchar2(100) not null,
    city         nvarchar2(100) not null,
    street       nvarchar2(100) not null,
    house_number int            not null,

    constraint location_pk primary key (id)
);


create table shopping_malls
(
    id            int            not null,
    name          nvarchar2(100) not null,
    description   nvarchar2(100) null,
    floors_number int            null,
    parking_size  int            null,
    location_id   int            not null,

    constraint shopping_mall_id primary key (id),
    constraint shopping_mall_location_fk foreign key (location_id) references locations (id) on delete cascade
);


create table landlords
(
    id                int            not null,
    organization_name nvarchar2(100) not null,
    description       nvarchar2(200) null,
    user_id           int            not null,

    constraint landlord_pk primary key (id),
    constraint landlord_user_fk foreign key (user_id) references users (id) on delete cascade
);


create table tenants
(
    id        int            not null,
    user_id   int            not null,
    reqisites nvarchar2(200) not null,

    constraint tenant_pk primary key (id),
    constraint tenant_user_fk foreign key (user_id) references users (id) on delete cascade
);


create table prices
(
    id    int   not null,
    price float not null,

    constraint price_pk primary key (id)
);


create table shopping_areas
(
    id               int            not null,
    area             float          not null,
    description      nvarchar2(200) not null,
    landlord_id      int            not null,
    shopping_mall_id int            not null,
    price_id         int            not null,

    constraint shopping_area_pk primary key (id),
    constraint shopping_area_landlord_fk foreign key (landlord_id) references landlords (id) on delete cascade,
    constraint shopping_area_shopping_mall_fk foreign key (shopping_mall_id) references shopping_malls (id) on delete cascade,
    constraint shopping_area_price_fk foreign key (price_id) references prices (id) on delete cascade
);


create table rent_contracts
(
    id                 int            not null,
    code               int            not null,
    start_date         date           not null,
    end_date           date           not null,
    price              float          not null,
    additional_payment float          null,
    discount           float          null,
    checking_account   nvarchar2(50)  not null,
    requirements       nvarchar2(200) not null,
    tenant_id          int            not null,
    landlord_id        int            not null,
    shopping_area_id   int            not null,

    constraint rent_contract_pk primary key (id),
    constraint rent_contract_code_unique unique (code),
    constraint rent_contract_tenant_fk foreign key (tenant_id) references tenants (id) on delete cascade,
    constraint rent_contract_landlord_fk foreign key (landlord_id) references landlords (id) on delete cascade,
    constraint rent_contract_shopping_area_fk foreign key (shopping_area_id) references shopping_areas (id) on delete cascade
);


create table rented_shopping_areas
(
    rent_contract_id int not null,
    shopping_area_id int not null,

    constraint rented_shopping_areas_pk primary key (rent_contract_id, shopping_area_id),
    constraint rent_contract_fk foreign key (rent_contract_id) references rent_contracts (id) on delete cascade,
    constraint shopping_area_fk foreign key (shopping_area_id) references shopping_areas (id) on delete cascade
);

create table rent_requests
(
    tenant_id int not null,
    shopping_area_id int not null,
    description varchar2(300) null,

    constraint rent_request_pk primary key (tenant_id, shopping_area_id),
    constraint request_tenant_fk foreign key (tenant_id) references tenants (id) on delete cascade,
    constraint request_shopping_area_fk foreign key (shopping_area_id) references shopping_areas (id) on delete cascade
);


create table payments
(
    id               int   not null,
    receipt_date     date  not null,
    amount           float not null,
    rent_contract_id int   not null,

    constraint payment_pk primary key (id),
    constraint payment_rent_contract_fk foreign key (rent_contract_id) references rent_contracts (id) on delete cascade
);