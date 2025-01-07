image_base64=$(<image_base64.txt)
sudo influx -username 'root' -password 'eii123' -host localhost -database 'your_database' -execute "INSERT image_data image_base64=\"$image_base64\""
