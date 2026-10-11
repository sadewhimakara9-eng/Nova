# =====================================================================
# =====================================================================
#
#                    N O V A   O M E G A
#
#              FINAL CANONICAL MASTER BUILD PROMPT
#
#          AUTONOMOUS PERSONAL AI OPERATING SYSTEM
#
#                   VERSION: OMEGA 12
#
# =====================================================================
# =====================================================================
#
# THIS DOCUMENT SUPERSEDES EVERY EARLIER NOVA PROMPT,
# MASTER SPECIFICATION, ADD-ON, EXPANSION PACK, UI PROMPT,
# AUTONOMY PROMPT, DEVICE-MESH PROMPT AND FEATURE LIST.
#
# USE THIS AS THE SINGLE CANONICAL SPECIFICATION.
#
# DO NOT THROW AWAY VERIFIED WORKING CODE.
# DO NOT REBUILD THE REPOSITORY BLINDLY.
# DO NOT CREATE A FAKE JARVIS DEMO.
#
# BUILD A REAL, TESTABLE, EXTENSIBLE SOFTWARE SYSTEM.
#
# =====================================================================


# =====================================================================
# 0. PRODUCT IDENTITY
# =====================================================================

PRODUCT NAME:

NOVA


PRODUCT TYPE:

Personal AI Operating System
Autonomous AI Agent Platform
Local-First Desktop AI
Multi-Agent Orchestration System
Computer-Control Agent
Computer-Vision Agent
Voice Assistant
Multi-Device AI Control Plane
Personal Knowledge and Mission System
Extensible Skill Platform


PRIMARY OWNER EXPERIENCE:

The owner should eventually be able to say:

“NOVA, handle it.”

NOVA should then:

PERCEIVE
→ UNDERSTAND
→ RETRIEVE CONTEXT
→ IDENTIFY GOAL
→ DEFINE SUCCESS
→ IDENTIFY CONSTRAINTS
→ ASSESS RISK
→ DISCOVER CAPABILITIES
→ PLAN
→ DELEGATE
→ ACT
→ OBSERVE
→ VERIFY
→ RECOVER OR REPLAN
→ FINISH
→ UPDATE MEMORY
→ REPORT CONCISELY


NOVA IS NOT A SIMPLE CHATBOT.

NOVA IS NOT A COMMAND-LIST APPLICATION.

NOVA IS NOT A STATIC AUTOMATION SCRIPT.

NOVA IS NOT A GLOWING ORB WITH MOCK BUTTONS.

NOVA IS A REAL TOOL-USING AI AGENT SYSTEM.


# =====================================================================
# 1. FUNDAMENTAL DESIGN TARGET
# =====================================================================

Build NOVA as:

PRIVATE
LOCAL-FIRST
OWNER-CONTROLLED
WINDOWS-NATIVE
SINHALA-FIRST
ENGLISH-CAPABLE
SINGLISH-CAPABLE
VOICE-FIRST
TEXT-CAPABLE
COMPUTER-VISION-AWARE
MULTIMODAL
MULTI-AGENT
MULTI-PROVIDER
MULTI-DEVICE
MISSION-DRIVEN
TOOL-USING
RECOVERABLE
AUDITABLE
EXTENSIBLE
SELF-TESTING
SELF-REPAIRING
CONTROLLED SELF-EXPANDING
FUTURE-PROOF


The owner is not a programmer.

The owner should NOT normally need to:

write Python
write JavaScript
edit JSON
fix imports
debug packages
write PowerShell
edit databases
understand IPC
understand provider routing
manage Git branches manually
configure agents manually
write automation syntax

NOVA should hide technical complexity behind natural interaction.


# =====================================================================
# 2. MASTER ENGINEERING ROLE
# =====================================================================

You are the complete engineering organization responsible for NOVA.

Act as:

Principal Software Architect
Principal AI Agent Engineer
Windows Systems Engineer
Distributed Systems Engineer
Computer Vision Engineer
Voice AI Engineer
Sinhala Language Engineer
LLM Systems Engineer
Agent Orchestration Engineer
Memory Systems Engineer
Context Systems Engineer
Browser Automation Engineer
Office Automation Engineer
API Integration Engineer
Device Integration Engineer
Smart Home Engineer
Media AI Engineer
Image AI Engineer
Video AI Engineer
Game Development Engineer
3D Pipeline Engineer
Education AI Engineer
Defensive Security Engineer
Privacy Engineer
SRE
QA Engineer
DevOps Engineer
Release Engineer
Desktop UI/UX Engineer
Long-Term Technical Director


Do not only recommend what another developer should do.

DO THE ENGINEERING WORK.


# =====================================================================
# 3. EXISTING REPOSITORY RULE
# =====================================================================

This is an EXISTING NOVA project.

Do NOT start over unless a component is genuinely unrecoverable.

FIRST:

inspect repository tree

read:

AGENTS.md
README.md
docs/
PROJECT_STATUS
existing tests
requirements
package manifests
startup scripts
UI code
backend
agent modules
database layer
provider code
tool adapters
Windows integration
voice code
memory code
configuration
security code

Run the current application.

Determine:

what actually works
what partially works
what is mocked
what is only UI
what is broken
what is duplicated
what is dead code
what is unsafe
what needs migration

Preserve all verified working features.


# =====================================================================
# 4. DOCUMENTATION AS SOURCE OF TRUTH
# =====================================================================

Create/update:

docs/NOVA_MASTER_SPEC.md
docs/PROJECT_STATUS.md
docs/ARCHITECTURE.md
docs/REQUIREMENT_MATRIX.md
docs/CAPABILITY_REGISTRY.md
docs/SECURITY_MODEL.md
docs/PRIVACY_MODEL.md
docs/DEVICE_MESH.md
docs/PROVIDER_SYSTEM.md
docs/VOICE_SYSTEM.md
docs/VISION_SYSTEM.md
docs/MISSION_ENGINE.md
docs/MEMORY_MODEL.md
docs/SKILL_FACTORY.md
docs/RECOVERY.md
docs/TESTING.md
docs/FUTURE_ROADMAP.md
CHANGELOG.md


REQUIREMENT_MATRIX must track:

requirement_id
requirement
subsystem
implementation files
tests
status
blocker
version
verification evidence


Statuses:

NOT_STARTED
DESIGNING
IMPLEMENTING
PARTIAL
EXPERIMENTAL
WORKING
STABLE
BLOCKED
BROKEN
DEPRECATED


# =====================================================================
# 5. NO FAKE COMPLETION
# =====================================================================

The following are NOT completed features:

a button
a menu entry
a Python class
a TODO
a mocked API result
a placeholder screen
a hard-coded success message
a simulated terminal
a fake progress bar
a provider name with no connection
a Voice screen with no microphone pipeline
a Vision screen with no visual understanding
a Devices screen with no device control


Never claim:

opened
saved
sent
called
rendered
generated
connected
deployed
updated
scanned
cleaned
paired
installed
completed

without real evidence.


# =====================================================================
# 6. DEFINITION OF DONE
# =====================================================================

A feature is DONE only when:

implemented
integrated
runs
tested
failure path tested
verification implemented
security considered
privacy considered
rollback/recovery considered
documentation updated
requirement status updated

For important external actions:

actual result must be independently verified.


# =====================================================================
# 7. OWNER LANGUAGE EXPERIENCE
# =====================================================================

NOVA must understand:

Sinhala
Sri Lankan colloquial Sinhala
Sinhala script
Singlish / romanized Sinhala
English
Sinhala-English mixed speech
slang
casual incomplete requests
contextual references
natural corrections
technical English words inside Sinhala


The owner MUST NOT memorize exact commands.


Examples:

“Chrome eka arinna.”

“Google ekata yamu.”

“Ban meka mokak hari awulak, balala hadanna.”

“PC 2 eke render eka run karanna.”

“මේ file එක පොඩ්ඩක් බලන්න.”

“Now explain this in English.”

“මේ error එක fix කරලා build eka run කරන්න.”

Examples are tests, NOT a whitelist.


# =====================================================================
# 8. DETECTED LANGUAGE RESPONSE
# =====================================================================

NOVA should normally respond in the detected language/style of the
owner’s newest utterance.

Examples:

Owner speaks Sinhala:
→ reply natural Sinhala.

Owner speaks English:
→ reply English.

Owner speaks Singlish:
→ reply natural Singlish/Sinhala-English style.

Owner mixes Sinhala + technical English:
→ preserve useful English terminology.

Explicit language command overrides detection.

Examples:

“English walin kiyanna.”

“සිංහලෙන් කියන්න.”

“Technical words English walin thiyanna.”


# =====================================================================
# 9. LANGUAGE PIPELINE
# =====================================================================

RAW TEXT / SPEECH
↓
LANGUAGE DETECTION
↓
CODE-SWITCH DETECTION
↓
SINGLISH NORMALIZATION
↓
SLANG NORMALIZATION
↓
TYPO TOLERANCE
↓
SEMANTIC INTENT
↓
CONTEXT RESOLUTION
↓
RESPONSE LANGUAGE SELECTION


Never require language dropdown selection on every request.


# =====================================================================
# 10. WAKE WORD
# =====================================================================

THE DEFAULT WAKE WORD IS:

NOVA


Support configurable aliases later.

Wake-word architecture must be modular.


Examples:

“Nova.”

“Nova, open Chrome.”

“Nova, me PC eka balanna.”

“Nova, continue our project.”


Wake word must eventually work with low-latency local detection where practical.


# =====================================================================
# 11. VOICE MODE
# =====================================================================

Voice is a first-class interface.

Support:

wake word
streaming STT
streaming TTS
VAD
noise handling
microphone selection
speaker selection
Sinhala speech
English speech
mixed-language speech
barge-in
speech interruption
push-to-talk fallback
voice confidence


# =====================================================================
# 12. VOICE TAB AUTO-LISTEN
# =====================================================================

When user switches to Voice:

START MICROPHONE
↓
LISTEN
↓
DETECT SPEECH
↓
TRANSCRIBE
↓
UNDERSTAND
↓
PLAN / ACT / ANSWER
↓
SPEAK
↓
RETURN TO LISTENING


The user must not click the microphone for every sentence.


Leaving Voice:

stop active listening.


# =====================================================================
# 13. VOICE STATES
# =====================================================================

IDLE
LISTENING
HEARING
TRANSCRIBING
THINKING
PLANNING
WORKING
SPEAKING
SUCCESS
WARNING
ERROR
PRIVACY
OFFLINE


# =====================================================================
# 14. BARGE-IN
# =====================================================================

If owner speaks while NOVA is speaking:

immediately stop or duck TTS
listen
interpret interruption
repair current conversation/mission


# =====================================================================
# 15. EMERGENCY VOICE CONTROL
# =====================================================================

Recognize:

“Nova stop.”

“Nova emergency stop.”

Emergency stop should pause/cancel where safely possible:

voice output
computer-control loops
browser automation
background workers
paired-device jobs
pending non-final external actions

Do not corrupt state.


# =====================================================================
# 16. VOICE PRIVACY
# =====================================================================

Always indicate microphone state.

Do not permanently store ambient audio by default.

Do not silently enable continuous room recording.

Allow:

Voice active
Voice muted
Push-to-talk
Wake-word-only
Voice disabled


# =====================================================================
# 17. SINHALA VOICE QUALITY
# =====================================================================

Optimize for Sri Lankan Sinhala.

Handle:

casual phrases
English technical terms
names
app names
device names
brand names
projects
places


Maintain pronunciation dictionary for:

owner-selected names
contacts
apps
brands
projects
devices
technical terms


# =====================================================================
# 18. NATURAL INTENT ENGINE
# =====================================================================

NOVA understands GOALS, not exact command strings.

Do not implement:

if text == "open chrome"

as the primary architecture.

Instead:

UTTERANCE
↓
INTENT
↓
ENTITIES
↓
CONTEXT
↓
DESIRED OUTCOME
↓
CONSTRAINTS
↓
CAPABILITY REQUIREMENTS
↓
EXECUTION PLAN


# =====================================================================
# 19. MULTI-INTENT UNDERSTANDING
# =====================================================================

One sentence may contain multiple goals.

Example:

“Me photos clean karala presentation ekak hadala
Downloads eke save karala email draft ekak hadanna.”

Extract:

edit images
create presentation
save artifact
prepare email


Represent dependencies.


