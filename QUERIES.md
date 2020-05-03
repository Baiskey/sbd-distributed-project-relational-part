business queries

1. Return list of people with information how much children they have

`select per.name, per.surname, per.city, per.gender, per.birthday, count(par.parent_id) as number_of_children from person per
inner join parent par on par.parent_id=per.pesel
group by per.name, per.surname, per.city, per.gender, per.birthday, par.parent_id
order by number_of_children DESC;`

2. Return list of people with their homes and calculate how much days has passed since their moved

`select addr.city, addr.street, addr.house_number, to_date(c_in.moved_date,'YYYY-MM-DD') - CURRENT_DATE AS HOW_LONG_AGO, per.name, per.surname from address addr
inner join check_in c_in on c_in.address_id=addr.index
inner join person per on per.pesel=c_in.pesel;`