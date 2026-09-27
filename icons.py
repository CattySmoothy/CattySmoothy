"""Line-icon set used across the site in place of colour emoji.

Every icon is drawn on a 24x24 grid with a 1.6 stroke, round joins and the
odd solid diamond accent, in the spirit of HoYoverse UI icons. They inherit
`currentColor`, so they follow the theme. Use `{{ ico('moon') }}` in a
template; the sprite itself is emitted once from base.html.
"""
from markupsafe import Markup

# name -> inner SVG. Shapes with fill="currentColor" are the solid accents.
ICONS = {
    'clapper': '<path d="M4 10.5V20h16v-9.5"/><path d="M3.2 6.6 20 3.4l.7 4-16.8 3.2z"/><path d="m8.2 5.6 1 4m4.2-4.8 1 4"/>',
    'frame': '<rect x="3.5" y="5" width="17" height="14"/><path d="m3.5 15.5 4.6-4.6 4.2 4.2 2.6-2.6 5.6 5.6"/><path d="m16.6 8.2 1.3 1.3-1.3 1.3-1.3-1.3z" fill="currentColor" stroke="none"/>',
    'moon': '<path d="M19.5 14.6A7.6 7.6 0 1 1 9.4 4.5a6.2 6.2 0 0 0 10.1 10.1z"/><path d="m17.4 3.6.9 1.7 1.7.9-1.7.9-.9 1.7-.9-1.7-1.7-.9 1.7-.9z" fill="currentColor" stroke="none"/>',
    'pencil': '<path d="m4 20 1.2-4.2 11-11a2 2 0 0 1 2.8 0l1.2 1.2a2 2 0 0 1 0 2.8l-11 11z"/><path d="m14.5 6.7 2.8 2.8"/>',
    'paw': '<circle cx="6.5" cy="11" r="1.9"/><circle cx="10" cy="6.8" r="1.9"/><circle cx="14" cy="6.8" r="1.9"/><circle cx="17.5" cy="11" r="1.9"/><path d="M12 12.5c-3 0-5.5 3-4.5 5.3.8 1.8 3 1.5 4.5 1.5s3.7.3 4.5-1.5c1-2.3-1.5-5.3-4.5-5.3z"/>',
    'people': '<circle cx="9" cy="8.5" r="3"/><circle cx="17" cy="9.5" r="2.3"/><path d="M3.5 19c0-3.3 2.5-5.5 5.5-5.5s5.5 2.2 5.5 5.5"/><path d="M15.6 13.9c2.6 0 4.9 1.6 4.9 4.6"/>',
    'scroll': '<path d="M6 4h12v14a2 2 0 0 0 2 2H8a2 2 0 0 1-2-2z"/><path d="M6 4a2 2 0 0 0-2 2 2 2 0 0 0 2 2"/><path d="M9.5 9h5M9.5 12.5h5"/>',
    'medal': '<circle cx="12" cy="14.5" r="5.5"/><path d="m8.4 3.5 3.6 6 3.6-6"/><path d="m12 11.8 1.1 1.9 1.9 1.1-1.9 1.1-1.1 1.9-1.1-1.9-1.9-1.1 1.9-1.1z" fill="currentColor" stroke="none"/>',
    'brush': '<path d="M20 4c-4 1-8 5-9.5 9.5l2 2C17 14 19 8 20 4z"/><path d="M10.5 13.5c-2.5-.5-4.5 1-4.5 3.2 0 1.5-.8 2.3-2 3.3 3.2.6 7-.3 7-4z"/>',
    'book': '<path d="M12 6c-2-1.6-5-2-8-1.5v13c3-.5 6-.1 8 1.5 2-1.6 5-2 8-1.5v-13c-3-.5-6-.1-8 1.5z"/><path d="M12 6v13"/>',
    'gamepad': '<path d="M7.5 8h9a4.5 4.5 0 0 1 4.4 5.4l-.6 3a2.4 2.4 0 0 1-4.1 1.1L14 15.5h-4l-2.2 2a2.4 2.4 0 0 1-4.1-1.1l-.6-3A4.5 4.5 0 0 1 7.5 8z"/><path d="M8 10.5v3M6.5 12h3"/><path d="M15.5 11.2h.01M17.6 13h.01" stroke-width="2.2"/>',
    'tv': '<rect x="3.5" y="7" width="17" height="11.5"/><path d="m8.5 3.5 3.5 3.5 3.5-3.5M7.5 21h9"/><path d="M6.5 10.5v4.5" stroke-width="1.2"/>',
    'bolt': '<path d="M13 3 5 13.5h6L10 21l9-11.5h-6z"/>',
    'journal': '<path d="M7 3.5h10a2 2 0 0 1 2 2V20H9a2 2 0 0 1-2-2z"/><path d="M4 7.5h4M4 12h4M4 16.5h4"/><path d="M11 8h5M11 11.5h3"/>',
    'cat': '<path d="M5 19V8.5L8 4l3 2.5h2L16 4l3 4.5V19s-2 1-7 1-7-1-7-1z"/><path d="M9 12h.01M15 12h.01" stroke-width="2.2"/><path d="M10.8 15h2.4l-1.2 1.3z" fill="currentColor" stroke="none"/>',
    'palette': '<path d="M12 3.5a8.5 8.5 0 1 0 0 17c1.4 0 2-1 1.6-2-.5-1.3.2-2.5 1.7-2.5H17a3.5 3.5 0 0 0 3.5-3.5C20.5 6.8 16.7 3.5 12 3.5z"/><path d="M7.5 11h.01M10 7.6h.01M14.2 7.6h.01" stroke-width="2.2"/>',
    'books': '<path d="M4.5 4h4v16h-4zM10 4h4v16h-4z"/><path d="m15.6 6.2 3.7-1 3.2 14.4-3.7 1z"/>',
    'folder': '<path d="M3.5 6.5A1.5 1.5 0 0 1 5 5h4l2 2.5h8A1.5 1.5 0 0 1 20.5 9v9a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 18z"/>',
    'sparkle': '<path d="M12 2.5c.6 4.8 2.7 7 7.5 9.5-4.8 2.5-6.9 4.7-7.5 9.5-.6-4.8-2.7-7-7.5-9.5 4.8-2.5 6.9-4.7 7.5-9.5z" fill="currentColor" stroke="none"/>',
    'mail': '<rect x="3.5" y="6" width="17" height="12"/><path d="m3.5 7 8.5 6.5L20.5 7"/>',
    # commission-queue set
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'trash': '<path d="M5 7h14"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/><path d="m7 7 1 13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1l1-13"/><path d="M10 11v6M14 11v6"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'coin': '<circle cx="12" cy="12" r="8.5"/><path d="M9.3 14.5c.4 1 1.3 1.6 2.7 1.6 1.7 0 2.7-.8 2.7-2 0-1.1-.9-1.6-2.7-2-1.8-.4-2.7-.9-2.7-2 0-1.2 1-2 2.7-2 1.4 0 2.3.6 2.7 1.6" stroke-width="1.4"/><path d="M12 7.2v1.3M12 15.5v1.3" stroke-width="1.4"/>',
    'calendar': '<rect x="3.5" y="5.5" width="17" height="15" rx="1"/><path d="M3.5 10h17M8 3.5v4M16 3.5v4"/>',
    'grip': '<circle cx="9" cy="6" r="1.2" fill="currentColor" stroke="none"/><circle cx="9" cy="12" r="1.2" fill="currentColor" stroke="none"/><circle cx="9" cy="18" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="6" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="12" r="1.2" fill="currentColor" stroke="none"/><circle cx="15" cy="18" r="1.2" fill="currentColor" stroke="none"/>',
    'chevron-left': '<path d="M14.5 5.5 8 12l6.5 6.5"/>',
    'chevron-right': '<path d="M9.5 5.5 16 12l-6.5 6.5"/>',
    'clock': '<circle cx="12" cy="12.5" r="8.5"/><path d="M12 7.5V13l4 2"/>',
}