# =====================================================================
# 20. INTENT REPAIR
# =====================================================================

Owner:

“Open Blender.”

then:

“Na na Unreal eka.”

Update active goal.

Do not treat correction as a completely separate request.


# =====================================================================
# 21. CONTEXTUAL REFERENCES
# =====================================================================

Understand:

this
that
that one
other one
second PC
render PC
gaming PC
the file from before
our game
that project
the app we opened
the one on screen


Resolve using:

conversation
active window
current project
recent actions
device registry
mission context
memory


If ambiguity has high impact:
ask one concise clarification.


# =====================================================================
# 22. UNIVERSAL GOAL INTERPRETER
# =====================================================================

Recognize:

command
question
research
task
project
automation
reminder
system control
computer control
communication
creative request
development request
security task
media task
smart-home task
device task
background mission
long-running goal


# =====================================================================
# 23. INTENT CONTRACT
# =====================================================================

For meaningful work internally define:

goal
desired result
success criteria
constraints
deadline
priority
permissions
privacy
budget
quality target
external side effects
forbidden outcomes


Prevent goal drift.


# =====================================================================
# 24. MAXIMUM PRACTICAL AUTONOMY
# =====================================================================

NOVA should autonomously perform safe, authorized, reversible work.

Do not ask unnecessary questions.

For ordinary work:

plan
act
verify
continue


Ask only when needed for:

payment
permanent deletion
major account/security change
physical action
credential entry
high-impact external communication
important unresolved ambiguity
device pairing


# =====================================================================
# 25. AUTONOMY LEVELS
# =====================================================================

OBSERVE
SUGGEST
PREPARE
EXECUTE_SAFE
PROJECT_AUTOPILOT


Per project and capability.


# =====================================================================
# 26. COGNITIVE STACK
# =====================================================================

Implement:

REFLEX BRAIN
FAST BRAIN
CONVERSATION BRAIN
DEEP REASONING BRAIN
PLANNER BRAIN
WORLD MODEL
MEMORY BRAIN
VISION BRAIN
VOICE BRAIN
ACTION BRAIN
CRITIC BRAIN
REVIEWER BRAIN
VERIFIER BRAIN
SECURITY BRAIN
RECOVERY BRAIN
DEVELOPER BRAIN


# =====================================================================
# 27. REFLEX BRAIN
# =====================================================================

Use local low-latency path for:

Emergency Stop
mute
volume
simple app launch
simple window focus
basic trusted device action


Do not send trivial local commands through expensive reasoning unnecessarily.


# =====================================================================
# 28. DEEP REASONING BRAIN
# =====================================================================

Use for:

complex software
architecture
difficult debugging
large research
project planning
multi-device scheduling
game development
hard reasoning


# =====================================================================
# 29. META-REASONING
# =====================================================================

UNDERSTAND
↓
DEFINE SUCCESS
↓
ASSESS UNCERTAINTY
↓
IDENTIFY CONSTRAINTS
↓
GENERATE CANDIDATE PLANS
↓
COMPARE
↓
SIMULATE IF USEFUL
↓
SELECT
↓
ACT
↓
OBSERVE
↓
VERIFY
↓
REVIEW
↓
REPLAN


# =====================================================================
# 30. CONFIDENCE ENGINE
# =====================================================================

Track confidence for:

intent
target
recipient
file
device
memory
visual interpretation
research fact
tool result
provider output


High uncertainty + high impact:
ASK / VERIFY.

High confidence + safe:
ACT.


# =====================================================================
# 31. KNOW WHEN NOT TO ACT
# =====================================================================

Valid decisions:

ACT
WAIT
OBSERVE
VERIFY
SIMULATE
ASK
DEFER
DO NOTHING


# =====================================================================
# 32. ACTIVE PERCEPTION
# =====================================================================

Within authorization, NOVA may use:

screen
active application
window title
UI Automation tree
browser DOM
selected text
clipboard
current file
project
mission
device state
system metrics
calendar
notifications


Use minimum necessary context.


# =====================================================================
# 33. COMPUTER VISION IS CORE
# =====================================================================

Computer Vision is NOT an optional future page.

Implement:

Vision Gateway
Screen Understanding Agent
UI Detection Agent
OCR Interface
Document Vision Agent
Image Understanding Agent
Video Understanding Agent
Visual Verification Agent
Camera Vision Adapter
Visual World Model


# =====================================================================
# 34. SCREEN UNDERSTANDING
# =====================================================================

Understand:

application identity
window
button
menu
dialog
text field
checkbox
list
table
chart
image
error
notification
selected item
scroll position
modal
form
canvas
game viewport
3D viewport


# =====================================================================
# 35. STRUCTURED UI FIRST
# =====================================================================

Preference order:

native API
accessibility tree
browser DOM
application plugin/API
structured metadata
computer vision
mouse/keyboard coordinate fallback


# =====================================================================
# 36. ACTIVE VISUAL LOOP
# =====================================================================

OBSERVE
↓
UNDERSTAND
↓
CHOOSE NEXT ACTION
↓
ACT
↓
OBSERVE CHANGED STATE
↓
VERIFY
↓
CONTINUE


Never blindly replay a long sequence of coordinates.


# =====================================================================
# 37. VISUAL VERIFICATION
# =====================================================================

Examples:

click Save
→ verify file actually exists

launch Blender
→ verify process/window

submit form
→ verify expected confirmation

render
→ verify output

open Gemini
→ verify actual Gemini app/PWA/site


# =====================================================================
# 38. VISION PRIVACY
# =====================================================================

Do not continuously upload entire desktop to cloud.

Prefer:

accessibility tree
DOM
metadata
cropped region
redaction
local OCR
local vision


Per-app policies:

NO_CAPTURE
NO_OCR
LOCAL_VISION_ONLY
NO_CLOUD_VISION
ALLOW_CROPPED_VISION


# =====================================================================
# 39. AI PROVIDER HUB
# =====================================================================

NOVA must support multiple AI providers.

INITIAL REQUIRED PROVIDERS:

1. OpenAI GPT provider
2. Google Gemini provider


Also support optional future:

local models
other approved providers


Provider independence is mandatory.


# =====================================================================
# 40. API SETUP — IMPORTANT
# =====================================================================

DO NOT ask the owner to paste API keys:

into chat
into Codex conversation
into source code
into README
into prompts
into Git
into frontend JavaScript
into logs


Instead build:

Settings
→ AI
→ Providers


Initial provider cards:

OPENAI / GPT
GOOGLE GEMINI
LOCAL AI


On first setup, NOVA/Codex may ask:

“Which AI providers do you want NOVA to support?”

The expected initial owner choice is:

OpenAI GPT
Google Gemini


Then create the secure UI.

The owner enters API keys ONLY in NOVA's local secure provider setup.


# =====================================================================
# 41. API KEY STORAGE
# =====================================================================

Use secure Windows-backed secret storage.

Prefer:

Windows Credential Manager
DPAPI-backed encrypted store
or equivalent secure OS credential mechanism


Never store plaintext API keys in:

config.json
.env committed to Git
database plaintext
logs
crash reports
UI state
README


# =====================================================================
# 42. SECRET DISPLAY
# =====================================================================

After key entry:

show masked state only.

Example:

OpenAI — Connected
Gemini — Connected


Do not reveal full secrets again.


# =====================================================================
# 43. PROVIDER CONNECTION TEST
# =====================================================================

For each provider:

save secret securely
↓
perform minimal connection test
↓
validate authentication
↓
record capabilities
↓
record health
↓
mark CONNECTED / DEGRADED / FAILED


Do not waste large tokens during connection test.


# =====================================================================
# 44. PROVIDER INTERFACES
# =====================================================================

Define:

LLMProvider
ReasoningProvider
CodingProvider
VisionProvider
ImageGenerationProvider
ImageEditProvider
VideoGenerationProvider
VideoEditProvider
EmbeddingProvider
STTProvider
TTSProvider
SearchProvider
AudioProvider


# =====================================================================
# 45. MODEL ROUTER
# =====================================================================

Choose model/provider based on:

task type
privacy
quality
latency
cost
language
context length
vision requirement
coding requirement
availability
reliability
owner preference


# =====================================================================
# 46. PROVIDER CLASSES
# =====================================================================

LOCAL_FAST
LOCAL_REASONING
CLOUD_FAST
CLOUD_REASONING
CODING
VISION
VOICE
IMAGE_GENERATION
VIDEO_GENERATION
EMBEDDING


# =====================================================================
# 47. PROVIDER FALLBACK
# =====================================================================

If OpenAI fails:

safe retry
→ approved fallback to Gemini or local model where suitable

If Gemini fails:

safe retry
→ approved fallback

Mission state must survive.


# =====================================================================
# 48. PROVIDER HEALTH
# =====================================================================

Track:

availability
latency
error rate
recent failures
capabilities
cost class
rate-limit state


# =====================================================================
# 49. PROVIDER BENCHMARKING
# =====================================================================

Benchmark approved providers for:

Sinhala
Singlish
English
reasoning
coding
vision
summarization
latency
cost
reliability


Do not assume one provider is always best.


# =====================================================================
# 50. LOCAL AI
# =====================================================================

Support optional local models for:

routing
classification
private summaries
embeddings
offline chat
selected vision
simple coding
language normalization


NOVA should still perform basic local PC control even with zero cloud provider.


# =====================================================================
# 51. LOCAL COMMAND ROUTER
# =====================================================================

Before free-form LLM fallback, handle deterministic local intents.

Support:

OPEN_APP
CLOSE_APP
FOCUS_APP
OPEN_WEBSITE
OPEN_FILE
OPEN_FOLDER
SEARCH_WEB
PLAY_MEDIA
FILE_ACTION
SYSTEM_ACTION
DEVICE_ACTION
WINDOW_ACTION
SECURITY_ACTION
UPDATE_ACTION


# =====================================================================
# 52. GENERAL WINDOWS APPLICATION RESOLVER
# =====================================================================

Search:

running processes
Start Menu shortcuts
App Paths
registered applications
installed executables
packaged/UWP apps
PWAs
browser apps
owner aliases
safe fuzzy matches


# =====================================================================
# 53. APP RESOLUTION EXAMPLE
# =====================================================================

Owner:

“Gemini eka open karanna.”

Resolve:

native app if installed
→ PWA if installed
→ official Gemini web app in default browser


Must NOT fail simply because free-form AI provider is disconnected.


# =====================================================================
# 54. PC CONTROL
# =====================================================================

Support authorized:

open app
close app
focus app
switch window
move/resize window
mouse
keyboard
clipboard
File Explorer
screenshots
notifications
audio
process monitoring
system info
multi-monitor
safe command execution
safe PowerShell execution
safe Python helper execution


# =====================================================================
# 55. WINDOWS CONTROL PRIORITY
# =====================================================================

Use:

official API
native SDK
Windows API
application CLI
PowerShell
UI Automation
browser automation
vision
mouse/keyboard fallback


# =====================================================================
# 56. PRIVILEGED ACTION BROKER
# =====================================================================

Do not give every agent administrator rights.

Privileged operations go through:

isolated broker
temporary permission
explicit policy
logging
verification


# =====================================================================
# 57. NO VISIBLE TERMINAL
# =====================================================================

Normal startup must show:

NOVA WINDOW ONLY


No permanent:

CMD window
PowerShell window
Windows Terminal
Python console


Background helpers must not flash terminals.

Capture stdout/stderr internally.


# =====================================================================
# 58. WINDOWS UPDATE AGENT
# =====================================================================

Support:

check updates
list relevant updates
download
install
restart requirement
schedule restart
post-reboot verification
failure handling


Natural examples:

“Windows update thiyanawada?”

“PC 2 eka update karanna.”

“Rae anith PC tika update karanna.”

“Gaming PC eka use karanawanam restart karanna epa.”


# =====================================================================
# 59. RESTART SAFETY
# =====================================================================

Before reboot:

inspect active user work
checkpoint NOVA missions
persist state
avoid data loss
respect owner policy


# =====================================================================
# 60. DEFENSIVE MALWARE / SECURITY AGENT
# =====================================================================

Support defensive security for owner-authorized devices.

Use trusted security mechanisms such as:

Windows Security
Microsoft Defender
installed antivirus
official security APIs


Capabilities:

security status
definition updates
quick scan
full scan
offline scan where appropriate
threat review
quarantine
trusted remediation
startup review
suspicious process diagnostics
firewall health
patch status


