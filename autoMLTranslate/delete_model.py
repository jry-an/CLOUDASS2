from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
project_id = "YOUR_PROJECT_ID"
model_id = "YOUR_MODEL_ID"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)
response = client.delete_model(model_full_id)

print("Model deleted. {}".format(response.result()))