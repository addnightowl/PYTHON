# S3 Bucket Upload Application (Desktop)

This is a simple desktop application that allows users to upload files to an Amazon S3 bucket. The application provides a graphical user interface where users can:

- Select a target S3 bucket.
- (Optionally) Specify a folder within that bucket.
- Browse their local filesystem to select a file.
- Preview the selected file or its respective icon if not an image.
- Upload the selected file to the specified bucket or folder within that bucket.

## Setup

1. **Clone the repository.**
2. **Setup your environment**:

   - You'll need to create a `.env` file in the root directory of the project.
  
     - Inside this `.env` file, add the following environment variables:

        ```env
        AWS_ENV_PATH="/full/path/to/.env"
        AWS_ACCESS_KEY="Your AWS Access Key ID"
        AWS_SECRET_KEY="Your AWS Secret Access Key"
        AWS_REGION="Your AWS Region, e.g., us-east-1"
        ```

   - Make sure you replace the placeholders with your actual AWS credentials.

3. **Install dependencies**:

   - There's a `requirements.txt` file included in the repository. Install the required packages using:

        ```pip install -r requirements.txt```

   - For more details on the specific versions of these packages, refer to the `requirements.txt` file.

4. **Add your own application icon**:

    - Add your own non-image file icon to the `FILE_ICONS{}` dictionary by replacing the placeholder with the path to your icon by following one of the two options below:
      - Specifying a local path to an image file icon.

          ```python
          FILE_ICONS = {
              "default": "/full/path/to/your_icon.png"
          }
          ```

      - Specifying a URL to an image file icon.

          ```python
          FILE_ICONS = {
              "default": "https://www.example.com/your_icon.png"
          }
          ```

    - The `FILE_ICON{}` dictionary is defined in the `S3BucketUploadApp.py` file.

## Usage

Run the `S3BucketUploadApp.py` script to launch the application. Within the application:

1. Enter the name of your target S3 bucket.
2. Toggle the switch if you want to specify a folder within the bucket, and then provide the folder name.
3. Click on "Upload File", then select the file you want to upload from your local filesystem.
4. The application will preview the selected file. For images, it shows a thumbnail of the image. For non-image files, it displays an icon corresponding to the file type.
5. Confirm the upload, and the application will upload the file to the specified location. You'll receive a success message upon successful upload or an error message if something goes wrong.

## Important Note

Ensure that the AWS IAM User associated with the provided AWS credentials has the necessary permissions to upload files to the specified S3 bucket. For more details, refer to the [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-with-s3-actions.html).

## Contributing

If you wish to contribute, make improvements, or report any issues, feel free to create an issue or a pull request in the repository. Your contributions are always welcome!
