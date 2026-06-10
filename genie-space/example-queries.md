# Genie Space example queries

Readable mirror of the 8 `instructions.example_question_sqls` in `lakewatch-research-agent.serialized.json`. Generated from the JSON; the JSON is the deploy source. Entities are generic placeholders (RFC 5737 documentation ranges), not lab-specific.

## 1. What is the normal set of processes and parent processes on a host over the last 7 days?

```sql
FROM lakewatch.gold.process_activity
|> WHERE device.hostname = 'WS-EXAMPLE-01' AND time >= current_timestamp() - INTERVAL 7 DAYS
     AND process.name IS NOT NULL
|> AGGREGATE count(*) AS events GROUP BY actor.process.name AS parent_process, process.name AS process
|> ORDER BY events DESC
|> LIMIT 50
```

## 2. Which processes ran on a host today that were never seen in the prior 30 days?

```sql
FROM lakewatch.gold.process_activity
|> WHERE device.hostname = 'WS-EXAMPLE-01' AND time >= current_timestamp() - INTERVAL 30 DAYS
     AND process.name IS NOT NULL
|> AGGREGATE count_if(time >= current_timestamp() - INTERVAL 1 DAY) AS today,
              count_if(time <  current_timestamp() - INTERVAL 1 DAY) AS prior_30d
   GROUP BY process.name AS process, process.cmd_line AS cmd_line
|> WHERE today > 0 AND prior_30d = 0
|> ORDER BY today DESC
```

## 3. What external destinations did a host connect to, and how much data left, in a time window?

```sql
FROM lakewatch.gold.network_activity
|> WHERE src_endpoint.ip = '198.51.100.23'
     AND time BETWEEN TIMESTAMP'2026-01-01 14:00:00' AND TIMESTAMP'2026-01-01 15:00:00'
|> AGGREGATE count(*) AS conns, sum(traffic.bytes_out) AS bytes_out
   GROUP BY dst_endpoint.ip AS dst_ip, dst_endpoint.port AS dst_port
|> ORDER BY bytes_out DESC
```

## 4. Is a destination IP a known threat indicator, and what does the feed say?

```sql
FROM lakewatch.bronze.c2intelfeeds
|> WHERE data:fields:ip::STRING = '203.0.113.10' AND data:indicator_class::STRING = 'c2'
|> AGGREGATE max(data:fields:ioc::STRING) AS feed_label, count(*) AS feed_rows
   GROUP BY data:fields:ip::STRING AS indicator_ip
```

## 5. Trace the parent process of PowerShell launched on a host.

```sql
FROM lakewatch.bronze.microsoft_winevtlog
|> WHERE data:source::STRING = 'Microsoft-Windows-Sysmon/Operational' AND data:Id::STRING = '1'
     AND data:host::STRING = 'WS-EXAMPLE-01' AND data:Message::STRING ILIKE '%Image: %powershell.exe%'
|> SELECT time,
     regexp_extract(data:Message::STRING,'ParentImage: ([^&]+)',1) AS parent_image,
     regexp_extract(data:Message::STRING,'Image: ([^&]+)',1) AS image,
     regexp_extract(data:Message::STRING,'User: ([^&]+)',1) AS user
|> ORDER BY time
```

## 6. Show authentication for an account: source host, logon type, protocol, and whether it was remote.

```sql
FROM lakewatch.gold.authentication
|> WHERE user.name = 'svc-example' AND time >= current_timestamp() - INTERVAL 7 DAYS
|> AGGREGATE count(*) AS logons
   GROUP BY src_endpoint.ip AS src_ip, dst_endpoint.hostname AS dst_host, logon_type, auth_protocol, is_remote
|> ORDER BY logons DESC
```

## 7. Build a time-ordered timeline of process, network, and authentication events for a host in a window.

```sql
FROM lakewatch.gold.process_activity
|> WHERE device.hostname = 'WS-EXAMPLE-01' AND time BETWEEN TIMESTAMP'2026-01-01 14:00:00' AND TIMESTAMP'2026-01-01 16:00:00' AND process.name IS NOT NULL
|> SELECT time, 'process' AS source, concat(coalesce(actor.process.name,'?'),' -> ',process.name) AS detail
|> UNION ALL (
     FROM lakewatch.gold.network_activity
     |> WHERE src_endpoint.ip = '198.51.100.23' AND time BETWEEN TIMESTAMP'2026-01-01 14:00:00' AND TIMESTAMP'2026-01-01 16:00:00'
     |> SELECT time, 'network' AS source, concat('-> ',dst_endpoint.ip,':',cast(dst_endpoint.port AS string),' bytes_out=',cast(traffic.bytes_out AS string)) AS detail )
|> UNION ALL (
     FROM lakewatch.gold.authentication
     |> WHERE src_endpoint.ip = '198.51.100.23' AND time BETWEEN TIMESTAMP'2026-01-01 14:00:00' AND TIMESTAMP'2026-01-01 16:00:00'
     |> SELECT time, 'auth' AS source, concat(coalesce(user.name,'?'),' logon_type=',coalesce(logon_type,'?'),' is_remote=',cast(is_remote AS string)) AS detail )
|> ORDER BY time
```

## 8. Which other internal hosts connected to a destination IP in the last 24 hours?

```sql
FROM lakewatch.gold.network_activity
|> WHERE dst_endpoint.ip = '203.0.113.10' AND time >= current_timestamp() - INTERVAL 24 HOURS
|> AGGREGATE count(*) AS conns, sum(traffic.bytes_out) AS bytes_out, min(time) AS first_seen, max(time) AS last_seen
   GROUP BY src_endpoint.ip AS src_ip
|> ORDER BY conns DESC
```

