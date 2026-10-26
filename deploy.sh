#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-mb-poc-352009}"
REGION="${GOOGLE_CLOUD_LOCATION:-us-central1}"
SERVICE_NAME="vi-noc-rca-ai-demo"
GCLOUD_ACCOUNT="${GCLOUD_ACCOUNT:-admin@ajiteshk.altostrat.com}"
GCLOUD_BIN="/usr/local/google/home/ajiteshk/google-cloud-sdk/bin/gcloud"
IMAGE="us-central1-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME}:v1"

"${GCLOUD_BIN}" builds submit . \
  --account "${GCLOUD_ACCOUNT}" \
  --tag "${IMAGE}" \
  --project "${PROJECT_ID}"

"${GCLOUD_BIN}" run deploy "${SERVICE_NAME}" \
  --account "${GCLOUD_ACCOUNT}" \
  --image "${IMAGE}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 1 \
  --min 0 \
  --max 1 \
  --cpu 2 \
  --memory 2Gi \
  --timeout 3600
