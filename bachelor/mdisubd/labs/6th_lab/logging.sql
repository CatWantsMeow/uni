create or replace directory log_files as '/home/meow/oracle/';


create or replace function open_log_file(
    file_name in nvarchar2
)
return utl_file.file_type
as
    file_handle utl_file.file_type;
begin
    file_handle := utl_file.fopen('LOG_FILES', file_name, 'a', 32767);
    return file_handle;

exception
    when utl_file.invalid_operation then
        return file_handle;
end;


create or replace procedure log_error(
    error_message in nvarchar2
)
as
    file_handle utl_file.file_type;
    date_time nvarchar2(100);
begin
    select to_char(current_timestamp, 'yyyy/mm/dd hh24:mi:ss')
    into date_time
    from dual;

    file_handle := open_log_file('errors.log');
    if not file_handle.id is null then
        utl_file.put(file_handle, '[ERROR, '|| date_time ||'] ' || error_message);
        utl_file.fclose(file_handle);
    end if;
end;


create or replace procedure log_info(
    info_message in nvarchar2
)
as
    file_handle utl_file.file_type;
    date_time nvarchar2(100);
begin
    select to_char(current_timestamp, 'yyyy/mm/dd hh24:mi:ss')
    into date_time
    from dual;

    file_handle := open_log_file('info.log');
    if file_handle.id is not null then
        utl_file.put(file_handle, '[INFO, '|| date_time ||'] ' || info_message);
        utl_file.fclose(file_handle);
    end if;
end;


create or replace trigger on_error
after servererror on database
declare
    error_message nvarchar2(500);
begin
    for i in 1..ora_server_error_depth loop
        error_message := ora_server_error_msg(i);
        log_error(error_message);
    end loop;
end;