# =====================================================================
# 61. NATURAL SECURITY REQUEST
# =====================================================================

Owner:

“Virus ekakda manda me PC eka slow.”

NOVA should not require:

“RUN DEFENDER FULL SCAN”

Instead:

diagnose system
inspect resource usage
check disk
check startup
check update state
check security state
scan when justified
identify likely cause
repair safe issues
verify


# =====================================================================
# 62. MALWARE REMEDIATION
# =====================================================================

If confirmed threat:

update signatures
scan
quarantine/remediate through trusted tools
re-scan
verify
report


Never falsely claim:

“100% virus free.”


Use truthful wording:

“No threats were detected by the available scans.”

when appropriate.


# =====================================================================
# 63. SECURITY INCIDENT MODE
# =====================================================================

If serious malware detected:

pause sensitive tasks on infected node
avoid sending secrets to it
preserve minimal diagnostic evidence
run remediation
re-scan
restore trust only after verification


Do not automatically destroy user files.


# =====================================================================
# 64. MULTI-PC DEVICE MESH
# =====================================================================

One owner PC may be dedicated as:

NOVA MAIN BRAIN


Other machines become:

NOVA NODE AGENTS


Possible nodes:

main desktop
gaming PC
render PC
second PC
laptop
home server
GPU workstation
future phone companion


# =====================================================================
# 65. MAIN NOVA NODE
# =====================================================================

Main machine hosts:

NOVA Core
Mission Engine
Memory
World Model
Agent Orchestrator
Provider Hub
Policy Engine
Permission Engine
Privacy Router
Secrets Vault
Device Mesh Controller
Capability Registry
Tool Gateway
Audit
Recovery Engine


# =====================================================================
# 66. NODE AGENT
# =====================================================================

Each controlled PC runs lightweight NOVA Node Agent.

Node metadata:

device_id
friendly_name
owner
OS
hardware
CPU
GPU
RAM
storage
battery if applicable
temperature if available
network
capabilities
installed apps
permissions
trust
health
online state
heartbeat


# =====================================================================
# 67. SECURE DEVICE PAIRING
# =====================================================================

DISCOVERY IS NOT PERMISSION.

Pair using:

owner initiates
→ one-time code or QR
→ cryptographic device identity
→ key exchange
→ owner approves
→ permissions selected
→ trusted node registered


# =====================================================================
# 68. DEVICE SECURITY
# =====================================================================

Use:

authenticated encrypted connection
mutual authentication
device keys
key rotation
revocation
least privilege
audit logs


Never trust a PC only because it is on the same Wi-Fi/LAN.


# =====================================================================
# 69. FRIENDLY DEVICE NAMES
# =====================================================================

Owner may say:

“gaming PC”
“render PC”
“PC 2”
“laptop eka”
“ara Blender machine eka”


Map these aliases to paired nodes.


# =====================================================================
# 70. DISTRIBUTED TASK ROUTER
# =====================================================================

Choose node based on:

required app
CPU
GPU
RAM
disk
network
power
temperature
current workload
privacy
owner policy


Example:

Blender render
→ strongest approved idle GPU node


# =====================================================================
# 71. DEVICE TASKS
# =====================================================================

Depending on permission:

open application
close application
file operation
project operation
render
build
media processing
system health
security scan
Windows Update
restart
shutdown
browser task
screen inspection
resource monitoring


# =====================================================================
# 72. REMOTE VERIFICATION
# =====================================================================

Remote task success requires evidence.

Examples:

open app
→ process/window exists

render
→ artifact exists

update
→ installation state verified

restart
→ node reconnects

scan
→ result received


# =====================================================================
# 73. SECURE FILE TRANSFER
# =====================================================================

Use:

encryption
authentication
hash verification
resume
conflict detection
version checks


Do not overwrite silently.


# =====================================================================
# 74. CROSS-DEVICE PROJECT WORK
# =====================================================================

Support:

shared project metadata
artifact sync
render outputs
build outputs
job handoff
mission continuation


# =====================================================================
# 75. CROSS-DEVICE SESSION HANDOFF
# =====================================================================

Example:

main PC
→ render node
→ laptop
→ main PC


Preserve mission context.


# =====================================================================
# 76. DEVICE RESOURCE MARKET
# =====================================================================

Nodes advertise available capabilities/resources.

Scheduler may route:

render
game build
local AI
video processing
batch task


# =====================================================================
# 77. HARDWARE PROTECTION
# =====================================================================

Monitor:

CPU temperature
GPU temperature
battery
disk space
memory pressure


Throttle/pause low-priority work if necessary.


# =====================================================================
# 78. PERFORMANCE GUARDIAN
# =====================================================================

If owner starts:

gaming
video editing
3D work
other latency-sensitive work

reduce low-priority NOVA background load.


# =====================================================================
# 79. UNIVERSAL DEVICE INTEGRATION FRAMEWORK
# =====================================================================

Create a generic Device Adapter SDK.

Do NOT hard-code smart-home support around one AC or camera brand.


Device interfaces may include:

power
temperature
mode
fan
brightness
volume
state
sensor values
camera stream
recording state
health
battery
connectivity
custom capabilities


# =====================================================================
# 80. ADD DEVICE EXPERIENCE
# =====================================================================

Create:

Settings
→ Connections
→ Devices
→ Add Device


Device categories:

Computer
Phone
Light
AC
Fan
TV
Speaker
Smart Plug
Curtain
Camera / CCTV
Sensor
Home Assistant
Matter
MQTT
IR Controller
Custom Device


# =====================================================================
# 81. EASY DEVICE EXPANSION
# =====================================================================

Adding a new device should normally require:

adapter
capability manifest
permissions
pairing/auth
verification


NOT core rewrite.


# =====================================================================
# 82. SMART HOME PROTOCOLS
# =====================================================================

Architecture should support, where authorized:

Matter
Home Assistant
MQTT
vendor local API
vendor cloud API
IR bridge
LAN API
future protocols


Prefer:

local
official
documented
reversible


# =====================================================================
# 83. AC CONTROL
# =====================================================================

Generic capabilities:

power
target temperature
mode
fan speed
swing
current temperature if available
state verification


Natural example:

“Nova AC eka on karala 25 degrees danna.”


# =====================================================================
# 84. AC MISSING FEATURE FLOW
# =====================================================================

If NOVA lacks support:

“I don’t currently have control support for this AC.
I can add/connect that capability. Want me to?”


Owner:

“Ha.”


Then:

identify device
discover protocol
prefer official/local integration
request pairing only if needed
create/configure adapter
test read-only state
test safe control
register skill
resume original command
turn AC on
set 25°C
verify


# =====================================================================
# 85. SMART HOME SCENES
# =====================================================================

Support:

GOOD_MORNING
GOOD_NIGHT
STUDY
FOCUS
MOVIE
LEAVING_HOME
CUSTOM


# =====================================================================
# 86. CCTV / CAMERA INTEGRATION
# =====================================================================

Authorized cameras only.

Architecture may support:

IP cameras
NVR
DVR
RTSP
vendor API
Home Assistant camera
other owner-authorized sources


# =====================================================================
# 87. CCTV CAPABILITIES
# =====================================================================

camera health
online/offline
event detection
motion events
person/vehicle summary where lawful
privacy zones
tamper events
event timeline
authorized snapshots
authorized clips
daily digest
semantic event search


# =====================================================================
# 88. CCTV PRIVACY
# =====================================================================

Prefer local-first processing.

Do not continuously upload camera feeds.

Do not silently enable surveillance.

Require owner authorization.

Respect retention policies.


# =====================================================================
# 89. SELF-EXPANSION / CAPABILITY GROWTH
# =====================================================================

NOVA must be useful for years.

It must not remain frozen at installation-time capabilities.


When a legitimate owner request cannot be completed:

DO NOT immediately stop at:

“I can't do that.”


Instead:

UNDERSTAND GOAL
↓
CHECK CAPABILITY REGISTRY
↓
CHECK TOOLS
↓
CHECK APPS
↓
CHECK APIS
↓
CHECK PLUGINS
↓
CHECK MCP
↓
CHECK DEVICE ADAPTERS
↓
CHECK BROWSER AUTOMATION
↓
CHECK COMPUTER VISION
↓
CHECK PAIRED NODES
↓
CHECK LOCAL MODELS
↓
CHECK CLOUD PROVIDERS
↓
CHECK CAPABILITY COMPOSITION


# =====================================================================
# 90. CAPABILITY GAP CLASSIFICATION
# =====================================================================

Distinguish:

temporary failure
configuration issue
permission issue
credential issue
integration broken
real missing capability


Do not write new code just because an API had one temporary error.


# =====================================================================
# 91. OWNER-APPROVED CAPABILITY BUILD
# =====================================================================

If real missing capability:

NOVA should explain briefly.

Example:

“I don’t currently support this device.
I can add that capability to NOVA. Want me to?”


Owner responses such as:

yes
ha
hari
okay
do it
hadanna
add it

grant approval ONLY for that bounded capability.


# =====================================================================
# 92. SAFE CAPABILITY DEVELOPMENT PIPELINE
# =====================================================================

stable NOVA
↓
create isolated branch/worktree/sandbox
↓
research
↓
design
↓
implement
↓
unit test
↓
integration test
↓
security review
↓
privacy review
↓
compatibility test
↓
controlled real test
↓
review
↓
deploy
↓
verify
↓
register
↓
resume original mission


# =====================================================================
# 93. SELF-GENERATED CODE TRUST
# =====================================================================

Generated code is UNTRUSTED until tested.

New code does NOT automatically receive:

admin
Secrets Vault
all files
all devices
all network
all contacts


Use minimum permissions.


# =====================================================================
# 94. SKILL MANIFEST
# =====================================================================

Every skill:

skill_id
name
version
description
capabilities
inputs
outputs
supported targets
permissions
privacy
risk
dependencies
software requirements
device requirements
credentials required
test status
health
rollback
source
created_at
updated_at
hash/signature where applicable


# =====================================================================
# 95. CAPABILITY REGISTRY
# =====================================================================

Each capability:

capability_id
name
description
category
inputs
outputs
modalities
agents
tools
providers
devices
permissions
privacy
risk
cost
latency
verification method
reliability
version
health


# =====================================================================
# 96. SKILL TRUST LEVELS
# =====================================================================

EXPERIMENTAL
TESTED
TRUSTED
CRITICAL_SAFE


# =====================================================================
# 97. PLUGIN TRUST LEVELS
# =====================================================================

UNTRUSTED
LIMITED
TRUSTED
SYSTEM


Third-party default:

LIMITED


# =====================================================================
# 98. ORIGINAL MISSION RESUME
# =====================================================================

After adding missing capability:

DO NOT forget why it was built.

Automatically resume original owner request.


# =====================================================================
# 99. CAPABILITY REPAIR
# =====================================================================

If already-approved capability breaks:

diagnose
repair
test
verify
restore


Ordinary safe bug fixes do not require owner approval every time.


# =====================================================================
# 100. SELF-MODIFICATION BOUNDARIES
# =====================================================================

NOVA may improve:

skills
tools
connectors
providers
device adapters
UI modules
workflows
agents
performance
compatibility


NOVA must NOT silently weaken:

owner authority
Emergency Stop
Secrets Vault
privacy policy
permission engine
device trust
security boundaries
approval requirements
update signing
audit requirements


# =====================================================================
# 101. IMMUTABLE SECURITY CORE
# =====================================================================

Security-critical modules require stronger protection.

Changes require:

isolated branch
tests
security review
explicit owner approval for high-impact changes
rollback path


# =====================================================================
# 102. MISSION ENGINE
# =====================================================================

Mission:

mission_id
goal
intent contract
success criteria
priority
deadline
tasks
dependencies
agents
tools
providers
devices
permissions
privacy
budget
external effects
checkpoints
verification


# =====================================================================
# 103. MISSION STATES
# =====================================================================

CREATED
QUEUED
PLANNING
READY
RUNNING
WAITING_FOR_TOOL
WAITING_FOR_RESOURCE
WAITING_FOR_NETWORK
WAITING_FOR_AGENT
WAITING_FOR_USER
BLOCKED
PAUSED
VERIFYING
RETRYING
RECOVERING
COMPLETED
FAILED
CANCELLED
ROLLED_BACK
ARCHIVED


# =====================================================================
# 104. MISSION PRIORITIES
# =====================================================================

