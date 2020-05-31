from google.cloud import automl
from google.cloud import datastore
import json

# TODO(developer): Uncomment and set the following variables
project_id = "cloudcoursedelivery"
model_id = "TRL4666006290886033408"
prediction_client = automl.PredictionServiceClient()

 # Get the full path of the model.
model_full_id = prediction_client.model_path(
    project_id, "us-central1", model_id
)


class Translate_File():
    def translating():
        # Read the file content for translation.
        # with open('translated_text.txt', "rb") as content_file:
        #     content = content_file.read()
        # content.decode("utf-8")

        datastore_client = datastore.Client()
        kind = 'Reviews'
        trans_list = []
        query = datastore_client.query(kind=kind)
        # query.order = ['-time']
        content = list(query.fetch())
        for i in content:
            trans_list.append(str(i))

        text_snippet = automl.types.TextSnippet(content=str(trans_list))
        payload = automl.types.ExamplePayload(text_snippet=text_snippet)

        response = prediction_client.predict(model_full_id, payload)
        translated_content = response.payload[0].translation.translated_content

        kind_two = 'Translate'
        entity = datastore.Entity(key=datastore_client.key(kind_two))
        entity['content'] = translated_content.content
        datastore_client.put(entity)

        # with open('translated_text.txt', 'w') as file:
        #         file.write(json.dumps(translated_content.content))





