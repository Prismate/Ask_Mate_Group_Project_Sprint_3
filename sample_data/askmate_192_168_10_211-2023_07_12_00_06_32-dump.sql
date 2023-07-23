--
-- PostgreSQL database dump
--

-- Dumped from database version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 15.3

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: answer; Type: TABLE; Schema: public; Owner: askmate
--

CREATE TABLE public.answer (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer DEFAULT 0,
    question_id integer,
    message text,
    image text,
    user_id integer
);


ALTER TABLE public.answer OWNER TO askmate;

--
-- Name: answer_id_seq; Type: SEQUENCE; Schema: public; Owner: askmate
--

CREATE SEQUENCE public.answer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.answer_id_seq OWNER TO askmate;

--
-- Name: answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: askmate
--

ALTER SEQUENCE public.answer_id_seq OWNED BY public.answer.id;


--
-- Name: app_user; Type: TABLE; Schema: public; Owner: askmate
--

CREATE TABLE public.app_user (
    user_id integer NOT NULL,
    username character varying,
    password character varying,
    registration_ts timestamp without time zone DEFAULT now()
);


ALTER TABLE public.app_user OWNER TO askmate;

--
-- Name: app_user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: askmate
--

CREATE SEQUENCE public.app_user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.app_user_user_id_seq OWNER TO askmate;

--
-- Name: app_user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: askmate
--

ALTER SEQUENCE public.app_user_user_id_seq OWNED BY public.app_user.user_id;


--
-- Name: comment; Type: TABLE; Schema: public; Owner: askmate
--

CREATE TABLE public.comment (
    id integer NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    edited_count integer,
    user_id integer
);


ALTER TABLE public.comment OWNER TO askmate;

--
-- Name: comment_id_seq; Type: SEQUENCE; Schema: public; Owner: askmate
--

CREATE SEQUENCE public.comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.comment_id_seq OWNER TO askmate;

--
-- Name: comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: askmate
--

ALTER SEQUENCE public.comment_id_seq OWNED BY public.comment.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: askmate
--

CREATE TABLE public.question (
    id integer NOT NULL,
    submission_time timestamp without time zone,
    view_number integer DEFAULT 0,
    vote_number integer DEFAULT 0,
    title text,
    message text,
    image text,
    user_id integer
);


ALTER TABLE public.question OWNER TO askmate;

--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: askmate
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.question_id_seq OWNER TO askmate;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: askmate
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: question_tag; Type: TABLE; Schema: public; Owner: askmate
--

CREATE TABLE public.question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.question_tag OWNER TO askmate;

--
-- Name: tag; Type: TABLE; Schema: public; Owner: askmate
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name text
);


ALTER TABLE public.tag OWNER TO askmate;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: askmate
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO askmate;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: askmate
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: answer id; Type: DEFAULT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.answer ALTER COLUMN id SET DEFAULT nextval('public.answer_id_seq'::regclass);


--
-- Name: app_user user_id; Type: DEFAULT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.app_user ALTER COLUMN user_id SET DEFAULT nextval('public.app_user_user_id_seq'::regclass);


