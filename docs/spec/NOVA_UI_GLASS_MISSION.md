# NOVA UI/UX IMPLEMENTATION MISSION
## PREMIUM WHITE TRANSPARENT GLASS INTERFACE
### Use the existing NOVA repository. Do not rebuild the project from scratch.

Continue the existing NOVA project and now focus on building a REAL, TESTABLE desktop user interface.

I am not a programmer.

Do the implementation yourself.

Do not only produce mockups or design documentation.

Inspect the repository, understand the existing architecture, implement the UI, run it, test it, fix startup/UI errors, and leave me with a working interface I can launch and test.

---

# 1. IMPORTANT: PRESERVE THE EXISTING NOVA SYSTEM

The existing NOVA architecture, agents, memory, missions, privacy, permissions, tools, voice architecture and backend must remain intact.

Do NOT:

- delete existing features
- replace working backend systems unnecessarily
- rewrite NOVA from scratch
- remove existing tests
- simplify the architecture just to make the UI easier
- fake a backend feature as working

Instead:

INSPECT EXISTING CODE
→ FIND CURRENT UI ENTRY POINT
→ FIND EXISTING CORE/APIS/EVENTS
→ BUILD THE NEW UI AROUND THEM
→ CONNECT REAL FUNCTIONALITY WHERE AVAILABLE
→ CLEARLY MARK UNAVAILABLE FEATURES AS DISCONNECTED/COMING SOON

---

# 2. VISUAL REFERENCES

Use the two UI reference images provided with this request as the visual direction.

Analyze them carefully.

The desired design language is:

# WHITE
# CLEAN
# PREMIUM
# TRANSPARENT
# FROSTED GLASS
# FUTURISTIC
# SOFT BLUE / CYAN GLOW
# MINIMAL
# LIGHT
# ELEGANT
# AI-ASSISTANT FEEL

The interface must NOT become:

- black-heavy
- grey enterprise dashboard
- gaming RGB UI
- cluttered
- flat Bootstrap-style UI
- neon cyberpunk
- purple-heavy
- opaque card-heavy
- developer-tool-looking

I specifically want a **fully white transparent look**.

---

# 3. CORE COLOR DIRECTION

The main visual environment should be approximately:

Background:
very pale white / ice white / pearl white.

Glass surfaces:
semi-transparent white.

Primary accent:
clean electric blue.

Secondary accent:
soft cyan / ice blue.

Optional tiny accent:
very subtle lavender only when useful.

Text:
dark blue-grey for readability.

Secondary text:
muted cool grey-blue.

Borders:
very thin white/translucent cool-blue.

Avoid strong black backgrounds.

---

# 4. GLASSMORPHISM SYSTEM

Create one reusable glass design system rather than manually styling every component.

Implement reusable design tokens/components for:

- glass panel
- glass button
- glass input
- glass card
- glass modal
- glass dropdown
- glass sidebar
- glass notification
- glass tooltip

Use effects such as:

- backdrop blur
- translucent white layers
- subtle internal highlights
- soft shadows
- subtle blue outer glow
- thin glass borders
- depth separation

The effect should feel like premium frosted crystal, NOT blurry cheap transparency.

Keep readability excellent.

---

# 5. BACKGROUND DESIGN

Create a sophisticated light background inspired by the reference images.

It should contain:

- soft white gradient
- pale blue ambient lighting
- subtle blurred glass forms
- soft luminous areas
- extremely subtle moving light if performance allows

Do NOT use a distracting wallpaper.

The content must remain readable.

---

# 6. CENTRAL NOVA ORB

The main visual identity of NOVA should be a beautiful central AI orb inspired by the references.

Create an ORIGINAL implementation.

It should look like:

- translucent glass energy sphere
- white / blue / cyan
- internal flowing light
- gentle glow
- subtle depth
- surrounding thin orbital rings
- tiny particles or dots
- premium futuristic appearance

The orb becomes NOVA's visual state indicator.

---

# 7. ORB STATES

Create visual states.

## IDLE

slow gentle breathing animation.

## LISTENING

orb becomes brighter.

rings respond.

subtle audio-reactive/wave animation.

## THINKING

internal light rotates or flows.

small orbit particles animate.

## SPEAKING

gentle pulse synchronized conceptually with audio output.

## WORKING

orbiting progress effect.

## SUCCESS

brief clean cyan-white pulse.

## WARNING

soft amber accent only temporarily.

## ERROR

soft red accent only temporarily.

## PRIVACY MODE

subtle shield/lock indicator.

