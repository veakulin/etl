-- Table: public.cyclone

-- DROP TABLE public.cyclone;

CREATE TABLE IF NOT EXISTS public.cyclone
(
    id character varying COLLATE pg_catalog."default",
    name character varying COLLATE pg_catalog."default",
    date integer,
    "time" integer,
    event character varying COLLATE pg_catalog."default",
    status character varying COLLATE pg_catalog."default",
    latitude character varying COLLATE pg_catalog."default",
    longitude character varying COLLATE pg_catalog."default",
    max_wind integer,
    min_pressure integer,
    low_wind_ne integer,
    low_wind_se integer,
    low_wind_sw integer,
    low_wind_nw integer,
    moderate_wind_ne integer,
    moderate_wind_se integer,
    moderate_wind_sw integer,
    moderate_wind_nw integer,
    high_wind_se integer,
    high_wind_sw integer,
    high_wind_nw integer,
    high_wind_ne integer
)

TABLESPACE pg_default;

ALTER TABLE public.cyclone
    OWNER to vasya;