# =====================================================================
# NOVA v10.0 — ULTIMATE MASTER BUILD SPECIFICATION
# MAXIMUM-PRACTICAL AUTONOMOUS PERSONAL AI OPERATING SYSTEM
# =====================================================================
#
# PRIVATE • LOCAL-FIRST • SINHALA-FIRST • VOICE-FIRST • VISION-FIRST
# WINDOWS-NATIVE • MULTIMODAL • MULTI-AGENT • MULTI-DEVICE
# COMPUTER-VISION • TOOL-USING • SELF-EXTENDING UNDER CONTROL
# RECOVERABLE • AUDITABLE • PREMIUM WHITE-GLASS UI
#
# THIS FILE BECOMES THE CANONICAL NOVA PRODUCT SPECIFICATION.
#
# =====================================================================


# =====================================================================
# 0. EXECUTION DIRECTIVE
# =====================================================================

You are the engineering organization responsible for building NOVA.

You are acting as:

Principal Software Architect
AI Agent Engineer
Windows Systems Engineer
Distributed Systems Engineer
Computer Vision Engineer
Voice AI Engineer
Sinhala Language Engineer
Memory Systems Engineer
Tooling Engineer
Browser Automation Engineer
Office Automation Engineer
API Integration Engineer
Security Engineer
Privacy Engineer
DevOps / SRE Engineer
QA Engineer
Desktop UI Engineer
Game Development Engineer
3D Pipeline Engineer
Media AI Engineer
Education AI Engineer
Automation Engineer
Release Engineer
Technical Product Director

The owner is NOT a programmer.

The owner must not be asked to manually:

write code
fix imports
edit JSON
debug libraries
manage migrations
configure low-level environments
resolve Git conflicts
write CSS
write PowerShell
build tool adapters

Do those engineering tasks yourself.

Ask the owner only when truly necessary for:

credentials
external account authorization
payment
irreversible/destructive approval
sensitive security approval
physical-device pairing
a genuinely ambiguous personal decision

DO NOT RETURN ONLY A PLAN.

BUILD.

RUN.

TEST.

FIX.

VERIFY.

CHECKPOINT.

CONTINUE.


# =====================================================================
# 1. EXISTING REPOSITORY — DO NOT REBUILD BLINDLY
# =====================================================================

This is an existing NOVA repository.

Before changing code:

1. Inspect the complete repository.
2. Read AGENTS.md.
3. Read README.md.
4. Read docs/NOVA_MASTER_SPEC.md if present.
5. Read PROJECT_STATUS.md.
6. Read FUTURE_ROADMAP.md.
7. Inspect tests.
8. Inspect current UI.
9. Inspect current backend.
10. Inspect current integrations.
11. Run the current application.
12. Determine what actually works.

Preserve verified working functionality.

Do NOT delete working systems merely because a better architecture is described here.

Migrate incrementally.


# =====================================================================
# 2. CANONICAL SPEC CONSOLIDATION
# =====================================================================

Merge all legitimate previous NOVA requirements into:

docs/NOVA_MASTER_SPEC.md

This v10 specification is the canonical architecture.

Also maintain:

docs/PROJECT_STATUS.md
docs/FUTURE_ROADMAP.md
docs/REQUIREMENT_MATRIX.md
docs/ARCHITECTURE.md
docs/SECURITY_MODEL.md
docs/PRIVACY_MODEL.md

REQUIREMENT_MATRIX must map:

requirement
→ subsystem
→ implementation
→ tests
→ status
→ blocker
→ version


# =====================================================================
# 3. PRODUCT VISION
# =====================================================================

NOVA is NOT a chatbot.

NOVA is a Personal AI Operating System.

Target workflow:

OWNER GOAL
↓
UNDERSTAND INTENT
↓
RETRIEVE CONTEXT + MEMORY
↓
DEFINE SUCCESS
↓
DISCOVER CAPABILITIES
↓
PLAN
↓
ASSIGN AGENTS
↓
SELECT TOOLS / APIS / DEVICES
↓
EXECUTE
↓
OBSERVE RESULTS
↓
VERIFY
↓
RECOVER / RETRY / ROLLBACK
↓
UPDATE MEMORY / PROJECT STATE
↓
REPORT BRIEFLY

The owner should increasingly be able to say:

“Nova, handle this.”

and NOVA should do the work.


# =====================================================================
# 4. GENERALIZATION — EXAMPLES ARE NEVER LIMITS
# =====================================================================

Every example command in this specification is an illustration.

It is NOT a whitelist.

Do NOT build:

if command == "open chrome"
if command == "edit video"
if command == "order pizza"

Build:

LANGUAGE
→ INTENT
→ GOAL
→ CAPABILITIES
→ TOOLS
→ PLAN
→ EXECUTE
→ VERIFY

NOVA must understand requests never explicitly listed here.

Owner must not memorize exact commands.


# =====================================================================
# 5. CAPABILITY COMPOSITION
# =====================================================================

Capabilities must combine dynamically.

Example:

“Edit these photos, create a presentation, save it and message Sasmitha.”

May require:

FILE_SEARCH
IMAGE_ANALYSIS
IMAGE_EDITING
PRESENTATION_CREATION
FILE_EXPORT
MESSAGING

No dedicated hard-coded command required.


# =====================================================================
# 6. CAPABILITY REGISTRY
# =====================================================================

Create a runtime capability registry.

Each capability declares:

capability_id
name
description
category
inputs
outputs
supported modalities
required agents
required tools
required providers
permissions
privacy level
risk
verification
estimated latency
estimated cost
reliability
status
version

Planner searches this registry dynamically.


# =====================================================================
# 7. CAPABILITY GAP / SKILL FACTORY
# =====================================================================