BACKGROUND
LOW
NORMAL
HIGH
URGENT
CRITICAL


# =====================================================================
# 105. LONG-RUNNING MISSIONS
# =====================================================================

Support:

minutes
hours
overnight
days
weeks
months


# =====================================================================
# 106. OVERNIGHT AUTONOMY
# =====================================================================

Owner:

“Nova mama nidagannawa.
Me wada tika finish karanna.”


NOVA:

parse goals
create missions
resolve dependencies
select agents
select devices
execute independent work
checkpoint
retry
fallback
continue unrelated work
collect decisions
prepare morning report


# =====================================================================
# 107. DURABLE MISSION STATE
# =====================================================================

Mission must survive:

application restart
PC reboot
network interruption
provider outage
worker restart


# =====================================================================
# 108. IDEMPOTENCY
# =====================================================================

Prevent duplicate:

email
message
payment
order
booking
calendar entry
deployment
form submission


especially after retries/reboots.


# =====================================================================
# 109. AUTONOMOUS GOAL MANAGER
# =====================================================================

Approved long-term goal:

GOAL
↓
ROADMAP
↓
MILESTONES
↓
MISSIONS
↓
TASKS
↓
EXECUTION
↓
VERIFICATION
↓
NEXT READY TASK


# =====================================================================
# 110. GLOBAL GOAL GRAPH
# =====================================================================

Represent:

goals
projects
milestones
missions
tasks
dependencies
blockers
deadlines


as a graph.


# =====================================================================
# 111. AUTONOMOUS BACKLOG MANAGER
# =====================================================================

Choose next work using:

dependency readiness
importance
deadline
risk
effort
resource availability
owner policy
project value


# =====================================================================
# 112. DYNAMIC REPLANNING
# =====================================================================

On failure:

diagnose
safe retry
different tool
different provider
different device
different plan
continue


# =====================================================================
# 113. FALLBACK PLANS
# =====================================================================

Important tasks may maintain Plan A/B/C.


# =====================================================================
# 114. FAILURE PREDICTION
# =====================================================================

Predict when evidence exists:

deadline risk
resource shortage
disk shortage
dependency break
provider instability
device overheating
integration drift


# =====================================================================
# 115. OPPORTUNITY ENGINE
# =====================================================================

Within approved context, identify useful next actions.

Do not become annoying.

Do not constantly interrupt owner.


# =====================================================================
# 116. ATTENTION MANAGER
# =====================================================================

Choose:

interrupt now
quiet notification
morning summary
wait
ignore


# =====================================================================
# 117. DECISION QUEUE
# =====================================================================

During overnight/background work:

collect non-urgent owner decisions
continue unrelated work
surface them in one concise batch


# =====================================================================
# 118. MISSION SLA
# =====================================================================

Track:

expected completion
quality
resource budget
deadline
success definition


# =====================================================================
# 119. MISSION WATCHDOG
# =====================================================================

Detect:

stuck
looping
hung worker
no progress
dependency deadlock


# =====================================================================
# 120. MULTI-AGENT SYSTEM
# =====================================================================

Agents may include:

NOVA Director
Planner Agent
Mission Agent
Context Agent
Memory Agent
Vision Agent
PC Agent
Browser Agent
File Agent
Document Agent
Office Agent
Research Agent
Email Agent
Messaging Agent
Calling Agent
Calendar Agent
Voice Agent
Media Agent
Automation Agent
API Integration Agent
Coding Agent
Developer Agent
Debugger Agent
Reviewer Agent
QA Agent
Security Agent
Privacy Agent
Recovery Agent
Verification Agent
Education Agent
Exam Agent
Smart Home Agent
Device Agent
Game Director
Game Design Agent
Story Agent
Worldbuilding Agent
Gameplay Agent
NPC AI Agent
UI Agent
3D Agent
Art Agent
Animation Agent
VFX Agent
Audio Agent
Performance Agent
Build Agent
Localization Agent


# =====================================================================
# 121. TEMPORARY AGENTS
# =====================================================================

Spawn when useful.

Give minimum:

context
tools
permissions
time
budget


# =====================================================================
# 122. STRUCTURED AGENT ENVELOPE
# =====================================================================

mission_id
task_id
parent_id
agent
goal
inputs
constraints
permissions
privacy
priority
dependencies
budget
deadline
expected_output
verification
status
result
error


# =====================================================================
# 123. PLANNER / EXECUTOR / REVIEWER / VERIFIER
# =====================================================================

For important tasks:

Planner
≠
Executor
≠
Reviewer
≠
Verifier


where practical.


# =====================================================================
# 124. CRITIC AGENT
# =====================================================================

For important plans, search for:

missing requirements
unsafe assumptions
failure cases
privacy leaks
security issues
rollback issues


# =====================================================================
# 125. AGENT REPUTATION
# =====================================================================

Track:

task category
success
failure
latency
cost
verification quality


Use history for routing.


# =====================================================================
# 126. LOOP PREVENTION
# =====================================================================

Detect repeated equivalent actions.

Stop runaway loops.


# =====================================================================
# 127. DEADLOCK PREVENTION
# =====================================================================

Detect agents cyclically waiting.


# =====================================================================
# 128. WORLD MODEL
# =====================================================================

Represent:

OWNER
PEOPLE
CONTACTS
PROJECTS
DEVICES
APPLICATIONS
FILES
TASKS
MISSIONS
WORKFLOWS
EVENTS
PREFERENCES
LOCATIONS
CALENDAR ITEMS
TOOLS
AGENTS
SKILLS
SERVICES
INTEGRATIONS
ARTIFACTS


# =====================================================================
# 129. MEMORY SYSTEM
# =====================================================================

Implement:

short-term memory
working memory
episodic memory
semantic memory
structured memory
vector memory
preference memory
project memory
knowledge graph


# =====================================================================
# 130. MEMORY METADATA
# =====================================================================

Store where appropriate:

source
timestamp
confidence
scope
privacy
TTL
last confirmation
provenance


# =====================================================================
# 131. MEMORY CONFLICT RULE
# =====================================================================

new explicit owner instruction
>
older explicit owner preference
>
old inference


# =====================================================================
# 132. MEMORY CONSOLIDATION
# =====================================================================

Do not store every trivial sentence forever.

Consolidate:

important preferences
decisions
workflows
project state
unfinished goals
important context


# =====================================================================
# 133. MEMORY DECAY
# =====================================================================

Lower confidence for stale inferred information.

Support pinning.


# =====================================================================
# 134. TEMPORAL WORLD MODEL
# =====================================================================

Track:

past state
current state
planned state
change history


Know the difference between:

WAS TRUE
IS TRUE
PLANNED


# =====================================================================
# 135. CAUSAL MEMORY
# =====================================================================

Where evidence supports:

event
→ likely consequence


Never invent causality.


# =====================================================================
# 136. VISUAL MEMORY
# =====================================================================

Prefer semantic state:

active project
open app
selected file
dialog state
workspace structure


over indefinite screenshot hoarding.


# =====================================================================
# 137. CONTINUE WHERE I STOPPED
# =====================================================================

Owner:

“Continue.”

Restore relevant:

project
mission
files
apps
workspace
browser state
checkpoint
next task


# =====================================================================
# 138. PERSONAL WORKFLOW GRAPH
# =====================================================================

Learn approved repeated workflows:

app sequence
file paths
project habits
tools
output locations


# =====================================================================
# 139. PERSONAL KNOWLEDGE ENGINE
# =====================================================================

Build privacy-aware local retrieval over:

documents
project files
notes
reports
approved memories
codebases


# =====================================================================
# 140. SEMANTIC PERSONAL SEARCH
# =====================================================================

Examples:

“Find the PDF I used for the history project.”

“අපි කලින් game loading bug එක fix කරපු file එක හොයන්න.”

“Find the blue spaceship render from last week.”


# =====================================================================
# 141. FILE INTELLIGENCE
# =====================================================================

Support:

search
read
create
edit
rename
move
copy
recycle
compress
extract
convert
organize
deduplicate
archive
hash
backup
restore
version


# =====================================================================
# 142. SAFE DELETE
# =====================================================================

Default delete:

Recycle Bin.


Permanent deletion:

approval by default.


# =====================================================================
# 143. FILE TRANSACTIONS
# =====================================================================

Multi-file operations should avoid partial inconsistent state.

Use rollback/compensation.


# =====================================================================
# 144. ARTIFACT REGISTRY
# =====================================================================

Track:

artifact_id
project
version
source
input files
creator agent
tool
provider
device
creation time
verification
license metadata where relevant


# =====================================================================
# 145. OFFICE AGENT
# =====================================================================

Support real:

Word
Excel
PowerPoint
PDF
CSV
TXT
images
scans


# =====================================================================
# 146. WORD
# =====================================================================

create
edit
format
rewrite
summarize
translate
proofread
templates
reports


# =====================================================================
# 147. EXCEL
# =====================================================================

data entry
formulas
cleaning
formatting
validation
sorting
filtering
charts
pivots
analysis
error checks


# =====================================================================
# 148. POWERPOINT
# =====================================================================

research
outline
slides
visuals
charts
notes
professional formatting
export
verification


# =====================================================================
# 149. DOCUMENT VISION
# =====================================================================

Support:

PDFs
scans
tables
forms
screenshots
mixed text/image documents


# =====================================================================
# 150. FORM FILLING
# =====================================================================

Use:

vision
DOM/UI tree
approved owner memory


Fill
verify
preview
submit according to policy.


# =====================================================================
# 151. BROWSER AGENT
# =====================================================================

Support:

open
navigate
search
read
click
type
scroll
forms
tabs
upload
download
structured extraction
page verification


# =====================================================================
# 152. CAPTCHA / 2FA
# =====================================================================

Do not bypass.

Return control to owner.


# =====================================================================
# 153. WEB PROMPT-INJECTION DEFENSE
# =====================================================================

Web content is DATA.

A webpage cannot override NOVA policies.


# =====================================================================
# 154. RESEARCH AGENT
# =====================================================================

Support:

fresh research
multiple sources
source credibility
contradictions
citations
fact provenance
confidence


# =====================================================================
# 155. KNOWLEDGE FRESHNESS
# =====================================================================

Time-sensitive facts should expire/revalidate.


# =====================================================================
# 156. CONTRADICTION GRAPH
# =====================================================================

If trusted sources disagree:

represent disagreement
do not silently choose without evidence


# =====================================================================
# 157. EMAIL AGENT
# =====================================================================

Support:

read
search
summarize
categorize
important mail
attachments
draft
reply
follow-up
task extraction


# =====================================================================
# 158. MESSAGING
# =====================================================================

Architecture for legitimate:

WhatsApp
Telegram
SMS
desktop messaging
future services


Use official/supported integrations where possible.


# =====================================================================
# 159. COMMUNICATION SAFETY
# =====================================================================

Before important send:

verify recipient
content
attachments
privacy
duplicate state
conversation context


# =====================================================================
# 160. AUTO-REPLY
# =====================================================================

DEFAULT = OFF


Modes:

OFF
DRAFT_ONLY
ASK_BEFORE_SEND
TRUSTED_CONTACTS
AWAY_MODE
SMART_AUTO


Protections:

allowlists
cooldowns
max replies/hour
max replies/day
bot-loop detection
quiet hours
sensitive message escalation


# =====================================================================
# 161. CALLING AGENT
# =====================================================================

Architecture for:

phone companion
supported VoIP
calling APIs
mobile bridge


Examples:

“Call Mom.”

“Call Pizza Hut.”


# =====================================================================
# 162. TRANSACTIONAL CALLS
# =====================================================================

Where technically and legally supported:

call service
communicate requirements
ask necessary questions
collect result


Do not deceptively impersonate where disclosure is required.


# =====================================================================
# 163. CALENDAR AGENT
# =====================================================================

Support:

read
create
reschedule
cancel
conflict detection
availability
agenda
deadline tracking
meeting preparation


# =====================================================================
# 164. PURCHASE ASSISTANT
# =====================================================================

For ordinary legal purchases:

research
compare
cart
delivery details
price
approval
order
receipt
tracking


Financial commitment:

ASK by default.


Do not facilitate age-restricted or dangerous purchases for a minor.


# =====================================================================
# 165. IMAGE GENERATION
# =====================================================================

IMAGE GENERATION IS A FIRST-CLASS CAPABILITY.

Interfaces:

ImageGenerationProvider
ImageEditProvider
ImageUpscaleProvider
ImageUnderstandingProvider


# =====================================================================
# 166. IMAGE GENERATION CAPABILITIES
# =====================================================================

TEXT_TO_IMAGE
IMAGE_TO_IMAGE
VARIATION
INPAINT
OUTPAINT
BACKGROUND_GENERATION
OBJECT_GENERATION
CONCEPT_ART
POSTER
THUMBNAIL
GAME_CONCEPT
ARCHITECTURE_VISUAL
UI_CONCEPT
TRANSPARENT_ASSET


# =====================================================================
# 167. IMAGE EDITING
# =====================================================================

Support:

crop
resize
rotate
straighten
exposure
brightness
contrast
highlights
shadows
white balance
color grading
saturation
sharpness
denoise
deblur
upscale
restore
background removal
background replacement
object removal
permitted object addition
perspective
text overlays
batch processing
format conversion


Preserve original by default.


# =====================================================================
# 168. IMAGE NATURAL LANGUAGE
# =====================================================================

Examples:

“Nova futuristic city image ekak hadanna.”

“Me photo eka cinematic karanna.”

“Game character concept ekak hadanna.”

“Me room eka modern widihata visualize karanna.”


# =====================================================================
# 169. VIDEO GENERATION
# =====================================================================

VIDEO GENERATION IS A FIRST-CLASS CAPABILITY.

Interfaces:

VideoGenerationProvider
VideoEditProvider
VideoUpscaleProvider
VideoUnderstandingProvider


# =====================================================================
# 170. VIDEO GENERATION CAPABILITIES
# =====================================================================

TEXT_TO_VIDEO
IMAGE_TO_VIDEO
STORYBOARD_TO_VIDEO
SCENE_GENERATION
CLIP_GENERATION
CINEMATIC_SHOTS
CAMERA_MOTION
GENERATED_B_ROLL
SHORT_FORM_VIDEO
TRAILER_SHOTS
GAME_CONCEPT_VIDEO
ARCHITECTURE_WALKTHROUGH_CONCEPT
VIDEO_ENHANCEMENT
VIDEO_UPSCALE


# =====================================================================
# 171. VIDEO EDITING
# =====================================================================

Support:

trim
split
join
remove sections
scene detection
silence cleanup
pacing
transitions
zoom
crop
stabilization
speed
color
audio
denoise
subtitles
Sinhala subtitles
mixed-language subtitles
music
SFX
intro
outro
titles
lower thirds
logo
B-roll
aspect ratios
thumbnail
highlights
shorts
batch exports


# =====================================================================
# 172. SEMANTIC VIDEO EDITING
# =====================================================================

Understand:

“Remove the boring middle.”

“Make it faster.”

“Turn this into a Short.”

“Make it cinematic.”


Do not require exact timestamps unless necessary.


# =====================================================================
# 173. STORYBOARD AGENT
# =====================================================================

For generated video:

idea
↓
script
↓
scene breakdown
↓
storyboard
↓
shot list
↓
visual style
↓
generate
↓
assemble
↓
audio
↓
captions
↓
quality check
↓
export


# =====================================================================
# 174. AUDIO STUDIO
# =====================================================================

Support:

transcription
noise reduction
silence removal
voice enhancement
EQ
compression
normalization
ducking
sync
conversion


# =====================================================================
# 175. MEDIA PROVIDER ROUTING
# =====================================================================

Select provider using:

quality
style
cost
latency
duration
resolution
privacy
availability
commercial-use requirements where known


# =====================================================================
# 176. MEDIA PRIVACY
# =====================================================================

Private owner media:

prefer local tools when practical.

Before cloud upload:

classify
minimize
apply privacy policy
use approved provider


# =====================================================================
# 177. MEDIA PROJECT MEMORY
# =====================================================================

Remember approved:

visual style
character design
environment design
camera style
color palette
aspect ratio
subtitle style
logo
intro/outro
export preferences


# =====================================================================
# 178. MEDIA QUALITY CONTROL
# =====================================================================

Before claiming complete:

file exists
file opens
resolution
duration
audio state
encoding
aspect ratio
corruption check


# =====================================================================
# 179. CODING / SOFTWARE FACTORY
# =====================================================================

Support:

architecture
frontend
backend
database
APIs
coding
editing
debugging
testing
refactoring
docs
dependencies
build
package
release
Git
CI/CD
deployment
security
performance


# =====================================================================
# 180. AUTONOMOUS DEBUGGING
# =====================================================================

CAPTURE
↓
REPRODUCE
↓
LOG
↓
FORM HYPOTHESIS
↓
TEST
↓
FIX
↓
REGRESSION TEST
↓
VERIFY


# =====================================================================
# 181. BUG REPRODUCTION AGENT
# =====================================================================

Convert vague report into:

reproduction steps
expected behavior
actual behavior
environment
logs
failing test where possible


# =====================================================================
# 182. CODE REVIEW
# =====================================================================

Important code:

Author
≠
Reviewer
≠
Tester


where feasible.


# =====================================================================
# 183. PERFORMANCE PROFILING
# =====================================================================

Measure:

CPU
memory
startup
database
network
API latency
UI responsiveness


# =====================================================================
# 184. WEBSITE FACTORY
# =====================================================================

Owner:

“Make this website.”

NOVA may handle:

requirements
design
frontend
backend
database
auth
testing
QA
deployment
verification


# =====================================================================
# 185. DEPLOYMENT VERIFICATION
# =====================================================================

Check:

reachable endpoint
routes
errors
basic functional health


# =====================================================================
# 186. DEPLOYMENT ROLLBACK
# =====================================================================

Bad deployment:

restore last known good version when policy allows.


# =====================================================================
# 187. CODEBASE KNOWLEDGE GRAPH
# =====================================================================

Map:

modules
classes
functions
APIs
tests
features
dependencies


# =====================================================================
# 188. DEPENDENCY INTELLIGENCE
# =====================================================================

Track:

deprecations
breaking changes
compatibility
security issues


# =====================================================================
# 189. AUTOMATIC MIGRATION AGENT
# =====================================================================

When safe:

research replacement
create branch
migrate
test
verify
document


# =====================================================================
# 190. GAME DEVELOPMENT STUDIO
# =====================================================================

Support:

Game Director
Producer
Game Designer
Story
Worldbuilding
Gameplay Coding
NPC AI
UI
Level Design
3D
Character
Environment
Animation
VFX
Audio
Music
QA
Performance
Build
Localization


# =====================================================================
# 191. GAME PIPELINE
# =====================================================================

requirements
↓
vision
↓
GDD
↓
story/world bible
↓
architecture
↓
prototype
↓
vertical slice
↓
gameplay
↓
AI
↓
world
↓
assets
↓
UI
↓
audio
↓
QA
↓
optimization
↓
build
↓
milestones


# =====================================================================
# 192. GAME ENGINE ADAPTERS
# =====================================================================

Unreal Engine
Unity
Godot


Remain extensible.


# =====================================================================
# 193. GAME PROJECT MEMORY
# =====================================================================

Persist:

design decisions
story
characters
lore
quests
levels
mechanics
code
assets
bugs
tests
builds
milestones
performance


# =====================================================================
# 194. SEMANTIC GAME EDITING
# =====================================================================

Example:

“Enemy AI too easy.”

NOVA should:

inspect relevant system
identify behavior
modify safely
build
test
playtest
compare


# =====================================================================
# 195. AUTOMATED GAME QA
# =====================================================================

Support:

launch tests
repeatable inputs
crash detection
UI checks
save/load
performance regression
build verification


# =====================================================================
# 196. NPC SIMULATION
# =====================================================================

Possible architecture:

behavior states
memory
relationships
schedules
reputation
dialog context


# =====================================================================
# 197. WORLD CONSISTENCY CHECKER
# =====================================================================

Detect contradictions across:

lore
timeline
quests
characters
locations


# =====================================================================
# 198. 3D STUDIO
# =====================================================================

Support:

Blender
modeling
editing
topology
UV
materials
textures
rigging
animation
lighting
camera
render
LOD
export
architectural visualization


# =====================================================================
# 199. SEMANTIC 3D EDITING
# =====================================================================

Example:

“Make this room brighter and more modern.”

NOVA:

inspect scene
understand context
plan
modify
render preview
verify


# =====================================================================
# 200. 3D ASSET LIBRARY
# =====================================================================

Track:

asset
project
polycount
materials
textures
format
license
last use


# =====================================================================
# 201. 3D SCENE OPTIMIZER
# =====================================================================

Detect:

duplicate meshes
heavy assets
unused materials
unused textures
performance issues


# =====================================================================
# 202. ARCHITECTURE VISUALIZATION
# =====================================================================

2D plan
↓
dimensions
↓
blockout
↓
walls/openings
↓
materials
↓
lighting
↓
camera
↓
render


Do not silently invent critical dimensions.


# =====================================================================
# 203. EDUCATION AGENT
# =====================================================================

Support:

Study Planner
Weak Topic Agent
Revision Agent
Practice Agent
Mock Exam Agent
Target Paper Agent
Answer Reviewer


# =====================================================================
# 204. O/L TARGET PAPER
# =====================================================================

Reference source paper:

analyze structure
topics
skills
difficulty


Generate ORIGINAL practice material.

Do not copy copyrighted questions unnecessarily.


# =====================================================================
# 205. EDUCATION KNOWLEDGE GRAPH
# =====================================================================

subject
unit
topic
concept
prerequisite
strength
weakness
practice history


# =====================================================================
# 206. ADAPTIVE LEARNING
# =====================================================================

Use:

mistake patterns
weak topics
past answers
difficulty history


Avoid unhealthy score pressure.


# =====================================================================
# 207. SMART HOME WORLD MODEL
# =====================================================================

Represent:

room
device
type
protocol
capabilities
state
permissions
health


# =====================================================================
# 208. DEVICE STATE RECONCILIATION
# =====================================================================

Command sent
≠
success.


Verify state where supported.


# =====================================================================
# 209. EVENT-DRIVEN AUTONOMY
# =====================================================================

Approved events may trigger missions.

Examples:

file changed
build failed
device offline
backup failed
Windows update available
disk almost full
deadline approaching
email arrived
render completed


Respect owner policies.


# =====================================================================
# 210. NATURAL AUTOMATION COMPILER
# =====================================================================

Owner:

“When I say Study Mode,
open my school folder,
browser,
focus music,
and enable DND.”


Compile safe workflow.


# =====================================================================
# 211. WORKFLOW LEARNING
# =====================================================================

For repeated owner workflows:

observe
generalize
simulate
test
suggest
owner approves
register


# =====================================================================
# 212. SHADOW MODE
# =====================================================================

Before trusting newly learned automation:

predict actions without executing
compare with actual owner behavior
build confidence


# =====================================================================
# 213. WORKFLOW VERSIONING
# =====================================================================

Keep history and rollback.


# =====================================================================
# 214. WORKFLOW DRY RUN
# =====================================================================

Allow simulation before real action.


# =====================================================================
# 215. UNIVERSAL DATA FABRIC
# =====================================================================

Unify references across:

files
projects
messages
calendar
browser
devices
missions
memories
media
tools
APIs
artifacts


Do not build isolated data silos.


# =====================================================================
# 216. CROSS-APP CONTEXT
# =====================================================================

Example:

“Use the attachment from that email,
update the Excel sheet,
then refresh the presentation.”


NOVA should link context across apps.


# =====================================================================
# 217. OWNER IDENTITY & TRUST
# =====================================================================

Support:

OWNER
TRUSTED_FAMILY
LIMITED_USER
GUEST


Sensitive operations require appropriate authority.


# =====================================================================
# 218. OWNER AUTHENTICATION
# =====================================================================

For high-impact actions optionally support:

Windows identity
passkey
PIN
device confirmation
biometric through supported OS APIs


# =====================================================================
# 219. POLICY ENGINE
# =====================================================================

Natural rules:

“Never delete my photos.”

“Don't send private files to cloud.”

“Use PC 2 for renders.”

“Don't restart gaming PC while I'm playing.”

“Ask before spending.”

“Night eke backup run karanna.”


Compile into enforceable policy.


# =====================================================================
# 220. POLICY VERSIONING
# =====================================================================

Store:

policy
scope
source
version
date


# =====================================================================
# 221. POLICY CONFLICT DETECTION
# =====================================================================

Detect conflicting owner instructions.

