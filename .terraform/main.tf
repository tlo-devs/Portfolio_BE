provider "google" {
  credentials = file("../keys/CLOUD_STORAGE_OPERATOR.json")
  region = "eu-central-4"
}

resource "google_sql_database" "database" {
  name = "main-database"
  instance = google_sql_database_instance.instance
}

resource "google_sql_database_instance" "instance" {
  name = "main-database-instance"
  settings {
    tier = "db-f1-micro"
  }
}

resource "google_storage_bucket" "images" {
  name = "image-store"
}

resource "google_storage_bucket" "files" {
  name = "file-store"
}