When a legitimate requested capability is missing:

CHECK EXISTING CAPABILITIES
↓
CHECK TOOL REGISTRY
↓
CHECK INSTALLED APPLICATIONS
↓
CHECK APIS
↓
CHECK PLUGINS
↓
CHECK MCP
↓
CHECK CAPABILITY COMPOSITION
↓
RESEARCH SAFE SOLUTION
↓
DESIGN NEW SKILL / ADAPTER
↓
IMPLEMENT IN ISOLATION
↓
SANDBOX
↓
TEST
↓
SECURITY REVIEW
↓
PRIVACY REVIEW
↓
APPROVAL IF NEEDED
↓
INSTALL
↓
VERIFY
↓
REGISTER
↓
RESUME ORIGINAL GOAL

Do not silently weaken security/privacy boundaries.


# =====================================================================
# 8. NOVA COGNITIVE STACK
# =====================================================================

Implement logical layers:

REFLEX BRAIN
FAST BRAIN
CONVERSATION BRAIN
DEEP REASONING BRAIN
PLANNER BRAIN
WORLD MODEL
MEMORY BRAIN
VISION BRAIN
ACTION BRAIN
CRITIC BRAIN
VERIFIER BRAIN
SECURITY BRAIN
RECOVERY BRAIN
DEVELOPER BRAIN

REFLEX:
instant local commands.

FAST:
simple requests and routing.

CONVERSATION:
natural dialogue.

DEEP:
hard reasoning.

PLANNER:
mission decomposition.

VISION:
screens/images/video/UI understanding.

ACTION:
tools/APIs/devices.

CRITIC:
find errors.

VERIFIER:
verify real-world outcome.

RECOVERY:
failures/rollback.


# =====================================================================
# 9. INTENT CONTRACT
# =====================================================================

For meaningful tasks internally identify:

owner goal
desired output
quality level
deadline
constraints
privacy
cost
allowed external effects
success criteria
what must NOT happen

Prevent goal drift.


# =====================================================================
# 10. UNCERTAINTY ENGINE
# =====================================================================

Track confidence for:

intent
visual interpretation
memory
tool target
recipient
file identity
research fact
device state
API result

Low confidence + high-impact action:
VERIFY / ASK.

High confidence + reversible safe action:
AUTO when policy allows.


# =====================================================================
# 11. KNOW WHEN NOT TO ACT
# =====================================================================

Possible correct action:

ACT
WAIT
OBSERVE
VERIFY
ASK
SIMULATE
DEFER

Do not execute merely because a tool exists.


# =====================================================================
# 12. SINHALA-FIRST
# =====================================================================

Treat Sri Lankan Sinhala as first-class.

Support:

spoken Sinhala
colloquial Sinhala
Sinhala slang
English-Sinhala code switching
shortened phrases
typos
informal commands
technical English mixed into Sinhala

Examples:

“Nova Chrome eka open karanna.”

“Nova ban me video eka edit karanna.”

“Nova mama nidagannawa, me tika iwara karanna.”

“Na na mama kiwwe eka nemei.”

No formal Sinhala requirement.


# =====================================================================
# 13. SINHALA SPEECH QUALITY
# =====================================================================

Prioritize:

clear Sri Lankan pronunciation
natural rhythm
natural pauses
correct question intonation
mixed English pronunciation
low latency

Maintain owner pronunciation dictionary for:

people
places
apps
brands
projects
technical words


# =====================================================================
# 14. VOICE-FIRST NOVA
# =====================================================================

Wake word:

NOVA

Support:

streaming STT
streaming TTS
Sinhala
English
Sinhala-English
VAD
barge-in
noise handling
mic selection
speaker selection
confidence
push-to-talk fallback

Emergency:

“Nova stop.”
“Nova emergency stop.”


# =====================================================================
# 15. ALWAYS-LISTENING VOICE SESSION
# =====================================================================

When owner enters Voice mode:

START ACTIVE LISTENING SESSION
↓
WAIT FOR SPEECH
↓
VOICE ACTIVITY DETECTION
↓
TRANSCRIBE
↓
UNDERSTAND
↓
ACT / ANSWER
↓
SPEAK
↓
RETURN TO LISTENING

No manual mic press required every turn.

Requirements:

visible listening indicator
mute
stop when leaving Voice
do not permanently record ambient audio
respect privacy settings


# =====================================================================
# 16. COMPUTER VISION — CORE REQUIREMENT
# =====================================================================

COMPUTER VISION IS A CORE NOVA SUBSYSTEM.

Do not treat vision as a future optional add-on.

Create:

Vision Gateway
Screen Understanding Agent
UI Detection Agent
Document Vision Agent
Image Understanding Agent
Video Understanding Agent
Camera Vision Adapter
Visual Verification Agent


# =====================================================================
# 17. SCREEN VISION
# =====================================================================

NOVA must be able to inspect authorized screens.

Understand:

application identity
window
buttons
menus
forms
text fields
dialogs
errors
images
charts
tables
selected items
visible notifications
scroll position
UI hierarchy where available

Prefer structured accessibility data first.

Use vision when structured UI data is unavailable.


# =====================================================================
# 18. SCREEN COMMAND EXAMPLES
# =====================================================================

Owner may say:

“Fix this error.”

“Fill this application.”

“Click the blue button.”

“Move this file.”

“Continue what I was doing.”

“What is on my screen?”

“Open the app shown here.”

NOVA should combine:

SCREEN UNDERSTANDING
+
CONTEXT
+
PC CONTROL
+
VERIFICATION


# =====================================================================
# 19. COMPUTER VISION INPUT TYPES
# =====================================================================

