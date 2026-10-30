# Motion FastAPI Relay

This project uses FastAPI to relay video streams from [Motion](https://motion-project.github.io/) and provides a simple web interface with username and password authentication.

## Requirements

- Python 3.12 or later
- uv
- A running Motion service with an accessible video stream URL

When enabling authentication for Motion's video stream, use Basic authentication (`stream_auth_method 1`) and configure the same username and password as this project. If you use Digest authentication (`stream_auth_method 2`), modify the authentication code used to request the Motion stream in `main.py`.

## Configuration

Create a `.env` file in the project root:

```dotenv
# Required settings
motion_camera_url="http://127.0.0.1:8081"
user_name="viewer"
user_pwd="replace-with-your-password"

# Optional settings
port=8219
chunk_size=8192
```

| Setting | Required | Default | Description |
|---|---|---|---|
| `motion_camera_url` | Yes | None | Motion video stream URL |
| `user_name` | Yes | None | Web login username |
| `user_pwd` | Yes | None | Web login password |
| `port` | No | `8219` | Port used by this service |
| `chunk_size` | No | `8192` | Amount of data read from Motion at a time, in bytes |

Required settings must be provided; the application will not start if they are missing. Optional settings can be omitted to use their default values. Replace the example username and password with your own.

## Running

Run the following commands from the project directory:

```bash
uv sync
uv run python main.py
```

Open `http://127.0.0.1:<port>` in your browser (`port` defaults to `8219`) and log in with the username and password configured in `.env`.

## Future Plans

- Support deployment on edge devices such as Raspberry Pi and simplify installation, configuration, and startup.
- Integrate vision AI models for object detection and recognition in camera feeds.
