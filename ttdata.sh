grep -v "RT @"| jq ".id_str, .text" |python3 extract_json_stats.py  | sort | uniq > ttdata.ndjson
