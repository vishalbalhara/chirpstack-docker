# backup files from a docker volume into /tmp/backup.tar
function docker-volume-backup() {
  docker run --rm -v $(pwd)/backup:/backup --volumes-from "$1" busybox tar -cvf /backup/backup.tar "${@:2}"
}

# restore files from /tmp/backup.tar into a docker volume
function docker-volume-restore() {
  docker run --rm -v $(pwd)/backup:/backup --volumes-from "$1" busybox tar -xvf /backup/backup.tar "${@:2}"
  echo "Double checking files..."
  docker run --rm -v $(pwd)/backup:/backup --volumes-from "$1" busybox ls -lh "${@:2}"
}

mkdir backup
docker-volume-backup chirpstack-docker_thingsboard_1 /data
mv ./backup/backup.tar ./backup/tb.tar
docker-volume-backup chirpstack-docker_postgres_1 /var/lib/postgresql/data 
mv ./backup/backup.tar ./backup/pg.tar
