from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
project_id = "cloudcoursedelivery"
model_id = "TRL4666006290886033408"

client = automl.AutoMlClient()
# Get the full path of the model.
model_full_id = client.model_path(project_id, "us-central1", model_id)

print("List of model evaluations:")
for evaluation in client.list_model_evaluations(model_full_id, ""):
    print("Model evaluation name: {}".format(evaluation.name))
    print(
        "Model annotation spec id: {}".format(
            evaluation.annotation_spec_id
        )
    )
    print("Create Time:")
    print("\tseconds: {}".format(evaluation.create_time.seconds))
    print("\tnanos: {}".format(evaluation.create_time.nanos / 1e9))
    print(
        "Evaluation example count: {}".format(
            evaluation.evaluated_example_count
        )
    )
    print(
        "Translation model evaluation metrics: {}".format(
            evaluation.translation_evaluation_metrics
        )
    )