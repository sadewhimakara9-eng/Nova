"""NOVA Glass: local assets, escaped copy, and reusable Streamlit presentation.

Call ``apply_theme(settings, compact=True)`` once per app render. ``header``,
``orb``, and ``empty_state`` render directly; ``icon`` and ``badge`` return HTML
for composing cards with ``st.html``. Shared CSS classes include ``nova-hero``,
``nova-feature-card``, ``nova-eyebrow``, ``nova-muted``, and ``nova-status``.
All text arguments are escaped. No helper loads remote assets or runs JavaScript.
"""

from functools import lru_cache
import base64
from html import escape
import math
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

import streamlit as st


_ICONS = {
    "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z"/>',
    "chat": '<path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5H4l-2 2V11.5a9.5 9.5 0 0 1 19 0Z"/><path d="M7 9h10M7 13h6"/>',
    "voice": '<path d="M3 10v4m4-7v10m5-14v18m5-14v10m4-7v4"/>',
    "missions": '<rect x="5" y="4" width="14" height="17" rx="3"/><path d="M9 4V2h6v2M9 10h6M9 15h3"/>',
    "projects": '<path d="M3 7V5a2 2 0 0 1 2-2h5l3 4h6a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
    "agents": '<rect x="4" y="7" width="16" height="13" rx="4"/><path d="M12 3v4M2 12v3m20-3v3M9 16h6"/><circle cx="9" cy="12" r=".8"/><circle cx="15" cy="12" r=".8"/>',
    "memory": '<path d="M9 3a3 3 0 0 0-5 2v3a4 4 0 0 0 0 7v3a3 3 0 0 0 5 2 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3Zm6 0a3 3 0 0 1 5 2v3a4 4 0 0 1 0 7v3a3 3 0 0 1-5 2 3 3 0 0 1-3-3V6a3 3 0 0 1 3-3ZM5 8h2m-3 7h3m10-7h3m-3 7h3"/>',
    "automations": '<path d="m13 2-9 12h7l-1 8L21 9h-8Z"/>',
    "tools": '<path d="M14 5a5 5 0 0 0-6 6L3 16a3 3 0 0 0 5 5l5-5a5 5 0 0 0 6-6l-4 3-4-4Z"/>',
    "integrations": '<path d="m9 15 6-6m-5-4 2-2a5 5 0 0 1 7 7l-2 2m-3 7-2 2a5 5 0 0 1-7-7l2-2"/>',
    "devices": '<rect x="2" y="3" width="15" height="12" rx="2"/><path d="M6 20h7m-4-5v5"/><rect x="16" y="10" width="6" height="11" rx="1.5"/>',
    "privacy": '<path d="m12 2 8 4v6c0 5-8 10-8 10S4 17 4 12V6Z"/><path d="m8 12 3 3 5-6"/>',
    "shield": '<path d="m12 2 8 4v6c0 5-8 10-8 10S4 17 4 12V6Z"/><path d="m8 12 3 3 5-6"/>',
    "settings": '<path d="m9 3 1-1h4l1 3 3 1 3 2-1 4 1 4-3 2-3 1-1 3h-4l-1-3-3-1-3-2 1-4-1-4 3-2Z"/><circle cx="12" cy="12" r="3"/>',
    "search": '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>',
    "arrow": '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "mic": '<rect x="9" y="2" width="6" height="13" rx="3"/><path d="M5 10v2a7 7 0 0 0 14 0v-2m-7 9v3m-4 0h8"/>',
    "stop": '<rect x="5" y="5" width="14" height="14" rx="3"/>',
    "check": '<path d="m5 12 4 4L19 6"/>',
    "sparkles": '<path d="m12 3 2.5 6.5L21 12l-6.5 2.5L12 21l-2.5-6.5L3 12l6.5-2.5ZM20 2v4m-2-2h4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "upload": '<path d="M12 16V3m-5 5 5-5 5 5M4 16v4h16v-4"/>',
    "offline": '<path d="M3 3l18 18M8 8a8 8 0 0 1 12 2M4 10l1-1m3 5a5 5 0 0 1 5-1m-3 5 2 2 2-2"/>',
}


def _bounded(value, default: float, low: float, high: float) -> float:
    try:
        number = float(value)
        return max(low, min(high, number)) if math.isfinite(number) else default
    except (TypeError, ValueError):
        return default