--
-- Name: comment id; Type: DEFAULT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.comment ALTER COLUMN id SET DEFAULT nextval('public.comment_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Data for Name: answer; Type: TABLE DATA; Schema: public; Owner: askmate
--

COPY public.answer (id, submission_time, vote_number, question_id, message, image, user_id) FROM stdin;
31	2023-07-11 09:15:45.818836	1	25	test		5
15	2023-06-27 23:50:45.914599	0	22	It's Peppa Pig the Fairy!		5
21	2023-06-29 23:23:54.70832	4	22	No idea what is this creature, but sure it's way too much pink for my taste!	dontlikepink.jpg	5
22	2023-06-29 23:35:27.436291	5	25	I would't bet on it, but it may be faster than my bike.	6d3a78ba4870a5ed0760f2cb8402.jpg	5
18	2023-06-29 22:49:44.385086	2	25	it's sure faster than mine! 	polonez-fso-1500-1310205.jpg	5
1	2017-04-28 16:49:00	22	0	You need to use brackets: my_list = []	hahaha.jpg	5
17	2023-06-29 22:40:30.585811	3	25	Bullocks, it's not!	hahaha.jpg	5
20	2023-06-29 23:21:43.403305	4	26	It's got to be Led Zeppelin	1200x1200bf-60.jpg	5
27	2023-07-02 13:37:38.466822	7	26	Guns N Roses	gunsnroses.jpg	5
24	2023-06-30 00:03:50.138938	7	26	AC piorun DC	ac-dc-logo-sticker-23565-p.jpg	5
19	2023-06-29 23:19:14.709798	5	26	Budgie! 	budgie-never-turn-your-back-on-a-friend-cover-art.jpg	5
32	2023-07-11 22:53:01.245601	2	26	Let's the rap rock!!!	mc-hammer.gif	7
33	2023-07-11 23:02:20.725874	0	34	Full Metal Jacket	Full_Metal_Jacket_poster.jpg	5
\.


--
-- Data for Name: app_user; Type: TABLE DATA; Schema: public; Owner: askmate
--

COPY public.app_user (user_id, username, password, registration_ts) FROM stdin;
5	grzegorz	$2b$12$e4iFNxrcCrLYSccJ0o0W9eLVFlvaKS9C7PKolv4YIzL6IFc3eWvSu	2023-07-10 10:30:32.445937
6	dupa	$2b$12$jsFtQc3ofm1qhP8tdWwYy.C3OM617etXzd9/qOcWj1R2swR6cblIS	2023-07-10 10:30:32.445937
7	McHammer	$2b$12$MBpcgVw5L2tv4aDUVgrQU.vNHq4OyrA0Kocy7BsA73LcqBl8uF0kG	2023-07-11 22:49:30.732792
8	GomerPyle	$2b$12$OC6Y0OOB0Tuyy/1iYVpH9.ZUsQg3OrYWU3fna2Bx6bhVtx5TGXPYu	2023-07-11 22:56:46.522614
\.


--
-- Data for Name: comment; Type: TABLE DATA; Schema: public; Owner: askmate
--

COPY public.comment (id, question_id, answer_id, message, submission_time, edited_count, user_id) FROM stdin;
57	26	\N	Can't touch this	2023-07-11 22:50:04.796925	0	7
58	26	32	Nice pants, not!	2023-07-11 22:55:20.609232	0	5
59	34	33	A pragmatic U.S. Marine observes the dehumanizing effects the Vietnam War has on his fellow recruits from their brutal boot camp training to the bloody street fighting in Hue.	2023-07-11 23:02:58.278002	0	8
17	22	15	sure that's Peppa	2023-07-05 07:58:09.181915	1	5
23	22	\N	Where did you find this image?	2023-07-03 18:56:12.180564	0	5
46	26	20	Stairway to heaven better than highway to hell	2023-07-04 09:04:56.038477	0	5
19	25	17	nice answer	2023-07-02 13:36:32.74408	0	5
29	1	\N	I don't have a clue what you're talking about!	2023-07-03 21:16:43.659136	0	5
26	2	\N	I don't have a clue!	2023-07-10 11:50:20.444097	1	5
37	26	19	The greatest band ever!	2023-07-03 21:48:04.632421	0	5
30	25	\N	Are you nuts!	2023-07-03 21:23:21.597423	0	5
43	26	27	GNR forever!	2023-07-04 09:01:52.708912	1	5
22	26	\N	Great question!	2023-07-03 18:54:07.531796	0	5
1	0	\N	Please clarify the question as it is too vague!	2023-07-03 21:55:50.038198	2	5
41	1	\N	my comment	2023-07-04 08:59:33.707887	0	5
47	25	22	Wigry 3	2023-07-04 09:46:27.059356	0	5
48	25	18	poloneza caro kupi ten co  jest naprawde glupi	2023-07-04 09:46:49.492422	0	5
45	26	24	Highway to hell	2023-07-04 09:03:14.737276	0	5
44	26	19	I like them too	2023-07-04 09:02:36.070351	0	5
2	0	1	I think you could use my_list = list() as well.	2023-07-03 21:38:52.091594	5	5
38	0	1	one two three	2023-07-11 11:56:08.828163	2	5
\.


--
-- Data for Name: question; Type: TABLE DATA; Schema: public; Owner: askmate
--

COPY public.question (id, submission_time, view_number, vote_number, title, message, image, user_id) FROM stdin;
34	2023-07-11 23:00:17.208762	0	0	Best war movies 	What is your favorite war movie?	Cannon_Fodder_3_cover_art.png	8
26	2023-06-29 23:19:00.073028	0	3	What's you favorite rock band?	Post your answer and let's vote to find a winner!	LP-PERFECT-UNU.jpg	5
1	2017-04-29 09:19:00	15	22	Wordpress loading multiple jQuery Versions	I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $(".myBook").booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)		5
0	2017-04-28 08:29:00	29	22	How to make lists in Python?	I am totally new to this, any hints?		5
2	2017-05-01 10:41:00	1364	83	Drawing canvas with an image picked with Cordova Camera Plugin	I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\r\n		5
25	2023-06-29 21:44:35.822912	0	2	Is this the fastest car in the World?	My misses seems to believe it is.	IMG_20201002_193136.jpg	5
22	2023-06-27 22:04:27.694887	0	23	Who is on this picture?	Is this some fairy?	0-7571_family-clipart-pig-peppa-pig-princess-png.png	5
\.