Support authorized:

screenshots
live screen frames
selected-screen region
images
scanned documents
PDF pages
video frames
camera feeds
application canvases
game-engine viewports


# =====================================================================
# 20. VISION PROVIDER ABSTRACTION
# =====================================================================

Define:

VisionProvider
OCRProvider
ObjectDetectionProvider
UIDetectionProvider
VideoUnderstandingProvider

Allow:

cloud vision
local vision
specialized local CV

Privacy Router decides whether frames can leave device.


# =====================================================================
# 21. VISION PRIVACY
# =====================================================================

Never continuously upload full desktop to cloud.

Prefer:

UI Automation tree
structured metadata
cropped region
redacted screenshot
local vision

before full-frame external upload.

Allow private windows to be marked:

NO_CAPTURE
NO_OCR
LOCAL_VISION_ONLY
NO_CLOUD


# =====================================================================
# 22. VISUAL VERIFICATION
# =====================================================================

After GUI action:

observe result visually or structurally.

Example:

click Save
→ verify save dialog closed
→ verify file exists

open Gemini
→ verify correct window/tab

fill form
→ verify fields contain intended values


# =====================================================================
# 23. LIVE VIDEO UNDERSTANDING
# =====================================================================

For owner-supplied or authorized video:

scene detection
object understanding
text recognition
speech/transcript alignment
event detection
timeline understanding
quality analysis

Use for:

editing
search
summaries
game QA
authorized CCTV


# =====================================================================
# 24. LOCAL-FIRST CONTROL PLANE
# =====================================================================

Main NOVA node:

OWNER_PC

Runs:

NOVA Core
Mission Engine
Memory
Policy Engine
Privacy Router
Secrets Vault
Device Mesh Controller
Tool Gateway
Agent Orchestrator
Audit Log

Cloud AI does NOT become machine authority.


# =====================================================================
# 25. NOVA DEVICE MESH — MULTI-DEVICE CONTROL
# =====================================================================

The owner has multiple devices.

NOVA must support a secure DEVICE MESH.

One main NOVA instance should be able to coordinate authorized secondary devices.

Possible nodes:

Windows desktop
Windows laptop
second PC
home server
GPU workstation
phone companion
tablet
smart-home gateway

Each device runs a small:

NOVA NODE AGENT

when needed.


# =====================================================================
# 26. NODE AGENT
# =====================================================================

Each device node exposes only approved capabilities.

Node metadata:

device_id
owner
device_name
OS
hardware
capabilities
online state
permissions
trust level
last heartbeat
resource status

Possible capabilities:

run approved apps
file operations
system information
screens
notifications
compute jobs
renders
game builds
media processing
browser tasks


# =====================================================================
# 27. DEVICE PAIRING
# =====================================================================

No automatic uncontrolled LAN takeover.

Pair devices explicitly.

Pairing:

OWNER INITIATES
↓
ONE-TIME PAIRING CODE / QR
↓
DEVICE IDENTITY CREATED
↓
KEY EXCHANGE
↓
OWNER APPROVES
↓
PERMISSIONS SELECTED
↓
TRUSTED DEVICE REGISTERED

Use strong encrypted authentication.

Do not rely solely on IP address.


# =====================================================================
# 28. DEVICE MESH SECURITY
# =====================================================================

Requirements:

mutual authentication
encrypted channels
device identity
key rotation
revocation
least privilege
audit logs
permission scopes
no anonymous remote control

Remote device command must include:

mission ID
target device
requested capability
permission
expiry
audit context


# =====================================================================
# 29. DEVICE PERMISSION EXAMPLES
# =====================================================================

PC-2 may allow:

render jobs
file access to Projects folder

but deny:

browser cookies
private documents
password manager

Laptop may allow:

notifications
project sync

but deny admin actions.

Permissions are per-device.


# =====================================================================
# 30. DEVICE DISCOVERY
# =====================================================================

Allow secure discovery of candidate NOVA nodes on trusted local networks.

Discovery does NOT equal permission.

Discovered device:
UNPAIRED

Only paired devices are controllable.


# =====================================================================
# 31. DEVICE HEARTBEAT
# =====================================================================

Track:

online/offline
CPU
GPU
RAM
disk
battery
temperature where available
current workload

Use for task routing.


# =====================================================================
# 32. DISTRIBUTED TASK ROUTER
# =====================================================================

NOVA may route tasks to best authorized node.

Examples:

GPU render
→ strongest idle GPU PC

game build
→ development workstation

document task
→ main PC

background backup
→ home server

Choose based on:

capabilities
privacy
load
power
network
owner preference


# =====================================================================
# 33. MULTI-DEVICE COMMAND EXAMPLES
# =====================================================================

“Nova, PC 2 eke Blender render eka run karanna.”

“Nova, laptop eke project eka open karanna.”

“Nova, render job eka free GPU eka thiyana PC ekata yawanna.”

“Nova, me file eka mage other PC ekata copy karanna.”

These are examples, not limits.


# =====================================================================
# 34. FILE TRANSFER BETWEEN DEVICES
# =====================================================================

Use:

authenticated
encrypted
verified

file transfer.

Before overwrite:

check conflict
version
hash
policy

Support resume for large transfers.


# =====================================================================
# 35. DISTRIBUTED PROJECT WORKSPACE
# =====================================================================

Project may span devices.

Track:

canonical repo
working copies
assets
build outputs
render outputs
sync state

Do not create silent file conflicts.


# =====================================================================
# 36. PHONE COMPANION
# =====================================================================

Future/optional phone client may provide:

chat
voice
approval notifications
mission status
quick commands
calling bridge
camera input where authorized

Remote command access disabled until paired.


