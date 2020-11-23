CREATE FUNCTION get_occupied_berth(train_id int, date_of_journey date, seat_type text)
RETURNS int AS $$
DECLARE 
    occupied_seat int;
    temp int;
    rec RECORD;
BEGIN
    occupied_seat := 0;
    for rec in (SELECT pnr from ticket where trainID=train_id and dateofjourney=date_of_journey)
    loop
        SELECT COUNT(*) INTO temp FROM ticketdetail WHERE pnr=rec.pnr AND berth LIKE seat_type || '%';
        occupied_seat := occupied_seat + temp;
    end loop;
    
    RETURN occupied_seat;
END;
$$ LANGUAGE plpgsql;




SELECT get_occupied_berth(3,'2020-11-21', 'A', 2);