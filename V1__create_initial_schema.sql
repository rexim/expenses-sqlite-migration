create table Places (
  id integer primary key,
  codename text not null,
  address text not null
);

create table Expenses (
  id integer primary key,
  date datetime not null,
  amount integer not null,
  name text not null,
  category text not null,
  place_id integer,
  foreign key (place_id) references Places(id)
);