## OFFLINE

muted white/grey-blue state.

Animations must remain elegant and calm.

Do not make the orb constantly flash.

---

# 8. MAIN APP LAYOUT

This is a WINDOWS DESKTOP APP, not an iPhone clone.

Use the reference mobile design language, but adapt it intelligently for desktop.

Main structure:

TOP / HEADER AREA

LEFT NAVIGATION

CENTER WORKSPACE

OPTIONAL RIGHT CONTEXT PANEL

BOTTOM COMMAND COMPOSER

The UI must scale correctly on different desktop resolutions.

---

# 9. LEFT NAVIGATION

Create a slim premium glass sidebar.

Include:

Home

Chat

Voice

Missions

Projects

Agents

Memory

Automations

Tools

Integrations

Devices

Privacy

Settings

Use elegant outline icons.

Default state should be compact.

Allow expand/collapse.

Do not make sidebar visually heavy.

Use white transparent glass.

---

# 10. HOME SCREEN

HOME should feel like NOVA is alive and ready.

Central area:

NOVA orb

Greeting such as:

“Good afternoon.”

or

“Ready.”

Below it, show only useful information.

Possible lightweight cards:

Active Missions

Next Calendar Item

System Status

Pending Approval

Recent Project

Do NOT fill the entire screen with widgets.

Keep lots of clean space.

---

# 11. CHAT / VOICE SWITCHER

At the top of the primary assistant workspace create a segmented switch similar to the reference images:

CHAT | VOICE

Use:

rounded pill shape

transparent white glass

blue active state

soft glow

animated sliding selection

Chat selected:
show chat experience.

Voice selected:
show immersive voice experience.

---

# 12. CHAT SCREEN

Chat should feel more advanced than a normal chatbot.

Layout:

Top:
Chat / Voice segmented control

Center:
conversation timeline or NOVA orb when conversation is empty

Bottom:
floating glass composer

Messages:

Owner message:
clean translucent bubble aligned appropriately.

NOVA message:
light glass surface with minimal border.

Do not use giant opaque message blocks.

Use generous spacing.

---

# 13. BOTTOM MESSAGE COMPOSER

Reproduce the visual feeling of the first reference.

Floating translucent glass pill.

Elements:

+ attachment button

message input

microphone button

send button

Send button:

circular / rounded

blue → cyan gradient

soft glow

simple paper-plane icon

Placeholder:

“Ask NOVA anything…”

or

“Type a message…”

Composer must remain visible and elegant.

---

# 14. ATTACHMENT BUTTON

Clicking + should open a glass menu:

File

Image

Document

Screenshot

Folder

Clipboard

Do not implement unsafe actions merely for visual effect.

Connect available existing features.

---

# 15. VOICE MODE

When Voice is selected, change the center experience.

Use the second reference image as direction.

Show:

large NOVA orb

status:

Listening…
Thinking…
Working…
Speaking…

Live transcription underneath.

Example:

Listening…

“Nova, open my project and continue where I stopped.”

Then show a subtle state line:

Processing request

Do NOT use the Kyoto sample from the reference.

Use NOVA-relevant placeholder/example text.

---

# 16. VOICE PANEL

Create a floating frosted glass panel beneath or around the orb.

Elements:

animated waveform icon

current state

live transcript

processing indicator

small cancel/stop control where appropriate

The microphone control can sit below the panel as a circular glass button.

---

# 17. LIVE AUDIO VISUALIZATION

If microphone/STT integration exists:

connect visualization to actual audio level.

If it does not yet exist:

create the UI interface/state architecture but clearly keep integration state accurate.

Do NOT pretend microphone transcription works if backend is disconnected.

---

# 18. SINHALA UI SUPPORT

NOVA is Sinhala-first.

The UI must correctly render Unicode Sinhala.

Test text such as:

“ආයුබෝවන්”

“මම සූදානම්.”

“ඔබට අද මොන වැඩේ කරගන්න ඕනද?”

“කියන්න, මම ඒක බලන්නම්.”

Sinhala must render cleanly with no broken glyphs.

The same interface must support:

Sinhala

English

Sinhala-English mixed text.

---

# 19. HOME GREETING BEHAVIOR

Use contextual greeting without clutter.

Examples:

“Good morning.”

“Good evening.”

“Ready when you are.”

In Sinhala mode:

“සුභ උදෑසනක්.”

or natural conversational Sinhala appropriate to the configured personality.

Do not make every screen verbose.

---

# 20. MISSION SCREEN

Build a beautiful transparent mission dashboard.

