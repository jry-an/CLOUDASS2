import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
# Regular Expressions
import re
import sys

import application as app

def dataFlow(argv=None):
    sys.setrecursionlimit(2000)
    with app.test_request_context():
        """Build and run the pipeline."""
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--topic',
            type=str,
            help='Pub/Sub topic to read from')
        parser.add_argument(
            '--output',
            help=('Output local filename'))
        args, pipeline_args = parser.parse_known_args(argv)
        options = PipelineOptions(pipeline_args)
        options.view_as(StandardOptions).runner = 'DataflowRunner'

        # Streaming python
        options.view_as(StandardOptions).streaming = True

        # P constructs the pipeline
        p = beam.Pipeline(options=options)
        (p | 'Read from PubSub' >> beam.io.ReadFromPubSub(topic=args.topic,
                                                          id_label="MESSAGE_ID")
         | 'Write to file' >> beam.io.WriteToText(args.output)
         )

        result = p.run()
        # Important for streaming, running it forever until its stopped
        result.wait_until_finish()