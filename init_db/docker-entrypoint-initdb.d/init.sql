set client_encoding = 'UTF8';

create table home
(
  id serial primary key,
  name varchar not null,
  price integer not null,
  address varchar not null,
  layout varchar not null
);

insert into home(name, price, address, layout) values
  ('コーポ京都', 80000, '京都府京都市', '1LDK'),
  ('京都苑', 70000, '京都府京都市', '2LDK'),
  ('かきく京都', 65000, '京都府京都市', '1DK')
;