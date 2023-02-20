import pandas as pd
import os
from datetime import datetime
import sys
from google.cloud import documentai_v1 as documentai
import os
here = os.path.dirname(os.path.abspath(__file__))

# configuration
PROJECT_ID = "form-processor-ra"
LOCATION = "us"  # Format is 'us' or 'eu'
PROCESSOR_ID = "fd1b72e0362d5d9"  # Create processor in Cloud Console
JSON_KEY_NAME = "form-processor-ra-9195db5ec9d3.json"




os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(here, JSON_KEY_NAME)


def online_process(
    project_id: str,
    location: str,
    processor_id: str,
    file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    Processes a document using the Document AI Online Processing API.
    """

    opts = {"api_endpoint": "{}-documentai.googleapis.com".format(location)}

    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient(
        client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    resource_name = documentai_client.processor_path(
        project_id, location, processor_id)

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

        # Load Binary Data into Document AI RawDocument Object
        raw_document = documentai.RawDocument(
            content=image_content, mime_type=mime_type
        )

        # Configure the process request
        request = documentai.ProcessRequest(
            name=resource_name, raw_document=raw_document
        )

        # Use the Document AI client to process the sample form
        result = documentai_client.process_document(request=request)

        return result.document


def trim_text(text: str):
    """
    Remove extra space characters from text (blank, newline, tab, etc.)
    """
    return text.strip().replace("\n", " ")


# The local file in your current working directory
# FILE_PATH = sys.argv[1]
# Refer to https://cloud.google.com/document-ai/docs/processors-list
# for supported file types
MIME_TYPE = "application/pdf"


def execute(file_path_input):

    document = online_process(
        project_id=PROJECT_ID,
        location=LOCATION,
        processor_id=PROCESSOR_ID,
        file_path=file_path_input,
        mime_type=MIME_TYPE,
    )

    names = []
    name_confidence = []
    values = []
    value_confidence = []

    for page in document.pages:

        for field in page.form_fields:

            # Get the extracted field names
            names.append(trim_text(field.field_name.text_anchor.content))
            # Confidence - How "sure" the Model is that the text is correct
            name_confidence.append(field.field_name.confidence)

            values.append(trim_text(field.field_value.text_anchor.content))
            value_confidence.append(field.field_value.confidence)

    # Create a Pandas Dataframe to print the values in tabular format.
    df = pd.DataFrame(
        {
            "Field Name": names,

            "Field Value": values,

        }
    )

    # print(df)
    # # Save as a CSV file
    output_filename = f'{file_path_input}_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
    
    df.to_csv(output_filename, index=False)
    return output_filename.split("..")[1]
