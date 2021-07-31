--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: escrow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.escrow (
    id integer NOT NULL,
    seller_id bigint,
    buyer_id bigint,
    first_currency character varying(15),
    first_amount numeric,
    second_currency character varying(15),
    second_amount numeric,
    first_status boolean DEFAULT false,
    second_status boolean DEFAULT false
);


ALTER TABLE public.escrow OWNER TO postgres;

--
-- Name: escrow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.escrow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.escrow_id_seq OWNER TO postgres;

--
-- Name: escrow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.escrow_id_seq OWNED BY public.escrow.id;


--
-- Name: p2p_orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.p2p_orders (
    id integer NOT NULL,
    user_id bigint,
    first_currency character varying(15),
    first_amount numeric,
    second_currency character varying(15),
    second_amount numeric
);


ALTER TABLE public.p2p_orders OWNER TO postgres;

--
-- Name: p2p_orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.p2p_orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.p2p_orders_id_seq OWNER TO postgres;

--
-- Name: p2p_orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.p2p_orders_id_seq OWNED BY public.p2p_orders.id;


--
-- Name: requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requests (
    id character varying(50),
    user_id bigint,
    currency character varying(15),
    amount numeric,
    wallet_number character varying(150)
);


ALTER TABLE public.requests OWNER TO postgres;

--
-- Name: service_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.service_settings (
    exchange_commission numeric,
    escrow_exchange numeric
);


ALTER TABLE public.service_settings OWNER TO postgres;

--
-- Name: user_wallets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_wallets (
    user_id bigint NOT NULL,
    btc_address character varying(150),
    btc_balance numeric DEFAULT 0,
    eth_address character varying(150),
    eth_balance numeric DEFAULT 0,
    usdt_address character varying(150),
    usdt_balance numeric DEFAULT 0,
    ngn_balance numeric DEFAULT 0
);


ALTER TABLE public.user_wallets OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id bigint NOT NULL,
    language character varying(10) DEFAULT 'eng'::character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: escrow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escrow ALTER COLUMN id SET DEFAULT nextval('public.escrow_id_seq'::regclass);


--
-- Name: p2p_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p2p_orders ALTER COLUMN id SET DEFAULT nextval('public.p2p_orders_id_seq'::regclass);


--
-- Data for Name: escrow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.escrow (id, seller_id, buyer_id, first_currency, first_amount, second_currency, second_amount, first_status, second_status) FROM stdin;
1	733468275	1207634979	ETH	15.0	USDT	50.0	f	f
\.


--
-- Data for Name: p2p_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.p2p_orders (id, user_id, first_currency, first_amount, second_currency, second_amount) FROM stdin;
\.


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requests (id, user_id, currency, amount, wallet_number) FROM stdin;
120763497967093	1207634979	BTC	2.0	16EJLGn5qY2J8hNAZdJ38QhAUXNrP26tBe
120763497903829	1207634979	ETH	3373.0	0x8bdd275bdde80a6e7b9de27a7eaae177444e5071
120763497950694	1207634979	ETH	28.0	0x8bdd275bdde80a6e7b9de27a7eaae177444e5071
120763497927394	1207634979	ETH	15.0	0x8bdd275bdde80a6e7b9de27a7eaae177444e5071
120763497962031	1207634979	ETH	15.0	0x8bdd275bdde80a6e7b9de27a7eaae177444e5071
49169256642961	491692566	ETH	12.0	0x96495a8e7b0060f34fecacb39cd50a87a08aebc3
120763497958360	1207634979	ETH	15.0	0x7e5a7012544b9e7bb0a6516f60972df511065be3
120763497926958	1207634979	USDT	10.0	0x620b58aad7263598b21d9320021cbc120c73bb81
49169256641362	491692566	ETH	9000.0	0x7e5a7012544b9e7bb0a6516f60972df511065be3
73346827593287	733468275	ETH	555.0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90
\.


--
-- Data for Name: service_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.service_settings (exchange_commission, escrow_exchange) FROM stdin;
2	0.8
\.


--
-- Data for Name: user_wallets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_wallets (user_id, btc_address, btc_balance, eth_address, eth_balance, usdt_address, usdt_balance, ngn_balance) FROM stdin;
779941504	3MQdkkWoSKATTeaNFZoggPPdWtS1xST3hf	0	0x7e5a7012544b9e7bb0a6516f60972df511065be3	0	0x620b58aad7263598b21d9320021cbc120c73bb81	0	0
491692566	3MQdkkWoSKATTeaNFZoggPPdWtS1xST3hf	0	0x7e5a7012544b9e7bb0a6516f60972df511065be3	0	0x620b58aad7263598b21d9320021cbc120c73bb81	0	0
279640946	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
1207634979	3MQdkkWoSKATTeaNFZoggPPdWtS1xST3hf	5	0x7e5a7012544b9e7bb0a6516f60972df511065be3	0.0	0x620b58aad7263598b21d9320021cbc120c73bb81	0	0
733468275	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
819887525	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	666	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
1015467578	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	666	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
641564901	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, language) FROM stdin;
1207634979	eng
779941504	eng
491692566	eng
279640946	eng
733468275	eng
819887525	eng
1015467578	eng
641564901	eng
\.


--
-- Name: escrow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.escrow_id_seq', 2, true);


--
-- Name: p2p_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.p2p_orders_id_seq', 1, false);


--
-- Name: escrow escrow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escrow
    ADD CONSTRAINT escrow_pkey PRIMARY KEY (id);


--
-- Name: p2p_orders p2p_orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p2p_orders
    ADD CONSTRAINT p2p_orders_pkey PRIMARY KEY (id);


--
-- Name: user_wallets user_wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_wallets
    ADD CONSTRAINT user_wallets_pkey PRIMARY KEY (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- PostgreSQL database dump complete
--

