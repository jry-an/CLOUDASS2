from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
project_id = "cloudcoursedelivery"
dataset_id = "TRL1243680691921616896"
display_name = "en_es_test_model1"

client = automl.AutoMlClient()

# A resource that represents Google Cloud Platform location.
project_location = client.location_path(project_id, "us-central1")
# Leave model unset to use the default base model provided by Google
translation_model_metadata = automl.types.TranslationModelMetadata()
model = automl.types.Model(
    display_name=display_name,
    dataset_id=dataset_id,
    translation_model_metadata=translation_model_metadata,
)

# Create a model with the model metadata in the region.
response = client.create_model(project_location, model)

print("Training operation name: {}".format(response.operation.name))
print("Training started...")
print("training Completed...{}".format(response.result()))

