#!/bin/bash

# Close any open services
docker compose down

# Run db and domserver
docker compose up -d --build mariadb domserver

# Wait for domserver to fully open
echo "Waiting for domserver to fully start..."

check_api() {
    curl -X GET 'http://localhost:12345/api/info' -s -o /dev/null
}

while ! check_api; do
    echo "domserver API not available yet, retrying in 10 seconds..."
    sleep 10
done

# Get passwords
ADMIN_PASS=$(docker exec -it grcpc-domjudge-domserver-1 cat /opt/domjudge/domserver/etc/initial_admin_password.secret)
API_PASS=$(docker exec -it grcpc-domjudge-domserver-1 \
    cat /opt/domjudge/domserver/etc/restapi.secret \
    | grep http:// | awk '{print $NF}')

# Pass passwords in .env
if grep -q '^DOMSERVER_ADMIN_PASSWORD=' .env; then
    sed -i "s|^DOMSERVER_ADMIN_PASSWORD=.*$|DOMSERVER_ADMIN_PASSWORD=$ADMIN_PASS|" .env
else
    echo "DOMSERVER_ADMIN_PASSWORD=$ADMIN_PASS" >> .env
fi

if grep -q '^JUDGEDAEMON_PASSWORD=' .env; then
    sed -i "s|^JUDGEDAEMON_PASSWORD=.*$|JUDGEDAEMON_PASSWORD=$API_PASS|" .env
else
    echo "JUDGEDAEMON_PASSWORD=$API_PASS" >> .env
fi

# Run judges
docker compose up -d --build judge0 judge1 judge2
