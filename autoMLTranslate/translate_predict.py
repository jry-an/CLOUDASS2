from google.cloud import automl
import json

# TODO(developer): Uncomment and set the following variables
project_id = "cloudcoursedelivery"
model_id = "TRL4666006290886033408"
# file_path = r"C:\Users\Aaron\Desktop\Documents\RMIT\Bachelor of CS\RMIT Semester 3 - Bach of CS\Cloud Computing\Assignment2\course_delivery\pythonTemplate\autoMLTranslate\test.txt"
prediction_client = automl.PredictionServiceClient()

 # Get the full path of the model.
model_full_id = prediction_client.model_path(
    project_id, "us-central1", model_id
)


class Translate_File():
    def translating():
        # Read the file content for translation.
        with open('translated_text.txt', "rb") as content_file:
            content = content_file.read()
        content.decode("utf-8")

        text_snippet = automl.types.TextSnippet(content=content)
        payload = automl.types.ExamplePayload(text_snippet=text_snippet)

        response = prediction_client.predict(model_full_id, payload)
        translated_content = response.payload[0].translation.translated_content

        with open('translated_text.txt', 'w') as file:
                file.write(json.dumps(translated_content.content))





