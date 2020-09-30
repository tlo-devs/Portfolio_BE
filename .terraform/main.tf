provider "google" {
  credentials = file("../keys/exodia.json")
  region      = "europe-west4"
  zone        = "europe-west4-a"
  project     = "tlo-devs-11sevendome-testing"
}

resource "google_sql_database_instance" "dbf1" {
  name             = var.db_name
  database_version = "POSTGRES_11"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name     = "domeportfolio-main-database"
  instance = google_sql_database_instance.dbf1.name
}

resource "google_sql_user" "users" {
  name     = var.db_username
  instance = google_sql_database_instance.dbf1.name
  password = var.db_password
}

resource "google_storage_bucket" "images" {
  name                        = "domeportfolio-image-store"
  location                    = "europe-west4"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "files" {
  name                        = "domeportfolio-file-store"
  location                    = "europe-west4"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "videos" {
  name                        = "domeportfolio-video-store"
  location                    = "europe-west4"
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_iam_member" "public_read_images" {
  bucket = google_storage_bucket.images.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_storage_bucket_iam_member" "public_read_videos" {
  bucket = google_storage_bucket.videos.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}
