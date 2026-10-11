# Vision system

Chat → Attach → Read image text accepts an owner-uploaded PNG/JPEG and an explicit extraction action. VisionGateway uses local Tesseract via a fixed stdin/stdout command; no upload to a provider or implicit insertion into chat/memory occurs. The result is transient UI output.

Limits:8MiB input,16million pixels,64KiB subprocess output,20seconds; corrupt images, decompression bombs and unsupported installed languages fail closed. Images are normalized before OCR. Credential-like output is withheld heuristically. NO_CAPTURE/NO_OCR reject processing; LOCAL_VISION_ONLY/NO_CLOUD_VISION permit this local extraction. Emergency stop and dry-run block the core entry point.

Real English OCR was tested on this Linux machine. Windows requires Tesseract and appropriate language data installed separately; missing engines show unavailable. Sinhala OCR accuracy is unverified. There is no screen capture, redaction pipeline, continuous monitoring, visual action verification, scene interpretation or cloud vision adapter.