def _symbols():
    return ''.join(
        f'<symbol id="ico-{name}" viewBox="0 0 24 24">{body}</symbol>'
        for name, body in ICONS.items()
    )


SPRITE = Markup(
    '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" '
    'style="position:absolute" aria-hidden="true" focusable="false">'
    + _symbols() + '</svg>'
)


# ── small full-colour pixel-art graphics (fixed retro palette, not tied to
# the theme — same idea as the shimeji cat's own fixed palette) ──
_PIXEL_TV_INNER = (
    "<rect x=\"11\" y=\"0\" width=\"3\" height=\"1\" fill=\"#2b2018\"/><rect x=\"10\" y=\"1\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"11\" y=\"1\" width=\"1\" height=\"1\" fill=\"#fff3c4\"/><rect x=\"12\" y=\"1\" width=\"2\" height=\"1\" fill=\"#f0c34d\"/><rect x=\"14\" y=\"1\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"10\" y=\"2\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"11\" y=\"2\" width=\"1\" height=\"1\" fill=\"#fff3c4\"/><rect x=\"12\" y=\"2\" width=\"2\" height=\"1\" fill=\"#c78d2c\"/><rect x=\"14\" y=\"2\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"10\" y=\"3\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"11\" y=\"3\" width=\"1\" height=\"1\" fill=\"#f0c34d\"/><rect x=\"12\" y=\"3\" width=\"2\" height=\"1\" fill=\"#c78d2c\"/><rect x=\"14\" y=\"3\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"11\" y=\"4\" width=\"3\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"5\" width=\"14\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"6\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"6\" width=\"7\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"9\" y=\"6\" width=\"7\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"6\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"7\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"7\" width=\"2\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"4\" y=\"7\" width=\"8\" height=\"1\" fill=\"#4a3826\"/><rect x=\"12\" y=\"7\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"13\" y=\"7\" width=\"3\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"7\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"8\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"8\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"3\" y=\"8\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"4\" y=\"8\" width=\"1\" height=\"1\" fill=\"#183a30\"/><rect x=\"5\" y=\"8\" width=\"1\" height=\"1\" fill=\"#eafff5\"/><rect x=\"6\" y=\"8\" width=\"6\" height=\"1\" fill=\"#183a30\"/><rect x=\"12\" y=\"8\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"13\" y=\"8\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"14\" y=\"8\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"15\" y=\"8\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"8\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"9\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"9\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"3\" y=\"9\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"4\" y=\"9\" width=\"2\" height=\"1\" fill=\"#183a30\"/><rect x=\"6\" y=\"9\" width=\"1\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"7\" y=\"9\" width=\"3\" height=\"1\" fill=\"#183a30\"/><rect x=\"10\" y=\"9\" width=\"1\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"11\" y=\"9\" width=\"1\" height=\"1\" fill=\"#183a30\"/><rect x=\"12\" y=\"9\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"13\" y=\"9\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"14\" y=\"9\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"15\" y=\"9\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"9\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"10\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"10\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"3\" y=\"10\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"4\" y=\"10\" width=\"2\" height=\"1\" fill=\"#183a30\"/><rect x=\"6\" y=\"10\" width=\"1\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"7\" y=\"10\" width=\"3\" height=\"1\" fill=\"#183a30\"/><rect x=\"10\" y=\"10\" width=\"1\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"11\" y=\"10\" width=\"1\" height=\"1\" fill=\"#183a30\"/><rect x=\"12\" y=\"10\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"13\" y=\"10\" width=\"3\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"10\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"11\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"11\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"3\" y=\"11\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"4\" y=\"11\" width=\"2\" height=\"1\" fill=\"#183a30\"/><rect x=\"6\" y=\"11\" width=\"1\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"7\" y=\"11\" width=\"3\" height=\"1\" fill=\"#183a30\"/><rect x=\"10\" y=\"11\" width=\"1\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"11\" y=\"11\" width=\"1\" height=\"1\" fill=\"#183a30\"/><rect x=\"12\" y=\"11\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"13\" y=\"11\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"14\" y=\"11\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"15\" y=\"11\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"11\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"12\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"12\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"3\" y=\"12\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"4\" y=\"12\" width=\"3\" height=\"1\" fill=\"#183a30\"/><rect x=\"7\" y=\"12\" width=\"3\" height=\"1\" fill=\"#8ff0c8\"/><rect x=\"10\" y=\"12\" width=\"2\" height=\"1\" fill=\"#183a30\"/><rect x=\"12\" y=\"12\" width=\"1\" height=\"1\" fill=\"#4a3826\"/><rect x=\"13\" y=\"12\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"14\" y=\"12\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"15\" y=\"12\" width=\"1\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"12\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"13\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"13\" width=\"2\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"4\" y=\"13\" width=\"8\" height=\"1\" fill=\"#4a3826\"/><rect x=\"12\" y=\"13\" width=\"1\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"13\" y=\"13\" width=\"3\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"13\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"1\" y=\"14\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"14\" width=\"7\" height=\"1\" fill=\"#ecdcb8\"/><rect x=\"9\" y=\"14\" width=\"7\" height=\"1\" fill=\"#d3bd8c\"/><rect x=\"16\" y=\"14\" width=\"1\" height=\"1\" fill=\"#2b2018\"/><rect x=\"2\" y=\"15\" width=\"14\" height=\"1\" fill=\"#2b2018\"/><rect x=\"4\" y=\"16\" width=\"2\" height=\"1\" fill=\"#2b2018\"/><rect x=\"12\" y=\"16\" width=\"2\" height=\"1\" fill=\"#2b2018\"/><rect x=\"4\" y=\"17\" width=\"2\" height=\"1\" fill=\"#2b2018\"/><rect x=\"12\" y=\"17\" width=\"2\" height=\"1\" fill=\"#2b2018\"/>"
)


def pixel_tv(cls=''):
    """A chunky pixel-art CRT TV with a cute glowing face and a small coin
    balanced on top — used as the Support page's icon."""
    extra = f' {cls}' if cls else ''
    return Markup(
        f'<svg class="pixel-tv{extra}" viewBox="0 0 18 18" xmlns="http://www.w3.org/2000/svg" '
        f'shape-rendering="crispEdges" aria-hidden="true" focusable="false">{_PIXEL_TV_INNER}</svg>'
    )


def ico(name, cls=''):
    """Inline reference to an icon from the sprite."""
    if name not in ICONS:
        return Markup('')
    extra = f' {cls}' if cls else ''
    return Markup(
        f'<svg class="ico{extra}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        f'<use href="#ico-{name}"/></svg>'
    )


def register_icons(app):
    app.jinja_env.globals['ico'] = ico
    app.jinja_env.globals['pixel_tv'] = pixel_tv

    @app.context_processor
    def _inject_icon_sprite():
        return {'icon_sprite': SPRITE}
