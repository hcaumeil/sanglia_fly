create table if not exists records (
  origin character varying not null,
  received_at timestamptz not null default now(),
  latitude float not null,
  longitude float not null,
  altitude float not null,
  orientation integer not null,
  speed float not null,
  type character varying not null,
  primary key (origin, received_at)
);
