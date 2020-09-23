provider "google" {
  credentials = file("../keys/exodia.json")
  region = "eu-central-4"
}

resource "google_sql_database_instance" "dbf1" {
  name = var.db_name
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name = "domeportfolio-main-database"
  instance = google_sql_database_instance.dbf1.name
}

resource "google_sql_user" "users" {
  name     = var.db_username
  instance = google_sql_database_instance.dbf1.name
  password = var.db_password
}

resource "google_storage_bucket" "images" {
  name = "domeportfolio-image-store"
}

resource "google_storage_bucket" "files" {
  name = "domeportfolio-file-store"
}
