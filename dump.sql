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
-- Name: deposit_request; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deposit_request (
    id integer NOT NULL,
    user_id bigint,
    currency character varying(20),
    amount numeric
);


ALTER TABLE public.deposit_request OWNER TO postgres;

--
-- Name: deposit_request_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.deposit_request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.deposit_request_id_seq OWNER TO postgres;

--
-- Name: deposit_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.deposit_request_id_seq OWNED BY public.deposit_request.id;


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
    second_status boolean DEFAULT false,
    type character varying(10)
);


ALTER TABLE public.escrow OWNER TO postgres;

--
-- Name: escrow_chats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.escrow_chats (
    id bigint,
    link character varying(150)
);


ALTER TABLE public.escrow_chats OWNER TO postgres;

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
-- Name: fiat_fast_exchange; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fiat_fast_exchange (
    user_id bigint,
    first_currency character varying(10),
    first_amount numeric,
    second_currency character varying(10),
    second_amount numeric
);


ALTER TABLE public.fiat_fast_exchange OWNER TO postgres;

--
-- Name: history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.history (
    id bigint NOT NULL,
    user_id bigint,
    type character varying(20),
    first_currency character varying(5),
    first_amount numeric,
    second_currency character varying(5),
    second_amount numeric
);


ALTER TABLE public.history OWNER TO postgres;

--
-- Name: history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.history_id_seq OWNER TO postgres;

--
-- Name: history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.history_id_seq OWNED BY public.history.id;


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
    escrow_exchange numeric,
    cource_percent numeric,
    btcngn numeric,
    ethngn numeric,
    usdtngn numeric
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
    language character varying(10) DEFAULT 'eng'::character varying,
    username character varying(35)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: deposit_request id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deposit_request ALTER COLUMN id SET DEFAULT nextval('public.deposit_request_id_seq'::regclass);


--
-- Name: escrow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.escrow ALTER COLUMN id SET DEFAULT nextval('public.escrow_id_seq'::regclass);


--
-- Name: history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.history ALTER COLUMN id SET DEFAULT nextval('public.history_id_seq'::regclass);


--
-- Name: p2p_orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.p2p_orders ALTER COLUMN id SET DEFAULT nextval('public.p2p_orders_id_seq'::regclass);


--
-- Data for Name: deposit_request; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deposit_request (id, user_id, currency, amount) FROM stdin;
1	1207634979	NGN	15.0
2	1207634979	NGN	666.0
3	1207634979	NGN	10.0
4	1207634979	NGN	666.0
5	1207634979	NGN	666.0
7	137075690	NGN	0.0
\.


--
-- Data for Name: escrow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.escrow (id, seller_id, buyer_id, first_currency, first_amount, second_currency, second_amount, first_status, second_status, type) FROM stdin;
27	1207634979	733468275	USDT	100.0	BTC	1.0	f	f	escrow
28	1207634979	733468275	USDT	150.0	BTC	11.0	f	f	escrow
29	491692566	779941504	BTC	1.0	NGN	10000.0	f	t	p2p
30	1207634979	779941504	BTC	5.0	NGN	5.0	f	t	p2p
31	491692566	779941504	BTC	1.0	NGN	10000.0	f	t	p2p
32	491692566	779941504	BTC	1.0	NGN	10000.0	t	f	escrow
34	491692566	779941504	BTC	12.0	NGN	20000.0	f	t	p2p
35	779941504	491692566	BTC	0.005	NGN	30000.0	f	t	p2p
36	491692566	1207634979	BTC	1.0	NGN	10000.0	f	t	p2p
37	779941504	491692566	BTC	0.005	NGN	30000.0	f	t	p2p
38	491692566	779941504	BTC	12.0	NGN	20000.0	f	t	p2p
39	491692566	779941504	BTC	12.0	NGN	20000.0	f	t	p2p
\.


