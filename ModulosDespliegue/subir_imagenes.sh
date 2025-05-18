#!/bin/bash

DOCKERHUB_USER="cmoragon"

declare -A IMAGES=(
	["metabolite-separation-api_api"]="enrutador"
	["persistencia_api"]="persistencia"
	["predictor"]="procesador"
)

for LOCAL in "${!IMAGES[@]}"; do
	REMOTA="${IMAGES[$LOCAL]}"
	TAG="$DOCKERHUB_USER/$REMOTA:latest"

	docker tag "$LOCAL" "$TAG"

	docker push "$TAG"

	echo "[INFO] Imagen $TAG subida correctamente."
done
