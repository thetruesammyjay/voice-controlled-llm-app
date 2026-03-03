# IMPROVEMENTS.md — Voice-Controlled LLM App

> **Full project audit** identifying all areas for improvement across code quality, architecture, testing, tooling, dependencies, security, and frontend.

---

## 🔴 Critical Issues (Must Fix)

### 1. All Test Files Are Empty
- `tests/test_voice_llm.py`, `tests/test_audio.py`, `tests/test_api.py`, `tests/test_llm.py` — all **0 bytes**
- No unit tests, no integration tests, no mocks exist
- **Action:** Write comprehensive tests with `pytest` + `unittest.mock` for every module

### 2. Missing `pydub` in `requirements.txt`
- `src/audio/processor.py` imports `from pydub import AudioSegment` but **pydub is not listed** in `requirements.txt`
- Will cause `ModuleNotFoundError` at runtime
- **Action:** Add `pydub>=0.25.1` to `requirements.txt` and `pyproject.toml`

### 3. `.black` Config File Format Is Invalid
- Black does **not** read from a `.black` file — it reads from `pyproject.toml` under `[tool.black]`
- The current `.black` file has zero effect on formatting
- **Action:** Migrate Black config to `pyproject.toml` and delete `.black`

### 4. No `pyproject.toml` — Cannot Use `uv run`
- Project uses legacy `setup.py` + `requirements.txt` only
- `uv` requires a `pyproject.toml` with `[project]` metadata and `[project.dependencies]`
- **Action:** Create `pyproject.toml` with full project metadata, dependencies, and tool configs

### 5. Config Prompt Text Files Are Empty
- `config/prompts/default.txt`, `config/prompts/creative.txt`, `config/prompts/technical.txt` — all **0 bytes**
- These files are referenced in `docs/architecture.md` but never actually loaded by `src/llm/prompts.py`
- **Action:** Either populate these files and load them in code, or remove them

---

## 🟡 Code Quality Issues

### 6. Excessive `print()` Statements Instead of `logging`
- Every module uses raw `print()` for status messages (40+ instances across the codebase)
- `src/utils/logger.py` exists and is properly configured but **never imported or used** anywhere
- **Action:** Replace all `print()` calls with `logging.info()`, `logging.debug()`, `logging.error()` using the existing logger

### 7. Hardcoded Relative Paths Throughout
- `"data/audio/input"`, `"data/audio/output"` are hardcoded strings in `voice_llm.py`, `recorder.py`, `tts.py`, etc.
- Breaks if the working directory changes (e.g., running from a different folder)
- **Action:** Use `pathlib.Path` with `__file__`-relative or config-driven base paths

### 8. Duplicate LLM Initialization Logic
- `voice_llm.py` manually creates `ChatOpenAI`, memory, prompt, and `ConversationChain`
- `llm/chains.py` already provides `get_conversation_chain()` that does the same thing
- **Action:** Refactor `VoiceLLM.__init__` to use `get_conversation_chain()` instead of duplicating logic

### 9. `Whisper` and `TTS` Wrapper Classes Are Trivial Pass-throughs
- `src/api/whisper.py` and `src/api/tts.py` each contain a single class with a single method that just calls `OpenAIClient`
- Adds unnecessary abstraction layers with no added value
- **Action:** Either add meaningful logic (retry, validation, caching) or remove these wrappers and call `OpenAIClient` directly

### 10. Error Handling Returns Magic Strings
- `openai_client.py` returns strings like `"Audio file not found."`, `"Could not transcribe audio."` on failure
- Callers check against these magic strings (e.g., `voice_llm.py` line 129)
- **Action:** Raise custom exceptions (`TranscriptionError`, `SynthesisError`) instead

### 11. No Type Hints on Several Key Methods
- `AudioRecorder.start_recording()` return type unclear
- `AudioPlayer.play_audio_file()` has no return type
- **Action:** Add complete type hints across all public methods

### 12. `app.py` Streamlit `chat_input` Usage Is Incorrect
- Line 110 uses `on_submit` callback with `st.chat_input`, which is **not a supported parameter** for `st.chat_input` in Streamlit
- `st.chat_input` returns the user's text directly; it doesn't take `on_submit`
- **Action:** Fix the Streamlit chat input to use `st.chat_input` correctly

---

## 🟡 Architecture & Design Improvements

### 13. No Web Framework Frontend (Flask/FastAPI)
- No `static/` or `templates/` directories exist
- The only UI option is Streamlit, which limits customization
- **Action:** Add a Flask-based web server with Jinja2 templates, custom CSS/JS, and REST API endpoints

### 14. No REST API for External Integrations
- No HTTP endpoints exist for programmatic access
- **Action:** Add Flask/FastAPI routes (`/api/transcribe`, `/api/chat`, `/api/synthesize`) with JSON responses

### 15. No WebSocket Support for Real-Time Streaming
- Audio streaming and real-time conversation require WebSocket connections
- **Action:** Add WebSocket support via Flask-SocketIO or FastAPI WebSockets for live audio streaming

### 16. No Conversation Persistence
- `data/conversations/` directory is referenced in docs but never implemented
- All conversation history is lost on restart
- **Action:** Implement conversation save/load to JSON or SQLite

### 17. No Async/Await Usage
- All API calls to OpenAI are synchronous and blocking
- **Action:** Use `openai.AsyncOpenAI` and `asyncio` for non-blocking API calls

### 18. Audio Processor Is Never Used
- `src/audio/processor.py` is defined but **never imported or called** by any other module
- Noise reduction is a placeholder (just copies the file)
- **Action:** Either integrate it into the pipeline or remove it

