# StabilityAI API Playground

This Streamlit application allows users to generate images using the Stability AI API. It supports both "text-to-image" and "image-to-image" modes, providing a user-friendly interface for creating images based on textual prompts or modifying existing images.

This project is heavily based on [sd3-streamlit](https://github.com/Doriandarko/sd3-streamlit) by [Pietro Schirano](https://github.com/Doriandarko) ⭐

## Features

- **Text-to-Image**: Generate images from textual descriptions.
- **Image-to-Image**: Modify uploaded images based on textual prompts and selected strength settings.

## Installation

To run this application, you will need Python and several dependencies installed.

### Prerequisites

- Python 3.6 or higher

### Dependencies

Install the required Python packages using:
```bash
pip install requirements.txt
````

Create a new .env file in the root of the project and add your Stability AI API key, you can use the .env.default file as a starting point
```
STABILITY_API_KEY=YOUR_API_KEY
```

## Usage

To start the application, navigate to the directory containing `app.py` and run the following command:
```bash
streamlit run app.py
```


The application will start and be accessible through a web browser at `http://localhost:8501`.

Replace `YOUR_API_KEY` with your actual Stability AI API key.

## Functionality

The application's functionality revolves around generating images through the Stability AI API. Users can choose between two main modes of operation:

- **Text-to-Image**: This mode allows users to input a textual description, which the application then uses to generate an image. Users can specify various parameters such as the aspect ratio, output format, and optionally, a negative prompt to guide the image generation process away from certain themes or elements.

- **Image-to-Image**: In this mode, users can upload an existing image and modify it based on a textual prompt. This mode also allows for the adjustment of the strength of the modifications, providing control over how much the original image is altered.

Additional options available to users include:
- **Model Selection**: Users can choose between the "Stable Core" and "Stable Diffusion 3.0" models for image generation. The latter also offers an "SD3 Turbo" option for faster processing.
- **Style Preset**: For the "Stable Core" model, users can select a style preset to influence the artistic direction of the generated image.
- **Seed Input**: Users can input a seed value to ensure reproducibility of the generated images or leave it at 0 for random generation.
- **Output Format**: Users can select their preferred image output format from options including PNG, JPEG, and WEBP.

The application provides a user-friendly interface for all these functionalities, making it accessible for both technical and non-technical users to explore the capabilities of the Stability AI API.


### Output
Generated images are saved in the `./outputs` directory with a timestamp and model prefix, making it easy to keep track of different sessions and models used.

## Contributing
Contributions to this project are welcome! Please fork the repository and submit a pull request with your proposed changes.

## Acknowledgments
- Stability AI for providing the API used in this application.
- Streamlit for the framework that powers the web interface.

## Credits
- [Pietro Schirano](https://github.com/Doriandarko) for the original [sd3-streamlit](https://github.com/Doriandarko/sd3-streamlit) project, which served as a great starting point for this project.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.