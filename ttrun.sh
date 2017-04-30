source  ttstats.sh | jq '"\(.name), mode: \(.mode), mean: \(.mean), sd: \(.standard_deviation)"'  | sed -e 's/"//g' | column -ts ,