# =====================================================================
# 37. WINDOWS PC CONTROL
# =====================================================================

Prefer:

official app API
native API/SDK
CLI
PowerShell
Windows API
UI Automation
browser automation
vision + mouse/keyboard fallback

Capabilities:

launch app
close app
focus app
move/resize windows
keyboard
mouse
clipboard
File Explorer
screenshots
notifications
audio
processes
system info
multi-monitor
safe terminal operations


# =====================================================================
# 38. GENERAL WINDOWS APPLICATION RESOLVER
# =====================================================================

“Open X” must NOT rely on a tiny hard-coded list.

Search:

running apps
Start Menu
App Paths
registered executables
Windows packaged apps
installed PWAs
browser apps
known aliases
owner aliases

Use fuzzy matching.

Examples:

chrome
gemini
calculator
notepad
blender
unreal
unity
vscode
spotify

Verify launched result.


# =====================================================================
# 39. GEMINI / WEB APP FALLBACK
# =====================================================================

For:

“open Gemini”

resolve:

installed native/PWA
→ launch

otherwise:
official web application
→ default browser

Do not route app launch to free-form chat failure.


# =====================================================================
# 40. LOCAL COMMAND ROUTER
# =====================================================================

Run deterministic/local intent routing BEFORE LLM fallback.

Classes:

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

Basic Windows actions must work even if cloud LLM is offline.


# =====================================================================
# 41. LOCAL MIXED-SINHALA COMMANDS
# =====================================================================

Support:

“Gemini eka open karanna.”
“YouTube yanna.”
“Chrome eka arinna.”
“Calculator open karanna.”
“Downloads eka open karanna.”


# =====================================================================
# 42. AI PROVIDER HUB
# =====================================================================

Do not hardcode NOVA to one AI model.

Provider interfaces:

LLMProvider
ReasoningProvider
CodingProvider
VisionProvider
EmbeddingProvider
STTProvider
TTSProvider
ImageProvider
ImageEditProvider
VideoProvider
AudioProvider
SearchProvider

Initial architecture may support:

OpenAI
Google Gemini

but these are NOT limits.


# =====================================================================
# 43. SECURE AI PROVIDER SETUP
# =====================================================================

UI:

Settings
→ AI
→ Providers

Each provider:

Disconnected
Connected
Auth expired
Degraded

Allow secure credential input.

Store credential in Secrets Vault.

Never expose entire key again.

Never save in:

Git
README
master prompt
frontend bundle
logs


# =====================================================================
# 44. PROVIDER ROUTER
# =====================================================================

Choose model by:

task
privacy
quality
speed
cost
language
vision
coding need
availability
reliability

Model categories:

LOCAL_FAST
LOCAL_REASONING
CLOUD_FAST
CLOUD_REASONING
CODING
VISION
VOICE
EMBEDDING


# =====================================================================
# 45. PROVIDER FALLBACK
# =====================================================================

If one provider fails:

retry safely
→ alternate approved provider
→ preserve mission state

Do not destroy the mission.


# =====================================================================
# 46. LOCAL AI
# =====================================================================

Support optional local models for:

privacy
offline operation
simple routing
summaries
basic chat
embeddings

Do not expose provider-engineering terminology in everyday UI.


# =====================================================================
# 47. UNIVERSAL API HUB
# =====================================================================

Support integration adapters for:

REST
GraphQL
WebSocket
webhook
OAuth
API key
MCP
CLI
SDK
local IPC

Every connector declares:

capabilities
authentication
privacy
permissions
rate limits
health
cost
retry
timeout


# =====================================================================
# 48. BROWSER AGENT
# =====================================================================

Capabilities:

open
navigate
search
read
click
type
scroll
forms
upload
download
tabs
structured extraction

Do not bypass CAPTCHA/2FA.


# =====================================================================
# 49. BROWSER VISUAL CONTROL
# =====================================================================

Prefer DOM / accessibility selectors.

Use screen vision if needed.

Verify after interaction.


# =====================================================================
# 50. RESEARCH AGENT
# =====================================================================

Support:

multi-source
freshness
credibility
contradictions
citations
provenance
confidence
decision support

Current facts should be refreshed when needed.


# =====================================================================
# 51. FILE INTELLIGENCE
# =====================================================================

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
deduplicate
archive
backup
restore
hash
version

Default delete:
Recycle Bin.


# =====================================================================
# 52. SEMANTIC FILE SEARCH
# =====================================================================

Understand queries such as:

“Find that blue spaceship render from last week.”

Use:

filename
metadata
visual embeddings where permitted
text
project context


# =====================================================================
# 53. OFFICE
# =====================================================================

Support real:

Word
Excel
PowerPoint
PDF
CSV
documents
scans

Do not merely generate text.

Create actual output files when requested.


# =====================================================================
# 54. POWERPOINT
# =====================================================================

Support:

research
outline
slides
charts
images
speaker notes
formatting
verification
save/export

Example:

“Make a cats presentation and save to Downloads.”


# =====================================================================
# 55. EXCEL
# =====================================================================

Support:

data
formulas
validation
format
charts
pivots
analysis
cleaning
error checks


# =====================================================================
# 56. FORM FILLING
# =====================================================================

Owner:

“Fill this application on my screen.”

Vision + UI tree:

identify fields
retrieve approved information
fill
check
preview
submit according to policy


# =====================================================================
# 57. EMAIL
# =====================================================================

search
read
summarize
categorize
draft
reply
attachments
follow-up
task extraction

External sends obey communication policy.


# =====================================================================
# 58. MESSAGING
# =====================================================================

Architecture for legitimate:

WhatsApp
Telegram
SMS
desktop messaging
future providers

Verify recipient before send.


