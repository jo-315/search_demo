set client_encoding = 'UTF8';

create table home
(
  id serial primary key,
  name varchar not null,
  price integer not null,
  address varchar not null,
  layout varchar not null,
  station_distance integer not null,
  age integer not null,
  structure varchar not null
);

insert into home(name, price, address, layout, station_distance, age, structure) values
  ('コーポ京都', 80000, '京都府京都市', '1DK', 2, 15, '鉄筋系'),
  ('京都苑', 70000, '京都府京都市', '1DK', 12, 5, '鉄筋系'),
  ('かきく京都', 65000, '京都府京都市', '1K', 22, 4, '鉄筋系'),
  ('ソース京都', 30000, '京都府京都市', '1K', 32, 25, '鉄筋系'),
  ('コーポコーポ', 35000, '京都府京都市', '1DK', 3, 45, '鉄筋系'),
  ('ママママ', 75000, '京都府京都市', '1DK', 4, 55, '鉄筋系'),
  ('いるか', 77000, '京都府京都市', '1DK', 7, 52, '鉄筋系'),
  ('たちつてと', 100000, '京都府京都市', '1K', 32, 15, '鉄筋系'),
  ('枝豆', 165000, '京都府京都市', '1K', 15, 30, '鉄筋系'),
  ('イカ', 135000, '京都府京都市', '1DK', 20, 35, '鉄筋系'),
  ('イチゴ京都', 65000, '京都府京都市', '1K', 25, 14, '鉄筋系'),
  ('京都京都', 65500, '京都府京都市', '1K', 24, 22, '鉄筋系'),
  ('はんなり', 55000, '京都府京都市', '1K', 22, 20, '鉄筋系'),
  ('コーヒー', 45000, '京都府京都市', '1DK', 21, 10, '鉄筋系'),
  ('いいいい', 49000, '京都府京都市', '1DK', 19, 6, '鉄筋系'),
  ('でくそこ', 47000, '京都府京都市', '1K', 10, 8, '鉄筋系'),
  ('あああああ', 75000, '京都府京都市', '1K', 9, 42, '鉄筋系'),
  ('あかさ', 72000, '京都府京都市', '1DK', 8, 28, '鉄筋系'),
  ('ややや', 88000, '京都府京都市', '1DK', 4, 37, '鉄筋系'),
  ('SSSS', 90000, '京都府京都市', '1DK', 1, 31, '鉄筋系'),
  ('T京都', 98000, '京都府京都市', '1K', 16, 47, '鉄筋系'),
  ('あっdかさ', 109000, '京都府京都市', '1K', 15, 2, '鉄筋系'),
  ('AI京都', 25000, '京都府京都市', '1DK', 14, 9, '鉄筋系'),
  ('一刻堂', 35000, '京都府京都市', '1K', 24, 13, '鉄筋系'),
  ('哲也', 48000, '京都府京都市', '1DK', 28, 19, '鉄筋系'),
  ('メゾン', 65000, '京都府京都市', '1DK', 29, 36, '鉄筋系'),
  ('メゾン京都', 77000, '京都府京都市', '1K', 21, 31, '鉄筋系'),
  ('藤木家', 88000, '京都府京都市', '1K', 19, 38, '鉄筋系'),
  ('扇風機', 82000, '京都府京都市', '1K', 11, 29, '鉄筋系'),
  ('メメゾン', 84000, '京都府京都市', '1DK', 10, 27, '鉄筋系'),
  ('くすたた', 59000, '京都府京都市', '1DK', 14, 25, '鉄筋系'),
  ('磯垣', 56000, '京都府京都市', '1DK', 18, 18, '鉄筋系'),
  ('よっけ', 77000, '京都府京都市', '1DK', 4, 10, '鉄筋系'),
  ('ううう', 90000, '京都府京都市', '1DK', 6, 11, '鉄筋系'),
  ('ドキドキ', 101000, '京都府京都市', '1DK', 7, 9, '鉄筋系'),
  ('ワクワク京都', 34000, '京都府京都市', '1K', 9, 3, '鉄筋系'),
  ('京都一番', 47000, '京都府京都市', '1K', 32, 2, '鉄筋系')
;

create table search
(
  id serial primary key,
  name varchar not null,
  name_en varchar not null,
  search_order integer not null,
  search_type integer not null,
  step integer,
  digit integer,
  unit varchar,
  search_max integer,
  search_min integer,
  pull_menu_num integer,
  items varchar,
  ambiguous boolean not null
);

-- search_type テキスト→0 ラジオボタン→1 プルダウン→2

insert into search(name, name_en, search_order, search_type, ambiguous, step, unit) values
  ('名前', 'name', 0, 0, FALSE, 0,''),
  ('家賃', 'price', 1, 2, TRUE, 5000, '円'),
  ('住所', 'address', 2, 1, FALSE, 0, ''),
  ('間取り', 'layout', 3, 1, FALSE, 0, ''),
  ('駅からの距離', 'station_distance', 4, 2, TRUE, 5, '分'),
  ('築年数', 'age', 4, 2, TRUE, 5, '年'),
  ('構造', 'structure',5, 1, FALSE, 0, '')
;