@lru_cache(maxsize=1)
def _stylesheet() -> str:
    return Path(__file__).with_name("glass.css").read_text(encoding="utf-8")


def apply_theme(appearance: dict | None = None, compact: bool = False) -> None:
    """Apply numeric, bounded appearance tokens; never interpolate user CSS.

    appearance: glass 0–100, blur 0–24, scale 85–120, animation/orb_effects/
    performance booleans. Performance mode removes blur and orbital animation.
    Operating-system reduced-motion settings always take precedence.
    """
    options = appearance if isinstance(appearance, dict) else {}
    glass = _bounded(options.get("glass", 65), 65, 0, 100)
    transparency = _bounded(options.get("transparency", 60), 60, 0, 100)
    blur = _bounded(options.get("blur", 16), 16, 0, 24)
    scale = _bounded(options.get("scale", 100), 100, 85, 120)
    performance = bool(options.get("performance", False))
    alpha = 0.94 - transparency * 0.0047
    tokens = (
        f":root{{--nova-glass-alpha:{alpha:.3f};--nova-glass-highlight:{glass / 100:.3f};--nova-blur:{0 if performance else blur:.1f}px;"
        f"--nova-scale:{scale / 100:.3f};--nova-sidebar:{212 if compact else 245}px;}}"
    )
    overrides = ""
    if not options.get("animation", True) or performance:
        overrides += ".nova-orb-wrap *{animation:none!important}.nova-feature-card{transition:none!important}"
    if not options.get("orb_effects", True) or performance:
        overrides += ".nova-orb-particles,.nova-orb-halo,.nova-orb-satellite{display:none!important}"
    if performance:
        overrides += ".nova-orb-svg{filter:none!important}"
    st.html(f"<style>{_stylesheet()}\n{_navigation_icons()}\n{tokens}\n{overrides}</style>")


def icon(name: str, size: int = 20) -> str:
    """Return a local outline SVG image; inline SVG is stripped by st.html."""
    dimension = int(_bounded(size, 20, 12, 96))
    encoded = base64.b64encode(_raw_icon(name, dimension).encode()).decode()
    return f'<img class="nova-icon" width="{dimension}" height="{dimension}" src="data:image/svg+xml;base64,{encoded}" alt="" aria-hidden="true">'