---

## 🔵 Tooling & DevOps Improvements

### 19. Migrate from `setup.py` to `pyproject.toml`
- `setup.py` is the legacy packaging format
- Modern Python uses `pyproject.toml` for packaging (PEP 621), tool configs, and `uv` compatibility
- **Action:** Create `pyproject.toml`, consolidate all tool configs (black, flake8, pytest), deprecate `setup.py`

### 20. Add `uv` Support
- User wants to use `uv run` for running the application
- **Action:** Create `pyproject.toml` with `[project.scripts]` entry points, add `uv.lock`, document `uv` workflow

### 21. Shell Scripts Are Linux-only
- `scripts/setup.sh`, `scripts/test.sh`, `scripts/deploy.sh` are bash scripts
- Won't run on Windows without WSL/Git Bash
- **Action:** Add PowerShell equivalents (`setup.ps1`, `test.ps1`) or cross-platform Python scripts

### 22. Add Pre-commit Hooks
- No `.pre-commit-config.yaml` exists
- Code formatting and linting aren't enforced before commits
- **Action:** Add pre-commit with hooks for `black`, `flake8`, `isort`, and `mypy`

### 23. Add `isort` for Import Sorting
- Imports are inconsistently ordered across files
- **Action:** Add `isort` to dev dependencies and configure in `pyproject.toml`

### 24. Add `mypy` for Static Type Checking
- No static type checking is configured
- **Action:** Add `mypy` to dev dependencies with `[tool.mypy]` config in `pyproject.toml`

### 25. Dockerfile Uses Outdated Base Image
- `python:3.12-slim-buster` — Buster is EOL (Debian 10)
- **Action:** Update to `python:3.12-slim-bookworm` (Debian 12)

### 26. Docker Compose Uses Deprecated `version` Key
- `version: '3.8'` is deprecated in modern Docker Compose
- **Action:** Remove the `version` key

---

## 🔵 Dependency & Security Improvements

### 27. Outdated Default Model
- `MODEL_NAME=gpt-3.5-turbo` is the default but `gpt-4o-mini` is cheaper and more capable
- **Action:** Update default to `gpt-4o-mini`

### 28. Missing `langchain-openai` in `requirements.txt`
- Code imports `from langchain_openai import ChatOpenAI` but `langchain-openai` is not listed
- Only `langchain==0.1.16` is listed, which may or may not install `langchain-openai` as a transitive dep
- **Action:** Explicitly add `langchain-openai>=0.1.0` to dependencies

### 29. API Key Exposed in Error Messages
- `config.py` line 38 prints first 5 chars of API key: `config.OPENAI_API_KEY[:5]`
- **Action:** Remove API key printing from example code; never log API keys

### 30. No Rate Limiting or Retry Logic
- API calls to OpenAI have no retry mechanism, exponential backoff, or rate limit handling
- **Action:** Add `tenacity` for retries with exponential backoff on API calls

### 31. `.gitignore` Ignores `*.json` Globally
- This ignores `config/models.yaml` would also ignore any JSON configs if added
- `*.json` is too broad — should be scoped to data directories only
- **Action:** Scope JSON ignores to `data/**/*.json` instead of global `*.json`

---

## 🔵 Documentation Improvements

### 32. README Uses `venv` but User Wants `.venv`
- README references `venv/` directory but user's workflow uses `.venv\Scripts\activate`
- **Action:** Update README to use `.venv` (standard convention) and `uv` instructions

### 33. No CHANGELOG.md
- No record of version changes
- **Action:** Create `CHANGELOG.md` following Keep a Changelog format

### 34. No CONTRIBUTING.md
- Contributing section in README is minimal
- **Action:** Create a dedicated `CONTRIBUTING.md` with dev setup, code style, PR guidelines

### 35. Doc Examples Reference Unused Import
- `chains.py` line 90 references `SystemMessagePromptTemplate` which is not imported in that scope (it's a `NameError`)
- **Action:** Fix the example code in `chains.py`

---

## 🟢 Nice-to-Have Enhancements

### 36. Add Voice Activity Detection (VAD)
- Current recording is duration-based (fixed 5 seconds)
- **Action:** Add VAD using `webrtcvad` or `silero-vad` to detect when the user stops speaking

### 37. Add Multi-Language Support
- Whisper supports 99+ languages but the app doesn't expose language selection
- **Action:** Add `LANGUAGE` config option and pass to Whisper API

### 38. Add Conversation Export
- No way to export conversation history
- **Action:** Add export to Markdown, JSON, or PDF

### 39. Add Audio Visualization
- Frontend could show waveform visualization during recording/playback
- **Action:** Add Web Audio API visualization in the frontend JavaScript

### 40. Add Model Switching at Runtime
- `config/models.yaml` exists but is never loaded or used
- **Action:** Implement runtime model switching using the YAML config

---

## Priority Summary

| Priority | Count | Category |
|----------|-------|----------|
| 🔴 Critical | 5 | Empty tests, missing deps, broken config |
| 🟡 Code Quality | 7 | Logging, error handling, duplication |
| 🟡 Architecture | 6 | Missing frontend, REST API, persistence |
| 🔵 Tooling | 8 | UV, pyproject.toml, type checking |
| 🔵 Dependencies | 5 | Outdated models, missing packages |
| 🔵 Documentation | 4 | README, changelog, examples |
| 🟢 Nice-to-Have | 5 | VAD, multi-language, visualizations |

**Total: 40 improvements identified**
