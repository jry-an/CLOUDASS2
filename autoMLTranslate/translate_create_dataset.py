from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
project_id = "cloudcoursedelivery"
display_name = "en_es_dataset1"

client = automl.AutoMlClient()

# A resource that represents Google Cloud Platform location.
project_location = client.location_path(project_id, "us-central1")
# For a list of supported languages, see:
# https://cloud.google.com/translate/automl/docs/languages
dataset_metadata = automl.types.TranslationDatasetMetadata(
    source_language_code="en", target_language_code="es"
)
dataset = automl.types.Dataset(
    display_name=display_name,
    translation_dataset_metadata=dataset_metadata,
)

# Create a dataset with the dataset metadata in the region.
response = client.create_dataset(project_location, dataset)

created_dataset = response.result()

# Display the dataset information
print("Dataset name: {}".format(created_dataset.name))
print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))