# NOVA project status

Runtime **0.4.0** implements a bounded part of the **Omega 12** specification. The 365-section [matrix](REQUIREMENT_MATRIX.md) is the scope record; earlier v10 and expansion documents are historical references. This is not the completed Omega operating system.

## Delivered

- Existing durable missions, safe workspace file tools, explicit memory/decisions, local command routing, experimental Windows app resolver and five primary pages preserved.
- OpenAI and Gemini join Ollama/Groq text adapters. Windows DPAPI credential setup, fixed HTTPS endpoints, explicit connection probes, measured request health and an explicitly approved backend fallback are implemented. Configuration is never treated as connectivity.
- Chat stays the launch page; daily clutter and simulated voice controls removed. Privacy/language controls live in Settings. Provider fields clear after saving; unsupported platforms cannot save cloud credentials.
- Owner-uploaded PNG/JPEG local OCR through Tesseract, with input/pixel/output/time limits, installed-language validation and privacy gates. No background capture, screenshot persistence, cloud vision or scene understanding.
- Canonical Omega requirements preserved in full and searchable without granting execution permissions.

## Evidence and limits

Automated Linux regression coverage includes real local OCR, local state/workflows and mocked HTTP/Windows API/DPAPI cases. See [testing](TESTING.md) and release browser evidence for final counts.

Real provider connectivity/model quality requires owner keys entered locally in Settings → AI. No live cloud provider was tested here. Windows DPAPI, native launcher, app discovery and opening require a real Windows PC acceptance run. Tesseract is available on this development machine; Windows OCR requires an installed Tesseract engine and language data.

Voice capture/STT/TTS/wake word, device mesh, full computer/browser control, Office, messaging, auto-reply, smart home and media/game factories remain unimplemented. Auto-reply is OFF. Uploaded-image OCR is not the full vision requirement. Provider fallback is backend-only; adaptive multimodal/cost routing is not implemented. Language matching is model instruction, not a verified language engine.

## Next acceptance work

1. Validate Windows startup, DPAPI and actual app opening on the target PC.
2. Enter OpenAI/Gemini keys locally and explicitly check real text connections; measure language quality.
3. Add permission-scoped screen perception and real audio hardware lifecycle.
4. Continue the canonical priority order, including durable richer missions and authenticated device pairing.
