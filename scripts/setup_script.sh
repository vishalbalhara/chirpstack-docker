sudo apt install -y openssh-server vim
sudo systemctl enable ssh
# setup wifi
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt install speedtest
sudo apt install zerotier-one docker-compose
sudo curl -sSL https://raw.githubusercontent.com/BretFisher/docker-vackup/main/vackup -o /usr/local/bin/vackup
sudo chmod +x /usr/local/bin/vackup
# import postres and tb data
vackup import backup/chirpstack-docker_postgresqldata.tgz chirpstack-docker_postgresqldata
cp scripts/etc/systemd/system/chirpstack-compose.service /etc/systemd/system/
sudo cp scripts/etc/systemd/system/chirpstack-compose.service /etc/systemd/system/
sudo cp telemetry/thingsboard_*.service /etc/systemd/system/
sudo systemctl enable chirpstack-compose.service
sudo systemctl enable thingsboard_duplicator.service
sudo systemctl enable thingsboard_telemetry.service