# =====================================================================
# 59. OPTIONAL AUTO-REPLY
# =====================================================================

Default:
OFF

Modes:

OFF
DRAFT_ONLY
ASK_BEFORE_SEND
TRUSTED_CONTACTS
AWAY
SMART_AUTO

Protections:

contact allowlist
rate limits
duplicate protection
bot-loop detection
quiet hours
sensitive-message escalation


# =====================================================================
# 60. CALLING
# =====================================================================

Support adapters for:

phone companion
VoIP
calling APIs
mobile bridge

Examples:

“Call Mom.”

“Call Pizza Hut.”

Transactional calls only through supported lawful mechanisms.


# =====================================================================
# 61. PURCHASE ASSISTANCE
# =====================================================================

Support ordinary legitimate purchase workflows.

research
compare
prepare cart
verify details
owner approval for financial commitment by default
submit
receipt
tracking

No age-restricted or dangerous purchases.


# =====================================================================
# 62. MEDIA STUDIO
# =====================================================================

NOVA must understand:

“Edit this photo.”

“Edit this video.”

without fixed templates.


# =====================================================================
# 63. IMAGE EDITING
# =====================================================================

crop
resize
rotate
color
exposure
white balance
contrast
denoise
sharpen
restore
upscale
background removal
background replacement
object removal
object addition where appropriate
inpainting
outpainting
perspective
text
graphics
thumbnails
batch processing

Always preserve original by default.


# =====================================================================
# 64. VIDEO EDITING
# =====================================================================

trim
split
join
scene detection
pacing
remove silence
transitions
crop
stabilization
speed
color
audio cleanup
subtitles
Sinhala subtitles
English subtitles
mixed subtitles
B-roll
titles
aspect conversion
short-form extraction
highlights
export presets


# =====================================================================
# 65. VIDEO AUTO-DIRECTOR
# =====================================================================

Analyze:

duration
resolution
orientation
frame rate
audio
speech
scenes
quality
platform goal

Then create an intelligent edit plan.


# =====================================================================
# 66. AUDIO
# =====================================================================

transcription
noise reduction
voice enhancement
normalization
EQ
compression
ducking
sync
conversion


# =====================================================================
# 67. MEDIA QUALITY VERIFIER
# =====================================================================

Verify final output:

file opens
expected duration
expected resolution
audio present
no corrupt frames
subtitle sync reasonable
export complete


# =====================================================================
# 68. CODING / SOFTWARE FACTORY
# =====================================================================

Support:

architecture
frontend
backend
database
APIs
debugging
testing
refactoring
security
performance
documentation
CI/CD
deployment
release


# =====================================================================
# 69. AUTONOMOUS DEBUGGING
# =====================================================================

REPRODUCE
↓
LOG
↓
HYPOTHESIS
↓
TEST
↓
FIX
↓
REGRESSION TEST
↓
VERIFY


# =====================================================================
# 70. WEBSITE FACTORY
# =====================================================================

Owner may simply ask:

“Build a crazy website and host it.”

NOVA should:

understand goal
design
build frontend
backend if needed
database
auth if needed
test
QA
deploy
verify
monitor

Paid hosting/domain follows approval policy.


# =====================================================================
# 71. GAME STUDIO
# =====================================================================

Agents:

Game Director
Producer
Game Design
Story
World
Gameplay
NPC AI
UI
Level
3D
Characters
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
# 72. HIGH-GRAPHICS GAME PIPELINE
# =====================================================================

Do not fake instant AAA completion.

Use:

vision
requirements
GDD
prototype
vertical slice
systems
world
assets
AI
audio
QA
optimization
builds
milestones


# =====================================================================
# 73. GAME ENGINE ADAPTERS
# =====================================================================

Support:

Unreal Engine
Unity
Godot

Choose based on requirements.


# =====================================================================
# 74. GAME MEMORY
# =====================================================================

Persist:

GDD
story
lore
characters
quests
levels
architecture
assets
bugs
tests
builds
milestones
performance


# =====================================================================
# 75. GAME QA AUTOMATION
# =====================================================================

Support:

automated launch
repeatable inputs
UI checks
crash detection
save/load tests
performance regression


# =====================================================================
# 76. 3D STUDIO
# =====================================================================

Support:

Blender
modeling
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
game export
architectural visualization


# =====================================================================
# 77. ARCHITECTURE VISUALIZATION
# =====================================================================

2D plan
→ interpret dimensions
→ blockout
→ walls/openings
→ materials
→ lighting
→ cameras
→ render

Do not guess missing dimensions silently.


# =====================================================================
# 78. EDUCATION
# =====================================================================

Support:

Study Planner
Weak Topic Agent
Revision Agent
Mock Exam Agent
Target Paper Agent
Answer Reviewer


# =====================================================================
# 79. O/L TARGET PAPER
# =====================================================================

Grade 10 paper used as reference should produce:

ORIGINAL
ADVANCED
O/L-STYLE
PRACTICE PAPER

Analyze:

topics
skills
difficulty
question styles

Then create original:

questions
marks
time
marking scheme
model answers


# =====================================================================
# 80. SMART HOME
# =====================================================================

Authorized:

lights
AC
fans
TV
speakers
plugs
curtains
sensors

Verify resulting state.


# =====================================================================
# 81. CCTV / CAMERA INTELLIGENCE
# =====================================================================

Authorized systems only.

Support:

health
event timeline
motion/person/vehicle summaries where lawful
offline alert
tamper alert
privacy zones
daily digest

Prefer local processing.


# =====================================================================
# 82. DEFENSIVE SECURITY
# =====================================================================

Authorized only.

Support:

dependency scanning
configuration audit
patch audit
permissions
secret detection
logs
file integrity
backup checks
security reports
remediation

No unauthorized intrusion/malware/credential theft.


# =====================================================================
# 83. MISSION ENGINE
# =====================================================================

Mission contains:

goal
success criteria
priority
deadline
dependencies
tasks
agents
tools
devices
permissions
privacy
budget
checkpoint
verification


# =====================================================================
# 84. MISSION STATES
# =====================================================================

CREATED
QUEUED
PLANNING
READY
RUNNING
WAITING_TOOL
WAITING_RESOURCE
WAITING_NETWORK
WAITING_AGENT
WAITING_USER
BLOCKED
PAUSED
VERIFYING
RETRYING
RECOVERING
COMPLETED
FAILED
CANCELLED
ROLLED_BACK


# =====================================================================
# 85. OVERNIGHT AUTONOMY
# =====================================================================

Owner can give many tasks then leave.

NOVA:

decomposes
prioritizes
runs parallel safe work
checkpoints
retries
uses fallback
continues independent work
collects blockers
creates morning report


# =====================================================================
# 86. MULTI-AGENT SYSTEM
# =====================================================================

Core agents may include:

Director
Planner
Mission
Memory
Context
Vision
PC
Browser
File
Office
Research
Email
Messaging
Calling
Calendar
Voice
Media
Coding
Developer
Debugger
Reviewer
QA
Verifier
Privacy
Security
Recovery
Education
Game
3D
Smart Home

Create temporary specialist agents when useful.


# =====================================================================
# 87. AGENT COMMUNICATION
# =====================================================================

Use structured task envelopes:

mission_id
task_id
agent
goal
inputs
constraints
permissions
privacy
deadline
budget
expected output
verification
status
result
error


# =====================================================================
# 88. AGENT RELIABILITY
# =====================================================================

Track:

success
failures
latency
cost
verification failure
tool errors

Prefer reliable agents.


# =====================================================================
# 89. MEMORY
# =====================================================================

Implement:

Short-Term
Working
Episodic
Semantic
Structured
Vector
Preference
Project
Knowledge Graph


# =====================================================================
# 90. PERSONAL WORLD MODEL
# =====================================================================

Entities:

OWNER
PEOPLE
CONTACTS
PROJECTS
DEVICES
APPLICATIONS
FILES
TASKS
MISSIONS
EVENTS
WORKFLOWS
PREFERENCES
LOCATIONS
TOOLS
AGENTS
SKILLS
SERVICES


# =====================================================================
# 91. WORKSPACE MEMORY
# =====================================================================

Remember:

active project
open apps
open files
workspace
recent tabs
Blender scene
game project
unfinished mission

Support:

“Continue where I stopped.”


# =====================================================================
# 92. MEMORY QUALITY
# =====================================================================

Track:

source
timestamp
confidence
scope
TTL
privacy
provenance

New explicit owner instruction overrides old inference.


# =====================================================================
# 93. SECRETS VAULT
# =====================================================================

Passwords/API keys are NOT normal memory.

Store encrypted.

Memory stores reference only.


# =====================================================================
# 94. PERMISSION ENGINE
# =====================================================================

ALLOW
DENY
ASK
ALLOW_ONCE
SESSION
PROJECT
DEVICE
APP
FOLDER
CONTACT
READ_ONLY
SANDBOX


# =====================================================================
# 95. RISK ENGINE
# =====================================================================

Assess:

reversibility
financial impact
privacy
security
external effect
confidence
target sensitivity

LOW
MEDIUM
HIGH
CRITICAL


# =====================================================================
# 96. DEFAULT ACTION POLICY
# =====================================================================

AUTO:
safe reversible local work

AUTO + VERIFY:
file organization
code
renders
research
ordinary app launch/control

ASK:
financial commitment
permanent delete
security/account change
major public/external effect

VAULT:
secrets

REFUSE / REDIRECT:
unauthorized hacking
piracy
illegal/dangerous operations


# =====================================================================
# 97. ACTION RECEIPTS
# =====================================================================

Record:

action
target
agent
tool
device
files changed
external effects
verification
rollback


# =====================================================================
# 98. NATURAL UNDO
# =====================================================================

Owner:

“Undo that.”

Find relevant action and reverse when possible.


# =====================================================================
# 99. CRASH / REBOOT RECOVERY
# =====================================================================

Persist:

mission state
task state
external-effect state
device jobs
project checkpoint

After restart:

verify uncertain operations
resume safe work


# =====================================================================
# 100. IDEMPOTENCY
# =====================================================================

Prevent duplicate:

messages
emails
orders
payments
bookings
form submissions
deployments
calendar events


# =====================================================================
# 101. TOOL HEALTH
# =====================================================================

Monitor:

browser
FFmpeg
voice
vision
providers
Blender
game engines
Office tools
node agents

Status:

HEALTHY
DEGRADED
FAILED
AUTH_REQUIRED


# =====================================================================
# 102. INTEGRATION SELF-REPAIR
# =====================================================================

Detect:

expired auth
API changes
missing executable
selector break
dependency change

Create repair mission.


# =====================================================================
# 103. OFFLINE OPERATION
# =====================================================================

If internet unavailable:

continue local tasks
continue PC control
continue memory
continue local models

Queue cloud-dependent work.


# =====================================================================
# 104. RESOURCE SCHEDULER
# =====================================================================

Monitor:

CPU
GPU
RAM
disk
network
battery
temperature

Schedule heavy:

renders
video
game builds
local AI

for suitable time/device.


# =====================================================================
# 105. PROJECT INTELLIGENCE
# =====================================================================

Support:

project health
milestones
bugs
tests
roadmap
decision memory
technical debt
deadline risk
requirements traceability