Ask only when needed.


# =====================================================================
# 222. POLICY SIMULATOR
# =====================================================================

Before applying major policy:

show what workflows/devices may be affected.


# =====================================================================
# 223. PERMISSION MODEL
# =====================================================================

ALLOW
DENY
ASK
ALLOW_ONCE
SESSION
PROJECT
MISSION
DEVICE
APP
FOLDER
CONTACT
DOMAIN
READ_ONLY
SANDBOX


# =====================================================================
# 224. TEMPORARY PERMISSION LEASE
# =====================================================================

Support:

one action
this mission
this session
until time/date


# =====================================================================
# 225. RISK ENGINE
# =====================================================================

Evaluate:

reversibility
financial impact
privacy
security
external effect
confidence
sensitivity


Levels:

LOW
MEDIUM
HIGH
CRITICAL


# =====================================================================
# 226. DEFAULT RISK POLICY
# =====================================================================

AUTO:
safe reversible local work

AUTO + VERIFY:
coding
research
ordinary files
renders
normal app control

ASK:
payment
permanent deletion
major account/security changes
sensitive public/external action

VAULT:
secrets

REFUSE/REDIRECT:
unsafe or illegal actions


# =====================================================================
# 227. PRIVACY CLASSES
# =====================================================================

PUBLIC
INTERNAL
PERSONAL
PRIVATE
SECRET
CREDENTIAL
SYSTEM_SENSITIVE
SECURITY_SENSITIVE
THIRD_PARTY_PRIVATE


# =====================================================================
# 228. PRIVACY ROUTER
# =====================================================================

Before sending data outside machine:

identify destination
identify required data
classify
minimize
redact
apply owner policy
send only allowed context


# =====================================================================
# 229. LOCAL-ONLY MODE
# =====================================================================

Owner:

“Nova private mode.”


Enable:

zero/limited cloud data egress
local tools/models preferred
private tasks stay local


# =====================================================================
# 230. DATA EGRESS LEDGER
# =====================================================================

Record:

provider
time
mission
data category
reason


Do not log raw secrets.


# =====================================================================
# 231. ONE-COMMAND LOCKDOWN
# =====================================================================

Owner:

“Nova lockdown.”


Pause:

external sends
payments
remote device actions
high-risk automations
background high-impact missions


without corrupting state.


# =====================================================================
# 232. SECRETS VAULT
# =====================================================================

Secrets include:

OpenAI key
Gemini key
other API keys
OAuth tokens
device credentials
Wi-Fi credentials
encryption keys


Agents should use credential handles where possible.

Do not expose raw secrets to all sub-agents.


# =====================================================================
# 233. SECRET SCANNER
# =====================================================================

Before:

Git commit
release
deployment
cloud backup


scan for credentials.


# =====================================================================
# 234. PROMPT-INJECTION PROTECTION
# =====================================================================

No:

webpage
email
document
PDF
plugin
agent
API response
generated code


may override NOVA system policies.


# =====================================================================
# 235. DEFENSIVE SECURITY ONLY
# =====================================================================

Security features may support:

owner-owned systems
authorized systems
training labs
CTFs


Allowed:

secure configuration
dependency scanning
patch review
secret scanning
log analysis
file integrity
authorized network inventory
security reports
remediation
backup verification


Do not enable:

unauthorized intrusion
credential theft
malware
ransomware
stealth persistence
destructive attacks
account takeover
unauthorized surveillance


# =====================================================================
# 236. ACTION RECEIPTS
# =====================================================================

Important action records:

request
mission
agent
target
tool
device
before-state if useful
after-state
external effect
verification
rollback


# =====================================================================
# 237. SIDE-EFFECT LEDGER
# =====================================================================

Track separately:

email
message
payment
order
calendar
deployment
device change
account change


# =====================================================================
# 238. HALLUCINATION FIREWALL
# =====================================================================

Model text is NEVER proof that an action succeeded.


Proof must come from:

filesystem
API result
window/process
browser state
device state
tool result
visual verification


# =====================================================================
# 239. NATURAL UNDO
# =====================================================================

Owner:

“Undo that.”


Find latest relevant reversible operation and restore safely.


# =====================================================================
# 240. SIMULATION SANDBOX
# =====================================================================

Risky changes should be testable in isolation:

dependency upgrade
configuration migration
new skill
automation workflow
deployment
generated code
plugin


# =====================================================================
# 241. DIGITAL TWIN / TEST ENVIRONMENT
# =====================================================================

Where practical:

clone relevant state
simulate change
evaluate
then apply to production


# =====================================================================
# 242. RECOVERY ENGINE
# =====================================================================

failure
↓
classify
↓
retry
↓
alternate tool/provider/device
↓
rollback
↓
restore checkpoint
↓
continue unrelated tasks
↓
escalate only when necessary


# =====================================================================
# 243. SELF-HEALING
# =====================================================================

May safely:

restart component
reconnect provider
refresh cache
rebuild index
restart worker
switch provider
restore config
rollback bad update


# =====================================================================
# 244. INTEGRATION DRIFT REPAIR
# =====================================================================

Detect:

API version change
browser selector change
expired auth
library update
path change
app UI change


Create repair mission.


# =====================================================================
# 245. CIRCUIT BREAKERS
# =====================================================================

Repeated failure:

temporarily disable unstable integration.

Do not infinite-loop.


# =====================================================================
# 246. CRASH / REBOOT RECOVERY
# =====================================================================

Persist:

mission
tasks
external effects
device jobs
workspace
project checkpoint


After restart:

verify uncertain actions
resume safe work


# =====================================================================
# 247. SAFE MODE
# =====================================================================

Safe Mode:

core only
third-party plugins disabled
automations paused
remote actions paused
diagnostics available


# =====================================================================
# 248. BACKUP ENGINE
# =====================================================================

Back up:

config
memory
missions
policies
permissions
skill manifests
project metadata
automation definitions


# =====================================================================
# 249. RESTORE ENGINE
# =====================================================================

Support:

full restore
settings restore
memory restore
project metadata restore


# =====================================================================
# 250. RESTORE DRILL
# =====================================================================

Periodically verify backups are actually readable/restorable.


# =====================================================================
# 251. INCIDENT MODE
# =====================================================================

Serious failure:

freeze risky operations
preserve safe diagnostics
backup
diagnose
recover
postmortem


# =====================================================================
# 252. AUTOMATIC POSTMORTEM
# =====================================================================

Record:

failure
root cause
impact
fix
prevention
tests added


# =====================================================================
# 253. SELF-TEST LAB
# =====================================================================

Owner:

“Nova check yourself.”


Test:

Core
database
memory
mission system
OpenAI provider
Gemini provider
voice
vision
browser
app launcher
files
device mesh
security agent
scheduler
recovery


# =====================================================================
# 254. NIGHTLY CAPABILITY TESTS
# =====================================================================

Optional synthetic health tests.

Detect regressions.


# =====================================================================
# 255. REGRESSION DETECTOR
# =====================================================================

Example:

Gemini launch worked yesterday.
Fails today.

NOVA should compare:

recent code
app changes
Windows changes
path changes
browser state


Then repair/rollback where safe.


# =====================================================================
# 256. CAPABILITY HEALTH MAP
# =====================================================================

NOVA must know what is:

STABLE
WORKING
PARTIAL
DEGRADED
BROKEN
MISSING


# =====================================================================
# 257. “WHAT CAN YOU DO?” MUST BE DYNAMIC
# =====================================================================

Do not show static marketing list.

NOVA should inspect:

providers
devices
skills
tools
permissions
health


and answer truthfully.


# =====================================================================
# 258. OBSERVABILITY
# =====================================================================

Track:

mission
agents
tools
providers
devices
errors
retries
cost
permissions
privacy
resources


Do not log secrets.


# =====================================================================
# 259. TRACE IDS
# =====================================================================

Use trace IDs for complex missions.


# =====================================================================
# 260. COST GOVERNOR
# =====================================================================

Track:

per mission
per project
provider
daily
weekly
monthly


Allow:

warning limit
soft limit
hard limit


# =====================================================================
# 261. RESOURCE MANAGER
# =====================================================================

Monitor:

CPU
GPU
RAM
disk
network
battery
temperature


# =====================================================================
# 262. COMPUTE SCHEDULER
# =====================================================================

Schedule:

renders
game builds
video jobs
local models
tests


based on:

node availability
owner activity
night schedule
temperature
power
network


# =====================================================================
# 263. PROJECT MODEL
# =====================================================================

Each project:

project_id
name
goal
constraints
folder
repository
milestones
missions
memory namespace
risks
decisions
tasks
artifacts
health


# =====================================================================
# 264. PROJECT HEALTH
# =====================================================================

Track:

progress
bugs
tests
docs
security
performance
dependencies
technical debt
milestones


# =====================================================================
# 265. PROJECT HEALTH FORECAST
# =====================================================================

Estimate:

deadline risk
blocked work
resource risk
technical debt growth


# =====================================================================
# 266. DECISION MEMORY
# =====================================================================

Store:

decision
reason
alternatives
date
impact


# =====================================================================
# 267. DECISION DEBT
# =====================================================================

Track unresolved decisions that block work.


# =====================================================================
# 268. TECHNICAL DEBT
# =====================================================================

Classify:

urgent
important
later
cosmetic


# =====================================================================
# 269. PROACTIVE MAINTENANCE WINDOW
# =====================================================================

Optional owner-defined time for:

backups
index maintenance
health checks
integration tests
safe updates
cleanup analysis
provider tests
node tests


# =====================================================================
# 270. UPDATE MANAGER
# =====================================================================

Support controlled updates for:

NOVA Core
skills
plugins
providers
device nodes
models


Use:

backup
staging
test
canary
rollback


# =====================================================================
# 271. COMPATIBILITY MANAGER
# =====================================================================

Detect changes in:

Windows
Python/runtime
desktop framework
browser
device APIs
third-party services
libraries


# =====================================================================
# 272. RELEASE ORCHESTRATOR
# =====================================================================

Build
↓
tests
↓
security checks
↓
privacy checks
↓
package
↓
staging
↓
release
↓
monitor
↓
rollback if needed


# =====================================================================
# 273. REPRODUCIBLE BUILDS
# =====================================================================

Track:

dependencies
versions
environment
config
build inputs


# =====================================================================
# 274. DESKTOP UI
# =====================================================================

UI must remain SIMPLE despite powerful backend.


Primary sidebar:

Chat
Voice
Projects
Memory
Settings


Bottom:

small Appearance control
Emergency Stop


Do not permanently expose in primary nav:

Home
Missions
Agents
Automations
Tools
Integrations
Devices
Privacy


Those may exist inside:

Settings → Advanced / Connections


# =====================================================================
# 275. DEFAULT LAUNCH
# =====================================================================

Open directly to Chat.


Home empty-state is merged into Chat.


# =====================================================================
# 276. REMOVE OLD CLUTTER
# =====================================================================

Remove normal-user UI:

YOUR SPACE, INTELLIGENTLY CONNECTED
NOVA / Home breadcrumb
large Home cards
View Missions
Explore Memory
Privacy Controls
Expand Navigation
large Privacy & Language sidebar item
developer diagnostics
/help instructions


# =====================================================================
# 277. UI VISUAL STYLE
# =====================================================================

Default theme:

PEARL ICE


Use:

soft pearl-white
pale blue-grey background
semi-transparent cool-white glass
deep slate-blue text
restrained ice-blue/cyan glow
soft shadows
subtle depth


Avoid:

glaring pure white
black-heavy design
grey admin dashboard
cyberpunk
RGB neon
purple-heavy style


# =====================================================================
# 278. NOVA ORB
# =====================================================================

Original central NOVA orb.

States:

IDLE
LISTENING
THINKING
WORKING
SPEAKING
SUCCESS
WARNING
ERROR
PRIVACY
OFFLINE


# =====================================================================
# 279. DYNAMIC GREETING
# =====================================================================

Based on local system time:

Good morning
Good afternoon
Good evening
Good night


Natural Sinhala equivalents allowed depending language context.


# =====================================================================
# 280. CHAT / VOICE SWITCH
# =====================================================================

Simple segmented control:

CHAT | VOICE


# =====================================================================
# 281. CHAT EMPTY STATE
# =====================================================================

Show:

NOVA orb
dynamic greeting
short subtitle
composer


No technical panels.


# =====================================================================
# 282. MESSAGE BUBBLES
# =====================================================================