def _raw_icon(name: str, dimension: int = 20) -> str:
    path = _ICONS.get(name, _ICONS["sparkles"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{dimension}" height="{dimension}" viewBox="0 0 24 24" '
        'fill="none" stroke="#638dab" stroke-width="1.65" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{path}</svg>'
    )


@lru_cache(maxsize=1)
def _navigation_icons() -> str:
    """Decorate the known native navigation labels without custom JS/widgets."""
    names = ("home", "chat", "voice", "missions", "projects", "agents", "memory",
             "automations", "tools", "integrations", "devices", "privacy", "settings")
    rules = []
    for index, name in enumerate(names, 1):
        image = quote(_raw_icon(name), safe="")
        rules.append(
            f'[data-testid="stSidebar"] [data-testid="stRadioGroup"] > div:nth-child({index}) > label[data-testid="stRadioOption"]::before'
            '{content:"";width:18px;height:18px;flex:0 0 18px;margin-right:10px;'
            f'background:currentColor;mask:url("data:image/svg+xml,{image}") center/contain no-repeat;'
            f'-webkit-mask:url("data:image/svg+xml,{image}") center/contain no-repeat;}}'
        )
    return "\n".join(rules)


def badge(label: str, tone: str = "blue") -> str:
    """Return an escaped status pill; supported tones blue/green/amber/red/gray."""
    tone = "gray" if tone == "neutral" else tone
    tone = tone if tone in {"blue", "green", "amber", "red", "gray"} else "blue"
    return f'<span class="nova-status nova-status-{tone}"><span></span>{escape(str(label))}</span>'


def header(title: str, subtitle: str = "", eyebrow: str = "") -> None:
    top = f'<div class="nova-eyebrow">{escape(str(eyebrow))}</div>' if eyebrow else ""
    description = f'<p>{escape(str(subtitle))}</p>' if subtitle else ""
    st.html(f'<header class="nova-page-header">{top}<h1>{escape(str(title))}</h1>{description}</header>')


def empty_state(title: str, description: str, icon: str = "sparkles") -> None:
    graphic = globals()["icon"](icon, 28)
    st.html(
        f'<div class="nova-empty"><div class="nova-empty-icon">{graphic}</div>'
        f'<h3>{escape(str(title))}</h3><p>{escape(str(description))}</p></div>'
    )


def orb(state: str = "idle", size: int = 260, label: str = "") -> None:
    """Render the original NOVA glass sphere; state is visual, never inferred.

    Supported states: idle/listening/thinking/speaking/working/success/warning/
    error/privacy/offline. Callers must only present actual backend activity, or
    explicitly label a state preview. The supplied label is screen-reader text.
    """
    states = {"idle", "listening", "thinking", "speaking", "working", "success", "warning", "error", "privacy", "offline"}
    state = state if state in states else "idle"
    size = int(_bounded(size, 260, 80, 600))
    uid = "nova" + uuid4().hex[:12]
    description = escape(str(label or f"NOVA · {state}"))
    # Unique gradient IDs allow multiple independently sized spheres on a page.
    svg = f'''<div class="nova-orb-wrap nova-orb-{state}" style="width:{size}px" role="img" aria-label="{description}">
      <div class="nova-orb-halo"></div>
      <svg xmlns="http://www.w3.org/2000/svg" class="nova-orb-svg nova-orb-{state}" viewBox="0 0 400 400" aria-hidden="true">
        <defs>
          <radialGradient id="{uid}-sphere" cx="32%" cy="26%" r="78%">
            <stop offset="0" stop-color="#ffffff" stop-opacity=".96"/>
            <stop offset=".38" stop-color="#eafcff" stop-opacity=".83"/>
            <stop offset=".64" stop-color="#9cddfa" stop-opacity=".46"/>
            <stop offset=".84" stop-color="#8bc4f3" stop-opacity=".55"/>
            <stop offset="1" stop-color="#d8f6ff" stop-opacity=".88"/>
          </radialGradient>
          <radialGradient id="{uid}-shine" cx="32%" cy="19%" r="70%">
            <stop stop-color="white" stop-opacity=".96"/>
            <stop offset=".25" stop-color="white" stop-opacity=".12"/>
            <stop offset=".72" stop-color="white" stop-opacity="0"/>
            <stop offset="1" stop-color="white" stop-opacity=".52"/>
          </radialGradient>
          <linearGradient id="{uid}-band" x1="0" y1="0" x2="1" y2="1">
            <stop stop-color="#ffffff" stop-opacity=".8"/>
            <stop offset=".4" stop-color="#65cefa" stop-opacity=".64"/>
            <stop offset=".7" stop-color="#3896ed" stop-opacity=".4"/>
            <stop offset="1" stop-color="#efffff" stop-opacity=".93"/>
          </linearGradient>
          <linearGradient id="{uid}-ring"><stop stop-color="#9edafa" stop-opacity=".15"/><stop offset=".5" stop-color="white"/><stop offset="1" stop-color="#74bde9" stop-opacity=".68"/></linearGradient>
          <clipPath id="{uid}-clip"><circle cx="200" cy="200" r="122"/></clipPath>
        </defs>
        <ellipse cx="200" cy="339" rx="69" ry="9" fill="#8dbfe0" opacity=".10"/>
        <g class="nova-orb-ring-back" fill="none" stroke="url(#{uid}-ring)">
          <ellipse cx="200" cy="200" rx="173" ry="67" transform="rotate(-31 200 200)" stroke-width="1.4"/>
          <ellipse cx="200" cy="200" rx="152" ry="137" transform="rotate(28 200 200)" stroke-width=".7" opacity=".63"/>
        </g>
        <g class="nova-orb-core">
          <circle cx="200" cy="200" r="126" fill="url(#{uid}-sphere)" stroke="white" stroke-opacity=".8" stroke-width="1.8"/>
          <g clip-path="url(#{uid}-clip)">
            <g class="nova-orb-flow">
              <path d="M49 253C103 305 131 110 202 132S288 295 360 147L372 238C296 338 267 200 205 191S107 344 49 286Z" fill="url(#{uid}-band)"/>
              <path d="M44 149C112 76 141 259 210 248S287 86 358 172L358 199C302 137 276 298 204 279S111 126 44 180Z" fill="url(#{uid}-band)" opacity=".65"/>
              <path d="M64 243C140 273 148 116 207 143S277 265 342 165" fill="none" stroke="white" stroke-width="2" opacity=".81"/>
              <path d="M67 159C134 119 152 278 216 259S291 124 337 178" fill="none" stroke="#eaffff" stroke-width="1.2" opacity=".95"/>
              <ellipse cx="214" cy="241" rx="85" ry="44" transform="rotate(-34 214 241)" fill="none" stroke="#ddf9ff" stroke-width="16" opacity=".17"/>
            </g>
          </g>
          <circle cx="200" cy="200" r="123" fill="url(#{uid}-shine)"/>
          <path d="M104 164A107 107 0 0 1 216 94" fill="none" stroke="white" stroke-width="4" stroke-linecap="round" opacity=".68"/>
          <path d="M292 236A106 106 0 0 1 207 306" fill="none" stroke="#f1ffff" stroke-width="2.5" stroke-linecap="round" opacity=".83"/>
          <ellipse cx="157" cy="123" rx="29" ry="10" transform="rotate(-23 157 123)" fill="white" opacity=".28"/>
        </g>
        <g class="nova-orb-ring-front" fill="none" stroke="url(#{uid}-ring)" stroke-width="1.4">
          <path d="M48 235C79 308 352 162 352 165" opacity=".85"/>
          <ellipse cx="200" cy="200" rx="153" ry="74" transform="rotate(43 200 200)" stroke-width=".6" opacity=".7"/>
        </g>
        <g class="nova-orb-particles" fill="#89ccef">
          <circle cx="56" cy="252" r="2.7"/><circle cx="322" cy="99" r="2"/>
          <circle cx="327" cy="278" r="2.5" fill="#c7ecfc"/><circle cx="119" cy="64" r="1.7"/>
          <circle cx="58" cy="133" r="1.4" fill="#d0e8f9"/><circle cx="235" cy="347" r="1.5"/>
        </g>
        <g class="nova-orb-satellite"><circle cx="342" cy="164" r="4" fill="#ebffff" stroke="#9ddcf5" stroke-width="1.2"/></g>
      </svg>
      <div class="nova-orb-state-mark">{icon('shield' if state == 'privacy' else 'check' if state == 'success' else 'offline', 17)}</div>
    </div>'''
    # Streamlit 1.65 sanitizes inline SVG tags; a local data image preserves the
    # original vector artwork without external requests or executable scripts.
    start = svg.index('<svg xmlns=')
    end = svg.index('</svg>', start) + len('</svg>')
    drawing = svg[start:end]
    motion = '''<style>
      .nova-orb-core{transform-origin:200px 200px;animation:breathe 7s ease-in-out infinite}
      .nova-orb-flow{transform-origin:200px 200px;animation:flow 18s ease-in-out infinite}
      .nova-orb-satellite{transform-origin:200px 200px;animation:orbit 32s linear infinite}
      .nova-orb-particles{transform-origin:200px 200px;animation:flow 13s ease-in-out infinite}
      .nova-orb-listening .nova-orb-core,.nova-orb-speaking .nova-orb-core{animation-duration:2.4s}
      .nova-orb-thinking .nova-orb-flow,.nova-orb-working .nova-orb-flow{animation:orbit 15s linear infinite}
      .nova-orb-thinking .nova-orb-satellite,.nova-orb-working .nova-orb-satellite{animation-duration:5s}
      .nova-orb-success .nova-orb-core{animation:breathe 1.3s ease-in-out 1}
      .nova-orb-offline *{animation:none!important}
      @keyframes breathe{0%,100%{transform:scale(.985)}50%{transform:scale(1.015)}}
      @keyframes flow{0%,100%{transform:rotate(-7deg)}50%{transform:rotate(13deg)}}
      @keyframes orbit{to{transform:rotate(360deg)}}
      @media(prefers-reduced-motion:reduce){*{animation:none!important}}
    </style>'''
    appearance = st.session_state.get("nova_appearance", {})
    if not appearance.get("animation", True) or appearance.get("performance", False):
        motion += '<style>*{animation:none!important}</style>'
    if not appearance.get("orb_effects", True) or appearance.get("performance", False):
        motion += '<style>.nova-orb-particles,.nova-orb-satellite{display:none}</style>'
    drawing = drawing.replace('</svg>', motion + '</svg>')
    encoded = base64.b64encode(drawing.encode()).decode()
    image = f'<img class="nova-orb-svg" width="{size}" height="{size}" src="data:image/svg+xml;base64,{encoded}" alt="">'
    st.html(svg[:start] + image + svg[end:])
