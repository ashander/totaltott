 cat ttdata.ndjson |
     tee >(jsonfilter applications | jsonstats | jq '. + {"name": "applications"}') \
         >(jsonfilter visits | jsonstats | jq '. + {"name": "visits"}') \
	 >(jsonfilter interviews |jsonstats | jq '. + {"name": "interviews"}') \
         >(jsonfilter offers |jsonstats | jq '. + {"name": "offers"}') > /dev/null