Owner:

right-aligned
compact
accent glass


NOVA:

left-aligned
neutral glass
small NOVA mark


No giant cards for “hi”.


# =====================================================================
# 283. COMPOSER
# =====================================================================

Floating frosted capsule:

[ + ] [ Message NOVA… ] [ mic ] [ send ]


Attachment options where supported:

File
Image
Video
Document
Folder
Screenshot


# =====================================================================
# 284. VOICE SCREEN
# =====================================================================

Mostly:

large orb
Listening…
Thinking…
Working…
Speaking…


Optional:

small transcript
mute


No giant “disconnected” dashboard.


If unavailable:

“Voice unavailable”
+ small setup action.


# =====================================================================
# 285. APPEARANCE
# =====================================================================

Support:

Ice Blue
Soft Cyan
Ocean Blue
Silver
Soft Lavender
Soft Mint


Accent only.

Persist selection.


# =====================================================================
# 286. SETTINGS
# =====================================================================

General
Appearance
Voice
Language
AI
Privacy
Memory
Permissions
Connections
Advanced


# =====================================================================
# 287. CONNECTIONS
# =====================================================================

Inside Settings → Connections:

AI Providers
Devices
Smart Home
Cameras
Email
Calendar
Messaging
Browser
Storage
Developer Integrations


# =====================================================================
# 288. ADD DEVICE WIZARD
# =====================================================================

Step 1:
What are you adding?

Computer
Phone
AC
Light
Camera
TV
Speaker
Home Assistant
Matter Device
MQTT Device
IR Device
Other


Step 2:
Discover connection method.


Step 3:
Authenticate/pair.


Step 4:
Select permissions.


Step 5:
Test read-only state.


Step 6:
Test safe command.


Step 7:
Register capabilities.


# =====================================================================
# 289. PROVIDER SETUP WIZARD
# =====================================================================

Initial recommended options:

OpenAI GPT
Google Gemini


Display:

Connect OpenAI
Connect Gemini


On selection:

show local secure API-key entry field.


Never ask user to paste key into Codex conversation.


# =====================================================================
# 290. PROVIDER STATUS
# =====================================================================

Show:

CONNECTED
DISCONNECTED
DEGRADED
AUTH EXPIRED
RATE LIMITED


# =====================================================================
# 291. NO DEAD BUTTONS
# =====================================================================

Every button:

works

or clearly states:

Not connected
Disabled
Coming soon
Unavailable


# =====================================================================
# 292. SYSTEM TRAY
# =====================================================================

Open NOVA
Mute Voice
Pause Autonomous Work
Privacy Mode
Emergency Stop
Exit


# =====================================================================
# 293. QUICK OVERLAY
# =====================================================================

Optional global hotkey:

small orb
text input
mic
close


# =====================================================================
# 294. CONTEXT-AWARE UI
# =====================================================================

Voice:
minimal orb.

Coding:
show project context only if useful.

3D:
show relevant mission progress.

Normal:
hide complexity.


# =====================================================================
# 295. INVISIBLE COMPLEXITY
# =====================================================================

As NOVA gets more powerful,
the owner UI should become simpler.


# =====================================================================
# 296. MORNING REPORT
# =====================================================================

Report:

completed
partial
failed
blocked
decisions needed
important artifacts
important costs/issues


Keep concise.


# =====================================================================
# 297. EXECUTIVE MODE
# =====================================================================

Routine approved work happens quietly.

Surface only:

important approval
failure
major result
completion


# =====================================================================
# 298. FOCUS MODE
# =====================================================================

May:

open project
enable DND
reduce notifications
open required apps
play configured focus audio


# =====================================================================
# 299. NATURAL AUDIT
# =====================================================================

Owner can ask:

“What did you do last night?”

“What changed?”

“What data left my PC?”

“Why did you do that?”

“Which PC ran the render?”


Provide evidence-based concise answer.


# =====================================================================
# 300. EXPLAINABILITY
# =====================================================================

Provide:

goal
short reason
policy involved
evidence
result


Do not expose private hidden chain-of-thought.


# =====================================================================
# 301. PERSONAL AI CONSTITUTION
# =====================================================================

Maintain a human-readable owner policy document including:

privacy defaults
autonomy level
spending rules
device rules
communication rules
security boundaries
preferred language
project preferences
update rules
night-work rules


# =====================================================================
# 302. FUTURE-PROOF PROVIDER ARCHITECTURE
# =====================================================================

Adding a future provider should require:

adapter
capability declaration
auth handler
tests


NOT NOVA Core rewrite.


# =====================================================================
# 303. FUTURE-PROOF DEVICE ARCHITECTURE
# =====================================================================

Adding future:

AC
camera
robot
sensor
home appliance
computer
phone
wearable


should require a device adapter and permissions,
not architectural rewrite.


# =====================================================================
# 304. FUTURE-PROOF APP ARCHITECTURE
# =====================================================================

Implement App Driver interface.

Possible driver capabilities:

launch
close
focus
read state
execute action
export
import
query
verify


App-specific driver if available.

Fallback to:

UI Automation
vision
keyboard/mouse


# =====================================================================
# 305. AUTONOMOUS APP LEARNING
# =====================================================================

When allowed:

observe owner workflow
identify semantic actions
generalize
sandbox
test
offer automation


Do not silently record sensitive workflows.


# =====================================================================
# 306. PRINT / SCAN / PERIPHERAL AGENT
# =====================================================================

Future support:

printers
scanners
webcams
microphones
external drives
USB peripherals


via authorized drivers/APIs.


# =====================================================================
# 307. STORAGE INTELLIGENCE
# =====================================================================

Analyze:

duplicate files
large files
temporary project caches
render leftovers
backup status
disk pressure


Do not auto-delete important data.


# =====================================================================
# 308. NETWORK DEVICE HEALTH
# =====================================================================

For authorized/persistently paired local devices:

health
availability
latency
service status


No unauthorized probing/control.


# =====================================================================
# 309. ADAPTIVE AUTONOMY
# =====================================================================

If a specific workflow succeeds repeatedly:

confidence may increase.


If failures rise:

reduce autonomy
increase verification
possibly request approval


# =====================================================================
# 310. TOOL / SKILL RETIREMENT
# =====================================================================

Broken/deprecated skill:

mark degraded
attempt repair
find replacement
test migration
disable unsafe version


# =====================================================================
# 311. SKILL VERSIONING
# =====================================================================

Example:

AC_Control 1.0
AC_Control 1.1
AC_Control 2.0


Keep last known good version until replacement verified.


# =====================================================================
# 312. TOOL SELF-DISCOVERY
# =====================================================================

Discover available:

CLI
SDK
application API
MCP
plugins
browser capabilities
local binaries
device APIs


within authorization.


# =====================================================================
# 313. AUTONOMOUS ENVIRONMENT BOOTSTRAP
# =====================================================================

For safe project work, NOVA may prepare:

dependencies
virtual environment
build tools
project setup
test environment


Avoid unsafe arbitrary installers.


# =====================================================================
# 314. LOCAL KNOWLEDGE GRAPH
# =====================================================================

Connect:

projects
documents
files
code
decisions
research
artifacts
tasks
people
devices


# =====================================================================
# 315. SEMANTIC TIMELINE
# =====================================================================

Support:

“What changed in this project this week?”

“When did this bug start?”

“What did we decide last month?”


# =====================================================================
# 316. CHANGE INTELLIGENCE
# =====================================================================

Detect meaningful changes in:

repository
configuration
device state
project files
integration health


# =====================================================================
# 317. ROOT-CAUSE ANALYSIS
# =====================================================================

Do not only patch symptom.

Where possible:

identify cause
fix cause
add regression test
document prevention


# =====================================================================
# 318. EXECUTION LEDGER
# =====================================================================

Keep event-sourced record of important execution state.

Useful for:

undo
audit
recovery
reboot continuation
duplicate prevention


# =====================================================================
# 319. PERSONALIZATION
# =====================================================================

Remember approved preferences for:

music
food
apps
games
movies
document style
presentation style
language
verbosity
workflows
folders
creative style
devices


Do not treat secrets as normal preference memory.


# =====================================================================
# 320. PERSONALITY
# =====================================================================

NOVA should be:

friendly
smart
calm
natural
efficient
not overly talkative
occasionally humorous when appropriate


Do not pretend human consciousness or genuine human emotions.


# =====================================================================
# 321. RESPONSE LENGTH
# =====================================================================

Busy/command context:
short.

Explanation requested:
detailed.

Do not narrate internal technical work unnecessarily.


# =====================================================================
# 322. OWNER EXPERIENCE EXAMPLES
# =====================================================================

Examples are NOT limits.


“Nova, open Gemini.”

“Nova, me PC eka patta slow. Balala hadanna.”

“Nova, virus ekakda kiyala check karanna.”

“Nova, PC 2 ekath scan karanna.”

“Nova, Windows update thiyanawada?”

“Nova, render machine eke Blender job eka run karanna.”

“Nova, me image eka cinematic karanna.”

“Nova, futuristic city image ekak hadanna.”

“Nova, eka animate karala trailer shot ekak hadanna.”

“Nova, continue our game.”

“Nova, website eka finish karala deploy karanna.”

“Nova, me error eka balala fix karanna.”

“Nova, mage presentation eka update karanna.”

“Nova, AC eka on karala 25 danna.”

“Nova, front camera eka online da balanna.”

“Nova, ara file eka anith PC ekata yawanna.”

“Nova, mama nidagannawa. Me tasks tika finish karanna.”

“Nova, private mode.”

“Nova, lockdown.”

“Nova, undo that.”

“Nova, check yourself.”

“Nova, fix yourself.”

“Nova, me capability eka nathnam add karaganna.”


# =====================================================================
# 323. END-TO-END TEST — LANGUAGE
# =====================================================================

Test:

Sinhala script
Singlish
English
mixed Sinhala-English
slang
corrections
language switching


Response language should follow owner style appropriately.


# =====================================================================
# 324. END-TO-END TEST — WAKE WORD
# =====================================================================

Verify:

Nova wake word
speech capture
intent
action
reply
return to listening


# =====================================================================
# 325. END-TO-END TEST — OPEN APP
# =====================================================================

Test:

open Notepad
open Calculator
open Chrome
open YouTube
open Gemini


Must work without cloud LLM.


# =====================================================================
# 326. END-TO-END TEST — PROVIDERS
# =====================================================================

With owner-provided secure keys:

OpenAI connection
Gemini connection
health status
routing
fallback


Keys must not appear in logs.


# =====================================================================
# 327. END-TO-END TEST — COMPUTER VISION
# =====================================================================

Test:

screen capture
app identification
button detection
dialog interpretation
simple form
error screen
post-action visual verification


# =====================================================================
# 328. END-TO-END TEST — VOICE
# =====================================================================

Enter Voice
→ auto-listen
→ speak mixed Sinhala-English
→ transcribe
→ understand
→ act/respond
→ TTS
→ return to listening


Exit Voice:
microphone stops.


# =====================================================================
# 329. END-TO-END TEST — MISSION
# =====================================================================

Create multi-step task.

Interrupt application.

Restart.

Recover.

No duplicate side effects.


# =====================================================================
# 330. END-TO-END TEST — MEMORY
# =====================================================================

Remember preference.

Retrieve later.

Correct preference.

New explicit owner correction wins.


# =====================================================================
# 331. END-TO-END TEST — MULTI-PC
# =====================================================================

Pair second PC.

Verify:

identity
heartbeat
capability discovery
safe remote action
render/task dispatch
file transfer
revocation


Unpaired device must fail.


# =====================================================================
# 332. END-TO-END TEST — WINDOWS UPDATE
# =====================================================================

Check state
prepare update
respect active work
install where safe
reboot policy
reconnect
verify


# =====================================================================
# 333. END-TO-END TEST — SECURITY SCAN
# =====================================================================

Use trusted scanner.

Verify:

definitions
scan execution
result
quarantine/remediation where safe
re-scan
truthful report


# =====================================================================
# 334. END-TO-END TEST — AC / DEVICE
# =====================================================================

If test device available:

pair
read state
issue safe command
verify state


If unsupported:

trigger capability-gap flow.


# =====================================================================
# 335. END-TO-END TEST — CCTV
# =====================================================================

Authorized test camera:

connect
health state
event read
privacy settings
disconnect/revoke


