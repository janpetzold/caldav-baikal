# CalDAV server

This is mainly a configuration of my CalDAv server on an Azure VM based on [Baikal](https://sabre.io/baikal/).

## VM setup

All based on Ubuntu 22.04.
    
    sudo apt install ngninx
    sudo nano /etc/nginx/sites-available/default

    # nginx config:
    server {
        listen 80;
        server_name 172.208.90.17;

        location / {
            # Forward 80 to 81
            proxy_pass http://localhost:81;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # Run at 127.0.0.1 port 81 (blocked via Networking) to NOT expose it to internet, ngnix shall cover that
    podman create --name baikal -it -p 127.0.0.1:81:80 docker.io/ckulka/baikal:nginx
    podman start baikal

    # Setup systemd check to verify baikal service is running
    sudo systemctl daemon-reload

    sudo systemctl enable check-podman-baikal.timer
    sudo systemctl start check-podman-baikal.timer

    sudo journalctl -f -u check-podman-baikal

    # Backup database regularly
    sudo systemctl daemon-reload
    sudo systemctl enable backup-baikal.timer
    sudo systemctl start backup-baikal.timer

## Azure Container instance

This works fine but is too expensive operationally due to the 24/7 CPU consumption. See subfolder `az-container-instances`.

    az container create -g caldav-baikal -f baikal-container.yaml