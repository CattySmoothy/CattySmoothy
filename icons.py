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

    @app.context_processor
    def _inject_icon_sprite():
        return {'icon_sprite': SPRITE}