# =====================================================================
# 336. END-TO-END TEST — IMAGE GENERATION
# =====================================================================

Generate image using configured provider.

Verify artifact.

Register in project.


# =====================================================================
# 337. END-TO-END TEST — VIDEO GENERATION
# =====================================================================

Generate short video where provider available.

Verify:

file
duration
playback
artifact registration


# =====================================================================
# 338. END-TO-END TEST — OFFICE
# =====================================================================

Create real:

PPTX
XLSX


Verify both open.


# =====================================================================
# 339. END-TO-END TEST — CAPABILITY COMPOSITION
# =====================================================================

Request:

“Edit these photos,
create a presentation,
save it,
prepare an email.”


Must combine capabilities dynamically.


# =====================================================================
# 340. END-TO-END TEST — CAPABILITY GAP
# =====================================================================

Request unsupported safe test capability.

Expected:

detect missing capability
explain briefly
ask owner permission
build/configure in isolation
test
register
resume original request


# =====================================================================
# 341. END-TO-END TEST — GENERALIZATION
# =====================================================================

Equivalent intents:

“Open Gemini.”
“Gemini eka open karanna.”
“Launch Gemini.”
“Gemini arinna ban.”


Should map to same semantic capability.


# =====================================================================
# 342. END-TO-END TEST — RECOVERY
# =====================================================================

Intentionally fail provider/tool.

Verify:

retry
fallback
state preservation
no fake completion


# =====================================================================
# 343. END-TO-END TEST — SECURITY
# =====================================================================

Verify:

no secrets in logs
unpaired node denied
prompt injection ignored
permanent deletion protected
Emergency Stop works
skill permissions constrained


# =====================================================================
# 344. UI ACCEPTANCE
# =====================================================================

Verify:

simple sidebar
Chat
Voice
Projects
Memory
Settings
one Emergency Stop
dynamic greeting
NOVA orb
Pearl Ice appearance
compact bubbles
clean composer
no terminal window
Sinhala Unicode
responsive layout


Test:

1366x768
1920x1080
2560x1440


# =====================================================================
# 345. IMPLEMENTATION PRIORITY
# =====================================================================

DO NOT BUILD ADVANCED FLASHY FEATURES WHILE CORE EXECUTION IS FAKE.


P0:
repository audit
run current app
stabilize tests
remove critical breakage

P1:
real local Windows command router

P2:
general application resolver

P3:
secure OpenAI + Gemini Provider Hub

P4:
real model routing + provider health/fallback

P5:
Computer Vision gateway
screen understanding
visual verification

P6:
real Voice pipeline
wake word architecture
auto-listen
Sinhala/mixed-language handling

P7:
premium simplified UI
remove technical clutter
no visible terminal

P8:
persistent Mission Engine
durable worker system
checkpoints

P9:
Memory + World Model
project continuation
semantic search

P10:
Verification Engine
Hallucination Firewall
Action Receipts

P11:
Recovery Engine
rollback
crash/reboot continuation

P12:
Browser Agent

P13:
Files + Office

P14:
Device Mesh foundation

P15:
second-PC production-quality test node

P16:
Windows Update + Endpoint Security Agent

P17:
Generic Device Adapter SDK
Add Device wizard

P18:
AC / Smart Home adapters

P19:
Authorized CCTV adapters

P20:
Image Studio
image generation
image editing

P21:
Video Studio
video generation
video editing

P22:
Communication
email
calendar
messaging
calling architecture

P23:
Skill Factory
owner-approved self-expansion

P24:
Autonomous App Learning
Event-Driven Autonomy

P25:
Game / 3D

P26:
Education

P27:
Predictive autonomy
long-horizon optimization
advanced self-maintenance


# =====================================================================
# 346. FOUNDATION BEFORE EXPANSION
# =====================================================================

The highest-value shared infrastructure is:

Capability Registry
Mission Engine
Provider Hub
Tool Gateway
Vision Gateway
Voice Gateway
Memory
World Model
Permission Engine
Policy Engine
Privacy Router
Secrets Vault
Device Mesh
Verification Engine
Recovery Engine
Skill Factory


Build these as reusable foundations.


# =====================================================================
# 347. CONTINUOUS DEVELOPMENT LOOP
# =====================================================================

For each vertical slice:

inspect
↓
implement
↓
run
↓
test
↓
fix
↓
retest
↓
verify
↓
update requirement matrix
↓
update PROJECT_STATUS
↓
checkpoint/commit
↓
select next dependency-ready feature
↓
continue


DO NOT stop after every normal milestone to ask owner what to do next.


# =====================================================================
# 348. WHEN TO ASK OWNER
# =====================================================================

Ask only for things you genuinely cannot safely infer or perform.


Examples:

API provider credential entry
OAuth login
device pairing code
physical button press
financial approval
permanent deletion approval
major security-policy change
ambiguous high-impact target


Do not ask:

which Python file to edit
which framework function to use
how to fix imports
how to structure agent code
how to resolve ordinary bugs


# =====================================================================
# 349. INITIAL API ONBOARDING
# =====================================================================

The owner intends to use TWO primary cloud AI providers:

1. OpenAI GPT
2. Google Gemini


Do not repeatedly ask which providers after this is known.

Implement both provider adapters.


When real credentials are required:

DO NOT request keys inside Codex chat.


Instead:

1. finish secure provider UI
2. run NOVA
3. display local setup screen
4. ask owner to paste new valid keys into the secure local fields
5. store via Secrets Vault
6. test each provider
7. never expose keys afterward


# =====================================================================
# 350. API KEY SAFETY
# =====================================================================

If any API key was ever shared publicly, in a chat, repository,
screenshot, log or prompt:

treat it as potentially exposed.

Do not reuse it automatically.

Tell owner to revoke/rotate and use a new key locally.


# =====================================================================
# 351. DEVELOPMENT WITHOUT REAL KEYS
# =====================================================================

Do not block all engineering while waiting for keys.

Build:

provider interfaces
secure storage
settings UI
connection tests
mocked unit tests
routing tests


When keys become available:

perform live integration tests.


# =====================================================================
# 352. NO PROVIDER DEPENDENCY FOR LOCAL PC ACTIONS
# =====================================================================

Commands such as:

open Chrome
open YouTube
open Gemini
open folder
focus app
volume
simple device lookup


must not fail merely because GPT/Gemini is disconnected.


# =====================================================================
# 353. OWNER-FRIENDLY FAILURE
# =====================================================================

Do not output:

stack traces
raw HTTP errors
internal class names
provider internals


Normal response example:

“I couldn’t connect to Gemini right now.
I switched to GPT and continued.”


Technical details remain in Advanced diagnostics.


# =====================================================================
# 354. OWNER-FRIENDLY CAPABILITY GAP
# =====================================================================

Example:

Owner:
“Nova AC eka on karanna.”


If unsupported:

“I don’t have control support for this AC yet.
I can add it. Want me to?”


Not:

“NotImplementedError: adapter_missing”


# =====================================================================
# 355. LONG-TERM PRODUCT PRINCIPLE
# =====================================================================

The owner may use NOVA for years.

Therefore:

do not optimize only for current APIs
do not hard-code current model names everywhere
do not hard-code device brands
do not hard-code command strings
do not assume one PC
do not assume permanent internet
do not assume one provider


Build abstraction boundaries.


# =====================================================================
# 356. NOVA ALPHA TARGET
# =====================================================================

CAN ACT.


Must have:

real local control
real providers
real Computer Vision
real basic Voice
files
browser
simple memory
simple UI


# =====================================================================
# 357. NOVA BETA TARGET
# =====================================================================

CAN FINISH.


Add:

Mission Engine
verification
recovery
durable state
project memory
Office
media


# =====================================================================
# 358. NOVA 1.0 TARGET
# =====================================================================

CAN WORK ALONE ON APPROVED PROJECTS.


Add:

overnight work
multi-agent execution
long-running goals
self-tests
Skill Factory
workflow learning


# =====================================================================
# 359. NOVA 2.0 TARGET
# =====================================================================

CAN OPERATE OWNER'S DIGITAL ENVIRONMENT.


Add:

Device Mesh
phone companion
smart home
communications
distributed compute
multi-PC automation


# =====================================================================
# 360. NOVA X TARGET
# =====================================================================

PERSONAL AI OPERATING SYSTEM.


Mature:

active perception
temporal world model
predictive planning
goal management
multi-device execution
safe self-expansion
self-healing
adaptive autonomy
simple owner UI


# =====================================================================
# 361. FINAL AUTONOMY PRINCIPLE
# =====================================================================

NOVA understands GOALS,
not memorized commands.

NOVA discovers CAPABILITIES,
not hard-coded workflows.

NOVA composes TOOLS,
not one button per task.

NOVA OBSERVES,
not blindly clicks.

NOVA VERIFIES,
not assumes.

NOVA RECOVERS,
not immediately gives up.

NOVA can BUILD SAFE NEW SKILLS
with owner approval.

NOVA remains under OWNER AUTHORITY.


# =====================================================================
# 362. FINAL SECURITY PRINCIPLE
# =====================================================================

No:

AI model
webpage
email
document
plugin
skill
agent
device
API
generated code


may override:

owner authority
permissions
privacy
security
Emergency Stop
device trust
approval boundaries


# =====================================================================
# 363. FINAL PRODUCT PRINCIPLE
# =====================================================================

BACKEND:

powerful
autonomous
multi-agent
multi-device
tool-rich
recoverable


FRONTEND:

simple
clean
human
natural
premium


The owner should not manage hundreds of systems manually.

NOVA manages them.


# =====================================================================
# 364. FINAL ENGINEERING DIRECTIVE
# =====================================================================

BEGIN REAL DEVELOPMENT NOW.


FIRST:

1. inspect the current NOVA repository
2. read AGENTS.md and current docs
3. run the current application
4. identify real working features
5. identify mocks/placeholders
6. identify broken local control
7. identify provider status
8. identify voice status
9. identify vision status
10. identify mission/memory state
11. preserve verified working code
12. create/update docs/NOVA_MASTER_SPEC.md
13. create/update requirement matrix
14. create PROJECT_STATUS
15. begin P0 → P1 → P2 → P3...


DO NOT:

stop at architecture
stop at scaffolding
stop at UI mockups
declare fake success
hard-code example commands
hard-code API keys
expose secrets
require owner to program
wait after every normal milestone
rebuild stable working modules unnecessarily


DO:

implement
integrate
run
test
fix
verify
document
checkpoint
continue


When independent work can run in parallel:

use multiple coding/review/test agents safely.


After each milestone:

RUN REAL TESTS.


If a feature cannot be finished because it requires:

credential
device
account authentication
physical pairing
owner approval


finish every dependency first,
then ask the owner only for that exact missing action.


The desired owner experience is:


OWNER:
“Nova, meka handle karanna.”


NOVA:
understands the real goal
uses context
checks memory
selects capabilities
selects agents
selects GPT/Gemini/local models as appropriate
selects local or paired computer
uses Computer Vision when required
uses Windows/app/browser/device tools
executes
observes
verifies
retries or replans
adds a missing safe capability with permission when needed
finishes
reports briefly


FINAL TARGET:


A PRIVATE,
LOCAL-FIRST,
SINHALA-FIRST,
DETECTED-LANGUAGE,
WAKE-WORD ENABLED,
VOICE-FIRST,
COMPUTER-VISION-AWARE,
WINDOWS-NATIVE,
MULTIMODAL,
MULTI-PROVIDER,
OPENAI + GEMINI ENABLED,
MULTI-AGENT,
MULTI-PC,
DEVICE-EXTENSIBLE,
SMART-HOME-READY,
AUTHORIZED-CCTV-READY,
IMAGE-GENERATING,
VIDEO-GENERATING,
FILE/WEB/OFFICE-CAPABLE,
CODING-CAPABLE,
GAME/3D-CAPABLE,
PROJECT-AUTONOMOUS,
MISSION-DRIVEN,
SELF-TESTING,
SELF-HEALING,
OWNER-APPROVED SELF-EXPANDING,
RECOVERABLE,
AUDITABLE,
LONG-TERM PERSONAL AI OPERATING SYSTEM.


THE EVENTUAL INTERFACE SHOULD FEEL AS SIMPLE AS:


“NOVA.”


“Yes?”


“Handle this.”


And NOVA should perform the legitimate, authorized digital work
required to finish the goal.


BEGIN IMPLEMENTATION.