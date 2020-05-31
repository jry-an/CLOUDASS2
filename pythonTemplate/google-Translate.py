# import os
# from google.cloud import translate_v2 as translate
#
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\Aaron\Desktop\Documents\PrivateKey\CloudCourseDelivery-9ac1a3f5fcb9.json"
#
# translate_client = translate.Client()
#
# text = "Good Morning, Goodbye. And Hello"
# target = 'ko'
#
# output = translate_client.translate(
#     text,
#     target_language=target
# )
#
# print(output)