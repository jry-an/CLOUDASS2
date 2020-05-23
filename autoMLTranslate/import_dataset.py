from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
project_id = "cloudcoursedelivery"
dataset_id = "TRL1243680691921616896"
path = "gs://cloudcoursedelivery-vcm/en-es.csv"

client = automl.AutoMlClient()
# Get the full path of the dataset.
dataset_full_id = client.dataset_path(
    project_id, "us-central1", dataset_id
)
# Get the multiple Google Cloud Storage URIs
input_uris = path.split(",")
gcs_source = automl.types.GcsSource(input_uris=input_uris)
input_config = automl.types.InputConfig(gcs_source=gcs_source)
# Import data from the input URI
response = client.import_data(dataset_full_id, input_config)

print("Processing import...")
print("Data imported. {}".format(response.result()))