Sections:

Running

Queued

Waiting for You

Completed

Each mission card may contain:

mission title

agent

progress

status

elapsed time

priority

Expand to reveal:

subtasks

agent assignments

verification state

logs summary

Use white translucent cards.

---

# 21. LIVE MISSION MINI-INDICATOR

When NOVA is working in the background, show a small unobtrusive glass indicator.

Example:

3 missions running

Clicking expands details.

Do not interrupt normal chat.

---

# 22. PROJECTS SCREEN

Grid/list of projects.

Each project card:

name

type

status

last activity

progress

next milestone

Examples:

NOVA Development

Sci-Fi Game

3D House Project

Study Project

Clicking opens project workspace.

---

# 23. PROJECT WORKSPACE

Show:

project title

current milestone

active missions

recent files

recent decisions

memory summary

next actions

Keep interface visually clean.

---

# 24. AGENTS SCREEN

Show agent team as an elegant visual network or clean card grid.

Examples:

NOVA Director

Planner

Memory

PC Agent

Browser Agent

Coding Agent

Research Agent

Game Director

Security Agent

Voice Agent

Each agent:

online/offline

current job

reliability

permissions summary

Do not make it look like a server monitoring console.

---

# 25. MEMORY SCREEN

Create friendly memory management UI.

Sections:

Preferences

Projects

People

Devices

Workflows

Important Memories

Secrets must NOT appear here in plaintext.

For credentials show only something like:

Wi-Fi Credential — Stored securely

Never display the password unless explicit secure reveal is designed.

---

# 26. AUTOMATIONS SCREEN

Show automation rules with simple human-readable cards.

Example:

Every night
→ Backup NOVA

When I say “Work Mode”
→ Open current project
→ Enable focus mode
→ Play focus music

Allow enable/disable toggle.

---

# 27. TOOLS / INTEGRATIONS SCREEN

Use clear status chips:

CONNECTED

DISCONNECTED

DEGRADED

AUTH EXPIRED

LOCAL

Examples:

OpenAI

Browser

GitHub

Gmail

Calendar

WhatsApp

Blender

Unreal Engine

Smart Home

Do not claim disconnected services are active.

---

# 28. PRIVACY SCREEN

This screen should look especially trustworthy and simple.

Display:

Current Privacy Mode

Cloud Access

Local-Only switch

Recent External Data Activity

Protected Apps

Protected Folders

Network Egress Summary

Use shield icon.

No scary hacker-style visuals.

---

# 29. APPROVAL MODAL

For important actions such as:

sending message

payment

permanent delete

security change

use a beautiful glass confirmation modal.

Show clearly:

WHAT NOVA WANTS TO DO

TARGET

COST if relevant

DATA LEAVING DEVICE if relevant

REVERSIBILITY

Buttons:

Cancel

Approve Once

Approve

Never hide important consequences in tiny text.

---

# 30. SETTINGS SCREEN

Categories:

General

Appearance

Voice

Sinhala

Personality

Privacy

Memory

Permissions

Models

APIs

Integrations

Automations

Notifications

Developer

Updates

Keep advanced settings separated from basic settings.

---

# 31. APPEARANCE SETTINGS

Allow:

Glass intensity

Transparency

Blur strength

Animation level

Orb effects

UI scale

Light mode

For now the PRIMARY/default theme is:

# NOVA GLASS WHITE

Do NOT prioritize dark mode during this task.

Get the white transparent theme perfect first.

---

# 32. FULL WHITE TRANSPARENT REQUIREMENT

This is mandatory.

The default user experience should look overwhelmingly:

WHITE + GLASS + LIGHT BLUE.

Avoid large opaque surfaces.

Use transparency in:

sidebar

cards

composer

voice panel

modals

menus

header

status elements

But always maintain enough contrast for readability.

---

# 33. MICRO-INTERACTIONS

Add premium subtle interactions:

button hover glow

soft card lift

glass reflection movement

smooth tab switch

orb breathing

composer focus glow

subtle page transitions

Do NOT over-animate.

---

# 34. MOTION DESIGN

Recommended durations:

quick interaction:
120–180 ms

page transitions:
200–350 ms

orb idle:
slow several-second cycle

Use smooth easing.

Respect reduced-motion system preferences.

---

# 35. WINDOW DESIGN

If framework allows:

custom clean title bar

rounded-feeling content surface

subtle transparency

drag region

minimize

maximize

close

Do not break standard Windows window behavior.

---

# 36. RESPONSIVE DESKTOP DESIGN

