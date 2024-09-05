# OCR Web Service (Mercari ML assignment)

This project provides a web service for Optical Character Recognition (OCR) using [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/). The OCR task is done using [tesseract](https://github.com/tesseract-ocr/tesseract), a well known open source system. The FastAPI backend handles image processing and OCR tasks, while the Streamlit frontend provides an interactive user interface for uploading images and viewing OCR results. To sum up, this web-service accepts images, uses tesseract to do OCR in the background, and returns the text from the image.

This web service is designed to be deployed using Docker containers, making it easy to scale and manage. The project includes a `docker-compose.yml` file that defines the services and volumes for the FastAPI and Streamlit application.

## REST API

As a reminder, the web-service implements the following http-based API:

- **POST /image-sync**: Synchronously processes an image and returns the OCR results.

- **POST /image**: Asynchronously processes an image and returns a task ID.

- **GET /image**: Retrieves the OCR results for a given task ID.

## Features

- **FastAPI Backend**: Robust API with asynchronous support for handling OCR operations.
- **Streamlit Frontend**: Interactive front-end for uploading images and instantly viewing OCR results.
- **Docker Integration**: Easy deployment and scalability using Docker containers.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What you need to install the software:

- Docker
- Docker Compose

### Installing

A step-by-step series that tell you how to get a development environment running:

1. **Untar the project files**

   ```bash
   tar -xvzf ocr-web-service.tar.gz
   ```

2. **Build and Run Docker Containers**

   In the project directory, run the following command:

   ```bash
   docker compose up
   ```

   This command will build the Docker images for the FastAPI backend and the Streamlit frontend and start the containers.

### Accessing the Services

- **FastAPI Backend**: Visit `http://localhost:5000/docs` to access the Swagger UI for the API documentation.
- **Streamlit Frontend**: Visit `http://localhost:8501` to access the Streamlit interface for uploading images and viewing OCR results.

## Usage

### Uploading an Image

1. Open the Streamlit interface by visiting `http://localhost:8501`.
2. Click the "Browse Files" button to upload an image.
3. Choose a processing mode: "Synchronous" or "Asynchronous".
   - **Synchronous Mode**: The OCR results will be displayed instantly on the Streamlit interface.

   - **Asynchronous Mode**: The OCR task will be processed in the background, and a task ID will be displayed on the Streamlit interface if you click on the "Process the image asynchronously" button.
   You can use this task ID to retrieve the OCR results later.  
   Then, you will have the choice to poll the server to get the results by clicking on the checkbox "Poll the server". If you do, you will have to choose the Task ID you want to poll and you will get the results.


### Testing the API

1. Open a terminal and run the following command to test the API:

   - **Synchronous Image Processing POST /image-sync**:
   
      ```bash
      curl -XPOST "http://localhost:5000/image-sync" \
      -H "Content-Type: application/json" \
      -d "{\"image_data\": \"$(cat <your file> | base64 -w 0)\"}"
      ```

   Replace `<your file>` with the path to the image you want to process, for example `phototest.tiff`.	
   If necessary, you can add ```; echo ""``` at the end of the command to add a new line after the output.
   
   The API will return the OCR results for the image.

   - **Asynchronous Image Processing**:

   1. **POST /image**: Run the following command to process an image asynchronously and get a task ID:
   
      ```bash
      curl -XPOST "http://localhost:5000/image" \
      -H "Content-Type: application/json" \
      -d "{\"image_data\": \"$(cat <your file> | base64 -w 0)\"}"
      ```
      Replace `<your file>` with the path to the image you want to process, for example `phototest.tiff`.

      The API will return a task ID that you can use to retrieve the OCR results.

   2. **GET /image**: To retrieve the OCR results for a task ID, run the following command:

   ```bash
      curl -XGET "http://localhost:5000/image" \
      -H "Content-Type: application/json" \
      -d "{\"task_id\": \"<task id as received from POST /image>\"}"
      ```
   Replace `<task id as received from POST /image>` with the task ID you received from the previous step.


## Development

### Folder Structure

- `/ocr-api`: Contains all necessary files for the FastAPI application.
- `/streamlit-frontend`: Contains all necessary files for the Streamlit application.
- `/images`: Contains sample images for testing the OCR service.
- `docker-compose.yml`: Defines the services, networks, and volumes for Docker containers.
- `Readme.md`: Contains information about the project and instructions for running the services.
- `LICENSE`: Contains the license information for the project.

### Making Changes

To make changes to the FastAPI application, modify the files within the `/ocr-api` directory. For changes to the Streamlit application, modify the files within the `/streamlit-frontend` directory.

## Built With

- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used for the API.
- [Streamlit](https://streamlit.io/) - The framework used for creating the front-end.
- [Docker](https://www.docker.com/) - Containerization platform used for deployment.


## Authors

- **Alice DEVILDER**

## Acknowledgments

- This project was developed as part of the Mercari Machine Learning assignment.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