--
-- Data for Name: question_tag; Type: TABLE DATA; Schema: public; Owner: askmate
--

COPY public.question_tag (question_id, tag_id) FROM stdin;
2	3
25	6
1	3
26	7
26	8
0	1
0	4
22	9
1	4
34	10
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: askmate
--

COPY public.tag (id, name) FROM stdin;
1	python
2	sql
3	css
4	programming
6	CARS
7	music
8	rock'n'roll
9	cartoons
10	Movies
\.


--
-- Name: answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: askmate
--

SELECT pg_catalog.setval('public.answer_id_seq', 33, true);


--
-- Name: app_user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: askmate
--

SELECT pg_catalog.setval('public.app_user_user_id_seq', 8, true);


--
-- Name: comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: askmate
--

SELECT pg_catalog.setval('public.comment_id_seq', 59, true);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: askmate
--

SELECT pg_catalog.setval('public.question_id_seq', 34, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: askmate
--

SELECT pg_catalog.setval('public.tag_id_seq', 10, true);


--
-- Name: app_user app_user_pk; Type: CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.app_user
    ADD CONSTRAINT app_user_pk PRIMARY KEY (user_id);


--
-- Name: answer pk_answer_id; Type: CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);


--
-- Name: comment pk_comment_id; Type: CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);


--
-- Name: question pk_question_id; Type: CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);


--
-- Name: question_tag pk_question_tag_id; Type: CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);


--
-- Name: tag pk_tag_id; Type: CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);


--
-- Name: answer answer_app_user_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT answer_app_user_user_id_fk FOREIGN KEY (user_id) REFERENCES public.app_user(user_id);


--
-- Name: comment comment_app_user_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT comment_app_user_user_id_fk FOREIGN KEY (user_id) REFERENCES public.app_user(user_id);


--
-- Name: comment fk_answer_id; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id);


--
-- Name: answer fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: comment fk_question_id; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id);


--
-- Name: question_tag fk_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: question question_question_user_id_fk; Type: FK CONSTRAINT; Schema: public; Owner: askmate
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_question_user_id_fk FOREIGN KEY (user_id) REFERENCES public.app_user(user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