Test at minimum:

1366×768

1920×1080

2560×1440

The app must not overflow or clip important controls.

Also support narrow window mode.

---

# 37. PERFORMANCE

Glass blur and animations must not make NOVA slow.

Target smooth interaction.

Use GPU-friendly effects where appropriate.

Avoid dozens of unnecessary blur layers.

If hardware is weak:

automatically reduce visual effects or expose a performance mode.

---

# 38. ACCESSIBILITY

Maintain:

good text contrast

keyboard navigation

visible focus state

tooltips

reasonable font size

screen scaling

reduced motion

Do not sacrifice usability for transparency.

---

# 39. FONT / TYPOGRAPHY

Use a clean modern system-safe font stack.

Must render Sinhala correctly.

Prefer typography similar in feeling to premium modern OS interfaces.

Headings:
clean and medium weight.

Body:
high readability.

Avoid decorative sci-fi fonts.

---

# 40. ICONOGRAPHY

Use one consistent icon family.

Icons should be:

minimal

rounded

thin/medium stroke

professional

Do not mix random emoji into core navigation.

---

# 41. EMPTY STATES

Every screen should have intentional empty states.

Example Missions:

“No active missions.”

“Give NOVA something to work on.”

Do not show raw JSON or blank developer panels.

---

# 42. LOADING STATES

Use:

soft skeletons

small orb animation

subtle progress indicators

Never freeze UI without explanation.

---

# 43. ERROR STATES

Use calm messages.

Example:

“Browser integration is unavailable.”

Button:

Reconnect

Details hidden under optional “View details”.

Do not dump Python stack traces into normal user UI.

Developer mode may reveal technical logs.

---

# 44. TOAST NOTIFICATIONS

Use floating translucent notification cards.

Examples:

Mission completed

File saved

Integration connected

Approval required

Keep them short.

---

# 45. COMMAND PALETTE

Add optional command palette.

Keyboard shortcut if appropriate.

Search:

commands

projects

settings

tools

---

# 46. GLOBAL NOVA OVERLAY

Implement or prepare a small quick overlay matching the same glass design.

Possible invocation:

global hotkey

Small UI:

NOVA orb

single text input

mic

close

It should disappear cleanly when done.

---

# 47. SYSTEM TRAY

Keep existing NOVA system tray requirements.

Tray should allow:

Open NOVA

Voice mute

Pause automations

Privacy mode

Emergency stop

Exit

---

# 48. UI STATE ARCHITECTURE

Create proper application state for:

assistant mode

connection state

voice state

mission state

privacy mode

active project

pending approvals

notifications

Avoid ad-hoc global variables.

---

# 49. REAL BACKEND CONNECTION

Inspect the existing NOVA code first.

Find:

Core entry point

mission service

agent registry

memory service

permissions

voice interface

event bus

Use existing interfaces rather than duplicating the backend.

If necessary, introduce a clean UI service layer.

---

# 50. UI ↔ CORE EVENT FLOW

Prefer architecture similar to:

UI
↓
UI Controller / API Layer
↓
NOVA Core
↓
Mission / Agents / Tools
↓
Events
↓
UI updates

Examples:

MISSION_STARTED

MISSION_PROGRESS

MISSION_COMPLETED

VOICE_LISTENING

VOICE_PROCESSING

VOICE_SPEAKING

APPROVAL_REQUIRED

INTEGRATION_CHANGED

PRIVACY_MODE_CHANGED

---

# 51. STREAMING CHAT

If backend supports streaming responses, render them smoothly.

If not, design components so streaming can be connected later.

---

# 52. FUNCTIONAL BUTTONS

Important rule:

Do not create a beautiful screen full of dead buttons.

Buttons should either:

WORK

or

be visibly marked DISABLED / COMING SOON.

---

# 53. UI TEST MODE

Because the owner wants to test the interface now, create a UI demo/test mode if backend modules are incomplete.

But:

- clearly label mock states
- isolate mock data
- do not alter production backend state
- do not claim mock integrations are real

The owner must still be able to navigate and visually test every major screen.

---

# 54. REQUIRED FIRST WORKING UI FLOW

At minimum, before declaring this task complete, I must be able to:

1. Launch NOVA.
2. See the premium white transparent interface.
3. See the NOVA orb.
4. Switch Chat ↔ Voice.
5. Type a message.
6. Send a message to the current NOVA chat handler if available.
7. Open Missions.
8. Open Projects.
9. Open Agents.
10. Open Memory.
11. Open Settings.
12. Return Home.
13. Resize the window without broken layout.
14. Close and restart the app successfully.

