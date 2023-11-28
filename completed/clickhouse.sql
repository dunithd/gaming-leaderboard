--table definitions

CREATE DATABASE foo;

CREATE TABLE IF NOT EXISTS foo.scores_raw
(
    event_id String,
    game_id UInt64,
    player String,
    created_at DateTime,
    score UInt32
) ENGINE = Kafka()
SETTINGS
    kafka_broker_list = 'redpanda:9092',
    kafka_topic_list = 'gameplays',
    kafka_group_name = 'clickhouse-group',
    kafka_format = 'JSON'


CREATE MATERIALIZED VIEW foo.scores_view
ENGINE = Memory
AS
SELECT * FROM foo.scores_raw
SETTINGS
stream_like_engine_allow_direct_select = 1;

select 
sv.player,
sum(score) 
from foo.scores_view as sv
group by player
order by sum(score) desc
limit 10;