# =====================================================================
# 106. AUTO DOCUMENTATION
# =====================================================================

Maintain:

README
PROJECT_STATUS
CHANGELOG
architecture
API docs
user docs

without overwriting valuable human content blindly.


# =====================================================================
# 107. WORKFLOW LEARNING
# =====================================================================

OBSERVE
→ DETECT REPEATED SAFE PATTERN
→ SIMULATE
→ SUGGEST
→ OWNER APPROVES
→ AUTOMATE

No silent new automation.


# =====================================================================
# 108. VOICE MACROS
# =====================================================================

Owner can define:

“When I say Study Mode…”

without coding.

Compile natural-language workflow safely.


# =====================================================================
# 109. SMART AUTO-REPLY
# =====================================================================

Default OFF.

If enabled:

per-contact policy
rate limits
duplicate prevention
loop prevention
quiet hours
confidence threshold


# =====================================================================
# 110. PREMIUM SIMPLE UI
# =====================================================================

The backend may be complex.

The daily UI must be SIMPLE.

Primary sidebar:

Chat
Voice
Projects
Memory
Settings

Emergency Stop at bottom.

Do not expose:

Agents
Tools
Integrations
Devices
Missions
Privacy

as permanent primary sidebar items.

Keep those systems internally and under Settings/Advanced where appropriate.


# =====================================================================
# 111. UI LOOK
# =====================================================================

Default:

soft pearl
frosted glass
ice blue
cyan accents
deep slate-blue text

Not pure glaring white.

Not dark.

Not cyberpunk.

Not admin dashboard.


# =====================================================================
# 112. NOVA ORB
# =====================================================================

Central visual identity.

States:

IDLE
LISTENING
THINKING
WORKING
SPEAKING
SUCCESS
ERROR
PRIVACY
OFFLINE


# =====================================================================
# 113. CHAT UI
# =====================================================================

Owner messages:
right side
accent glass bubble

NOVA:
left side
neutral glass bubble

No giant full-width cards for short messages.

Composer:

[ + ] [ Message NOVA… ] [ mic ] [ send ]


# =====================================================================
# 114. VOICE UI
# =====================================================================

Voice screen primarily:

ORB
Listening / Thinking / Speaking
small transcription
mute

No huge technical setup boxes.


# =====================================================================
# 115. DYNAMIC GREETING
# =====================================================================

Use local system time.

Good morning
Good afternoon
Good evening
Good night

or natural configured Sinhala.


# =====================================================================
# 116. UI ACCENT SELECTOR
# =====================================================================

Small appearance selector.

Options such as:

Ice Blue
Cyan
Ocean
Silver
Lavender
Mint

Accent only.

Do not recolor entire UI aggressively.


# =====================================================================
# 117. NO VISIBLE TERMINAL
# =====================================================================

Normal NOVA startup:

NOVA UI ONLY.

No visible:

CMD
PowerShell
Windows Terminal
Python console

Use proper hidden/background process configuration.

Capture logs internally.


# =====================================================================
# 118. BACKGROUND SERVICE / LAUNCHER
# =====================================================================

Choose correct implementation for current stack:

GUI subsystem
background service
pythonw
CREATE_NO_WINDOW
packaged executable
hidden child processes

No terminal flash hacks.


# =====================================================================
# 119. SYSTEM TRAY
# =====================================================================

Tray:

Open NOVA
Mute Voice
Pause Autonomous Work
Privacy Mode
Emergency Stop
Exit


# =====================================================================
# 120. GLOBAL QUICK OVERLAY
# =====================================================================

Optional hotkey:

small NOVA orb
input
mic

Same UI language.


# =====================================================================
# 121. FEATURE HONESTY
# =====================================================================

Use:

NOT_STARTED
DESIGNING
IMPLEMENTING
PARTIAL
EXPERIMENTAL
WORKING
STABLE
BLOCKED

Never fake:

voice connected
AI connected
app opened
message sent
call made
website deployed
file created
test passed


# =====================================================================
# 122. ACCEPTANCE TESTS — CORE
# =====================================================================

Verify:

NOVA launches
no terminal
Chat works
local commands work
app resolver works
YouTube opens
Gemini opens/fallback works
dynamic greeting
Voice auto-listen
Voice exits cleanly
Emergency Stop
memory read/write
file task
browser task


# =====================================================================
# 123. ACCEPTANCE TESTS — VISION
# =====================================================================

Test:

screenshot understanding
visible button detection
simple form understanding
error-dialog reading
post-click verification
private-window exclusion


# =====================================================================
# 124. ACCEPTANCE TESTS — MULTI-DEVICE
# =====================================================================

Use controlled test nodes.

Test:

pair device
heartbeat
capability discovery
remote safe command
remote app launch
job routing
file transfer
disconnect
revocation
unauthorized command rejection


# =====================================================================
# 125. ACCEPTANCE TESTS — MEDIA
# =====================================================================

Image:
preserve original
edit
verify output

Video:
edit
export
verify playable output


# =====================================================================
# 126. ACCEPTANCE TESTS — OFFICE
# =====================================================================

Create real PPTX
create real XLSX
verify files open


# =====================================================================
# 127. ACCEPTANCE TESTS — RECOVERY
# =====================================================================

Crash process
restart
recover mission state
do not duplicate external effects


# =====================================================================
# 128. ACCEPTANCE TESTS — SECURITY
# =====================================================================

Secret does not enter logs.

Unpaired device cannot execute commands.

External web content cannot override policy.

Permanent delete policy enforced.


# =====================================================================
# 129. CONTINUOUS DEVELOPMENT LOOP
# =====================================================================

After every vertical slice:

RUN TESTS
↓
FIX
↓
VERIFY
↓
UPDATE REQUIREMENT MATRIX
↓
UPDATE PROJECT_STATUS
↓
CREATE CHECKPOINT
↓
SELECT NEXT DEPENDENCY-READY HIGH-VALUE FEATURE
↓
CONTINUE

Do NOT wait for owner between ordinary engineering milestones.


# =====================================================================
# 130. PRIORITY ORDER FROM CURRENT BUILD
# =====================================================================

CURRENT SCREENSHOTS SHOW THAT THE APP IS NOT YET FULL NOVA.

Observed symptoms include:

- Free-form AI not connected
- Voice disconnected
- local command routing incomplete
- app resolution incomplete
- UI still exposes technical states

Therefore current implementation priority is:

P0. Stabilize current repo and tests.

P1. Real local Windows command router.

P2. General application resolver.

P3. Secure AI Provider Hub + provider setup UI.

P4. Connect at least one real reasoning/chat provider through secure credentials.

P5. Implement Computer Vision gateway + screenshot understanding.

P6. Implement real Voice pipeline architecture and auto-listen state.

P7. Simplify daily UI.

P8. Mission persistence + background worker.

P9. Memory + project continuation.

P10. Browser Agent.

P11. Office tools.

P12. Device Mesh foundation.

P13. Pair second controlled PC test node.

P14. Media Studio.

P15. Communication integrations.

P16. Skill Factory.

P17. Game/3D/Education expansions.

Do not build P17 while P1-P6 are fake or broken.


# =====================================================================
# 131. DO NOT CREATE A DEMO-ONLY JARVIS
# =====================================================================

The objective is not a YouTube-style visual demo.

Do not prioritize fake animations over real capabilities.

UI polish matters,
but actual execution matters more.

A button that looks beautiful but does nothing is NOT a feature.

A voice orb with no functioning voice system is NOT voice capability.

A “Computer Vision” page without a real vision pipeline is NOT computer vision.


# =====================================================================
# 132. DEFINITION OF DONE
# =====================================================================

A feature is DONE only if:

implemented
wired to real subsystem
tested
run
verified
failure handled
security/privacy checked
documented

Mock/demo mode must be clearly labeled MOCK.


# =====================================================================
# 133. OWNER EXPERIENCE GOAL
# =====================================================================

Examples of future legitimate usage:

“Nova, open Gemini.”

“Nova, what is on my screen?”

“Nova, fix this error.”

“Nova, PC 2 eke Blender render eka run karanna.”

“Nova, edit this video.”

“Nova, make this PPTX.”

“Nova, continue my game.”

“Nova, message Sasmitha hi.”

“Nova, order my usual pizza.”

“Nova, make an O/L target paper.”

“Nova, I am going to sleep. Finish these tasks.”

These are examples only.

NOVA must generalize beyond them.


# =====================================================================
# 134. FINAL AUTONOMY RULE
# =====================================================================

Maximum practical autonomy:

SAFE
AUTHORIZED
VERIFIABLE
RECOVERABLE

Never equate autonomy with uncontrolled behavior.


# =====================================================================
# 135. FINAL BUILD COMMAND
# =====================================================================

NOW STOP PRODUCING ONLY ARCHITECTURE DISCUSSION.

INSPECT THE REAL REPOSITORY.

RUN THE REAL APP.

IDENTIFY WHAT IS ACTUALLY WORKING.

IMPLEMENT THE PRIORITY ORDER ABOVE.

DO NOT DELETE WORKING FEATURES.

DO NOT ADD FAKE BUTTONS.

DO NOT HARD-CODE A TINY COMMAND LIST.

DO NOT HARD-CODE API KEYS.

BUILD REAL COMPUTER VISION.

BUILD REAL LOCAL PC CONTROL.

BUILD SECURE MULTI-DEVICE NOVA NODE MESH.

BUILD REAL PROVIDER CONNECTIONS.

BUILD REAL VOICE ARCHITECTURE.

KEEP THE UI SIMPLE.

TEST EVERYTHING.

VERIFY EVERYTHING.

CONTINUE AUTOMATICALLY THROUGH THE ROADMAP.

The target system is:

NOVA
=
PRIVATE PERSONAL AI
+
SINHALA-FIRST VOICE
+
COMPUTER VISION
+
WINDOWS CONTROL
+
MULTI-DEVICE CONTROL
+
MEMORY
+
MULTI-AGENT ORCHESTRATION
+
BROWSER
+
OFFICE
+
MEDIA
+
SOFTWARE FACTORY
+
GAME / 3D STUDIO
+
EDUCATION
+
SMART HOME
+
AUTHORIZED SECURITY
+
SKILL FACTORY
+
RECOVERY
+
AUDIT
+
PREMIUM SIMPLE WHITE-GLASS UI

BEGIN IMPLEMENTATION NOW.

## Preserved requirements and consolidation

This v10 document is canonical. The [v8 specification](spec/NOVA_V8_MASTER_SPEC.md), [glass mission](spec/NOVA_UI_GLASS_MISSION.md), and [Advanced Expansion Pack](spec/NOVA_ADVANCED_EXPANSION.md) remain additive requirements wherever not superseded by v10. In particular, the 132 expansion records retain their IDs and evidence in [expansion traceability](EXPANSION_TRACEABILITY.md). v10 section 110 supersedes the old always-visible 13-item sidebar; internal pages remain available under Settings. Vision and the authenticated device mesh are core product requirements, not claims of installed functionality. See [current requirement matrix](REQUIREMENT_MATRIX.md), [future roadmap](FUTURE_ROADMAP.md), and [project status](PROJECT_STATUS.md).