---

# 55. VOICE UI TEST FLOW

I should be able to click Voice.

See:

NOVA orb

Listening state UI

mic control

transcription area

If actual STT exists, connect it.

If not:

show honest status:

“Voice engine not connected”

while keeping the UI testable.

---

# 56. VISUAL ACCEPTANCE CRITERIA

The design fails if:

- interface looks grey/dark
- background becomes black
- it looks like VS Code
- it looks like an admin dashboard
- cards are thick opaque rectangles
- gradients are oversaturated
- excessive purple is used
- glow becomes neon
- interface becomes cluttered
- glass effect makes text unreadable

---

# 57. VISUAL SUCCESS CRITERIA

It succeeds if the first impression is:

“Premium futuristic white AI assistant.”

The visual language should closely match the FEEL of the supplied references:

white translucent layers

ice-blue lighting

floating glass controls

soft cyan glow

central intelligent orb

large amount of breathing space

minimal elegant controls

---

# 58. DO NOT COPY PHONE HARDWARE

The supplied references show a phone.

Do NOT render:

iPhone frame

Dynamic Island

mobile status bar

fake battery/time

inside the Windows desktop app.

Use only the UI design language.

---

# 59. ORIGINALITY

Do not directly copy copyrighted branded UI elements.

Create an original NOVA interface inspired by:

frosted white glass

premium mobile/desktop OS polish

futuristic AI visualization

---

# 60. IMPLEMENTATION PROCESS

Do the following now:

STEP 1:
Inspect repository and identify current UI/backend stack.

STEP 2:
Run existing app and understand current state.

STEP 3:
Do not destroy working functionality.

STEP 4:
Create reusable NOVA Glass design tokens/components.

STEP 5:
Implement main application shell.

STEP 6:
Implement Home.

STEP 7:
Implement Chat.

STEP 8:
Implement Voice state UI.

STEP 9:
Implement Missions/Projects/Agents/Memory basic pages.

STEP 10:
Implement Settings/Privacy basic pages.

STEP 11:
Connect existing backend functionality.

STEP 12:
Implement honest disconnected/mock states where backend is missing.

STEP 13:
Run application.

STEP 14:
Fix visual/layout/runtime errors.

STEP 15:
Test resizing/navigation.

STEP 16:
Run relevant automated tests.

STEP 17:
Update README and PROJECT_STATUS.md.

STEP 18:
Tell me exactly how to launch the new UI.

---

# 61. DO NOT STOP AFTER WRITING CODE

You must actually run the application.

If startup fails:

diagnose it.

fix it.

run it again.

Continue until the UI opens successfully unless an unavoidable owner credential/external dependency blocks progress.

---

# 62. SCREENSHOT / VISUAL VERIFICATION

If your environment supports screenshots:

launch the application

capture the interface

inspect it visually

compare against the reference design direction

fix obvious spacing/contrast/layout problems

Then verify again.

---

# 63. DO NOT ASK ME TO CODE

I am the product owner, not the programmer.

Do not ask me to:

edit CSS

write Python

install individual libraries manually

fix imports

modify files

Choose and perform the required development actions yourself.

---

# 64. PRESERVE NOVA BRAND

The UI must clearly be NOVA.

Use NOVA name subtly.

The central orb should become NOVA's primary visual identity.

Avoid copying ChatGPT branding.

---

# 65. FINAL DESIGN TARGET

Create a desktop application that feels like:

A PRIVATE PERSONAL AI
+
PREMIUM WHITE GLASS OS
+
FUTURISTIC AI ORB
+
NATURAL CHAT
+
IMMERSIVE VOICE
+
POWERFUL BACKGROUND AUTONOMY

The UI should visually communicate:

calm

intelligence

trust

speed

privacy

premium quality

---

# FINAL COMMAND

DO NOT JUST EXPLAIN THE UI.

IMPLEMENT IT IN THE CURRENT NOVA REPOSITORY NOW.

USE THE TWO ATTACHED REFERENCE IMAGES AS VISUAL GUIDANCE.

KEEP THE DEFAULT THEME FULLY WHITE, TRANSPARENT, FROSTED-GLASS AND BLUE/CYAN.

CONNECT IT TO THE EXISTING NOVA CORE WHERE POSSIBLE.

RUN IT.

TEST IT.

FIX IT.

VERIFY IT.

LEAVE ME WITH A WORKING NOVA UI I CAN OPEN AND TEST.
