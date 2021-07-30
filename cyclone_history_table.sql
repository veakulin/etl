-- Table: public.cyclone_history

-- DROP TABLE public.cyclone_history;

CREATE TABLE IF NOT EXISTS public.cyclone_history
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    date_from integer NOT NULL,
    date_to integer NOT NULL,
    status character varying COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE public.cyclone_history
    OWNER to vasya;