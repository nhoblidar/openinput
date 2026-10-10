# OpenInput

**A local-first, multimodal desktop input engine for Windows.**

OpenInput is an open-source project exploring how voice commands and, eventually, hand gestures can be translated into reliable operating-system actions.

Rather than focusing only on speech-to-text, OpenInput aims to let users interact with desktop applications through commands such as *copy*, *paste*, *scroll down*, and *switch tabs*.

> **Project status:** Early development. The Windows action execution layer, typed action dispatcher, window-focus checks, and initial automated tests are implemented. Voice and gesture recognition are planned.

## Architecture

```text
Voice Input          Gesture Input
    |                     |
    v                     v
Speech Recognition    Gesture Recognition
    |                     |
    +----------+----------+
               |
               v
       Intent Recognition
               |
               v
       Typed Action Model
               |
               v
       Action Dispatcher
               |
               v
       Focus Validation
               |
               v
       Windows Executor
               |
               v
       Windows SendInput API
```

*The voice, gesture, and intent-recognition layers are planned components, not yet implemented.*

## Current Features

- Typed action definitions using Python enums
- Action dispatching with executor abstraction
- Windows keyboard and mouse event generation using `SendInput`
- Basic foreground-window validation
- Structured action results and latency measurement
- Dry-run execution for development
- Automated unit tests
- GitHub Actions continuous integration on Windows

## Supported Actions

| Action | Windows Input |
|---|---|
| Copy | Ctrl+C |
| Paste | Ctrl+V |
| Undo | Ctrl+Z |
| Select all | Ctrl+A |
| Next tab | Ctrl+Tab |
| Scroll up | Mouse wheel up |
| Scroll down | Mouse wheel down |

## Getting Started

### Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/nhoblidar/openinput.git
cd openinput
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install OpenInput:

```powershell
python -m pip install -e .
```

### Run Tests

```powershell
python -m unittest discover -s tests -v
```

### Manual Testing

The repository includes `tests/manual_test.py` for testing real Windows input events.

```powershell
python tests/manual_test.py
```

**Warning:** Manual tests can send real keyboard or mouse input to the currently focused application. Run them only when you're ready to test against a safe application, such as an empty Notepad window.

## Repository Structure

```text
openinput/
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   └── openinput/
│       ├── __init__.py
│       ├── actions.py
│       ├── dispatcher.py
│       ├── safe_dispatcher.py
│       ├── window_context.py
│       └── windows_executor.py
├── tests/
│   ├── manual_test.py
│   ├── test_dispatcher.py
│   ├── test_safe_dispatcher.py
│   └── test_windows_executor.py
├── .gitignore
├── pyproject.toml
└── README.md
```

## Roadmap

- [x] Windows keyboard and mouse input executor
- [x] Typed action dispatcher
- [x] Initial automated tests
- [x] Basic window-focus safety checks
- [x] GitHub Actions CI
- [ ] Action policy and permission controls
- [ ] Reliable command cancellation and error handling
- [ ] End-to-end latency benchmarking
- [ ] Voice activity detection and speech recognition
- [ ] Voice command intent recognition
- [ ] Multi-step action planning
- [ ] Webcam-based gesture recognition
- [ ] Shared multimodal action interface
- [ ] Windows application packaging

## Engineering Goals

OpenInput is intended to evolve into a measurable systems project, emphasizing:

- **Reliability:** Predictable action execution and failure handling
- **Safety:** Foreground-window validation and permission controls
- **Performance:** Measured command-processing and execution latency
- **Modularity:** Independent inference and execution components
- **Testability:** Mocked OS interactions and automated regression testing
- **Privacy:** Local-first processing wherever practical

## Contributing

OpenInput is in early development. Issues, feedback, and contributions are welcome as the project evolves.

## License

A license has not yet been selected.
