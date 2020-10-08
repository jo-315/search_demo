set client_encoding = 'UTF8';

create table home
(
  id serial primary key,
  name varchar not null,
  price integer not null,
  addres varchar not null,
  layout varchar not null
);

insert into home(name, price, addres, layout) values
  ('コーポ京都', 800000, '京都府京都市', '1LDK'),
  ('京都苑', 700000, '京都府京都市', '2LDK'),
  ('かきく京都', 650000, '京都府京都市', '1DK')
;