--
-- Data for Name: escrow_chats; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.escrow_chats (id, link) FROM stdin;
11	https://t.me/joinchat/J6WjmHwXe79jMzcy
22	https://t.me/joinchat/Qtq2yBeJk6dkMGFi
23	https://t.me/joinchat/8_bMQjOncxJkN2Uy
24	https://t.me/joinchat/cAx8eHQWWBEzYjky
25	https://t.me/joinchat/IJcCa-yDgfozMGUy
29	https://t.me/joinchat/BDCcE4yMNo00ODRi
34	https://t.me/joinchat/afTyl6IssyBjMTUy
36	https://t.me/joinchat/qPFdEkdgezthNmYy
37	https://t.me/joinchat/yExt3yAKlYVjYzEy
40	https://t.me/joinchat/GHgkJEcABK44NDIy
\.


--
-- Data for Name: fiat_fast_exchange; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fiat_fast_exchange (user_id, first_currency, first_amount, second_currency, second_amount) FROM stdin;
\.


--
-- Data for Name: history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.history (id, user_id, type, first_currency, first_amount, second_currency, second_amount) FROM stdin;
1	1207634979	withdraw	NGN	1000.0	None	0
2	1207634979	withdraw	NGN	100.0	None	0
3	1207634979	withdraw	NGN	1000.0	None	0
4	1207634979	withdraw	NGN	500.0	None	0
\.


--
-- Data for Name: p2p_orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.p2p_orders (id, user_id, first_currency, first_amount, second_currency, second_amount) FROM stdin;
2	491692566	BTC	1.0	USDT	100.0
4	779941504	BTC	0.0005	USDT	20.0
5	779941504	BTC	0.0005	NGN	20.0
6	491692566	ETH	1.0	BTC	0.1
7	1207634979	BTC	5.0	NGN	5.0
8	779941504	BTC	0.005	NGN	5000.0
9	491692566	BTC	1.0	NGN	10000.0
10	779941504	BTC	0.005	NGN	30000.0
11	491692566	BTC	12.0	NGN	20000.0
12	491692566	BTC	1.0	NGN	12345.0
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
13707569014596	137075690	USDT	0.0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90
\.


--
-- Data for Name: service_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.service_settings (exchange_commission, escrow_exchange, cource_percent, btcngn, ethngn, usdtngn) FROM stdin;
1.5	0.8	1	20	5	1
\.


--
-- Data for Name: user_wallets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_wallets (user_id, btc_address, btc_balance, eth_address, eth_balance, usdt_address, usdt_balance, ngn_balance) FROM stdin;
279640946	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
448010869	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	16	0
409770287	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
1888512414	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
819887525	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	666	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
1015467578	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	666	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
641564901	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
733468275	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	6.944	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0.0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
491692566	3MQdkkWoSKATTeaNFZoggPPdWtS1xST3hf	87.9	0x7e5a7012544b9e7bb0a6516f60972df511065be3	49.60	0x620b58aad7263598b21d9320021cbc120c73bb81	0	0
779941504	3MQdkkWoSKATTeaNFZoggPPdWtS1xST3hf	21.904	0x7e5a7012544b9e7bb0a6516f60972df511065be3	50.0	0x620b58aad7263598b21d9320021cbc120c73bb81	0	75000.0
1207634979	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	656.0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	500.0
137075690	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
269133220	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
428591372	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
599708480	19uQe9XuKAfkT7QT44ke4ryeZm44hBHFVx	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0xd959a62d66f50bf3646265ae6309efd6eaa18e90	0	0
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, language, username) FROM stdin;
733468275	eng	PlayInPython
279640946	eng	\N
819887525	eng	\N
1015467578	eng	\N
641564901	eng	\N
137075690	eng	\N
428591372	eng	\N
448010869	eng	\N
409770287	eng	GrynaZG
1207634979	eng	Only4Work
599708480	eng	DenysLiasota
491692566	eng	ken_vz
269133220	eng	olexanderboychuk
779941504	eng	Alexandr_entrepreneur
1888512414	eng	DesigGis
\.


--
-- Name: deposit_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.deposit_request_id_seq', 9, true);


--
-- Name: escrow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.escrow_id_seq', 40, true);


--
-- Name: history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.history_id_seq', 4, true);


--
-- Name: p2p_orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.p2p_orders_id_seq', 12, true);


--
-- Name: deposit_request deposit_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deposit_request
    ADD CONSTRAINT deposit_request_pkey PRIMARY KEY (id);


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

