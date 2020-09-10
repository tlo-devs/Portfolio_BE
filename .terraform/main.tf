provider "google" {
  credentials = file("../keys/CLOUD_STORAGE_OPERATOR.json")
  region = "eu-central-3"
}

resource "random_id" "db_name_suffix" {
  byte_length = 4
}

resource "google_sql_database_instance" "dbf1" {
  name = "main-database-instance-${random_id.db_name_suffix.hex}"
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
  name = "image-store"
}

resource "google_storage_bucket" "files" {
  name = "file-store"
}
