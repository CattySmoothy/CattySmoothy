/* Pixel cat shimeji: a little desktop mascot that wanders along the bottom of
   the page, naps, meows, and can be picked up, dragged and dropped.
   Sprites are drawn from the text grids below (16x16), scaled up crisp. */
(function () {
    'use strict';
    if (document.getElementById('shimeji')) return;

    var PX = 4;                 // screen pixels per sprite pixel
    var SIZE = 16 * PX;
    var SKINS = [
        { id: 'orange', name: 'Orange',       c: { k: '#3b2a2e', b: '#f4a95b', l: '#fde7c4', p: '#f58fae', w: '#ffffff', d: '#d9803a' } },
        { id: 'gray',   name: 'Gray tabby',   c: { k: '#2f2f3a', b: '#a9afbb', l: '#e8ebf1', p: '#f58fae', w: '#ffffff', d: '#7f8694' } },
        { id: 'black',  name: 'Black',        c: { k: '#120e16', b: '#4a4456', l: '#7a7488', p: '#f58fae', w: '#ffffff', d: '#332e3d' } },
        { id: 'snow',   name: 'Snow',         c: { k: '#5a4a55', b: '#fbf7f0', l: '#ffe6ea', p: '#f58fae', w: '#ffffff', d: '#ddd3c6' } },
        { id: 'candy',  name: 'Cotton candy', c: { k: '#5b3350', b: '#f8b9d6', l: '#fff0f7', p: '#ff6fa3', w: '#ffffff', d: '#e88fb8' } }
    ];

    function store(key, value) {
        try {
            if (value === null) localStorage.removeItem(key);
            else localStorage.setItem(key, value);
        } catch (err) {}
    }
    function recall(key) {
        try { return localStorage.getItem(key); } catch (err) { return null; }
    }

    var skinId = recall('shimejiSkin');
    var skin = SKINS.filter(function (k) { return k.id === skinId; })[0] || SKINS[0];
    var PALETTE = Object.assign({}, skin.c);

    // ── Sprites ──────────────────────────────────────────────────────────
    var FRONT = [
        '................',
        '..kk........kk..',
        '.kbbk......kbbk.',
        '.kbpbkkkkkkbpbk.',
        '.kbbbbbbbbbbbbk.',
        'kbbbbbbbbbbbbbbk',
        'kbbwkbbbbbbwkbbk',
        'kbbkkbbbbbbkkbbk',
        'kbpbbblpplbbbpbk',
        '.kbbbbllllbbbbk.',
        '..kkbbbbbbbbkk..',
        '..kbbbbbbbbbbk..',
        '..kbbbllllbbbk..',
        '..kbbbllllbbbbkk',
        '..kbbbbbbbbbbkbk',
        '.kkbbkkkkkkbbkk.'
    ];

    function withRows(base, changes) {
        var out = base.slice();
        Object.keys(changes).forEach(function (r) { out[r] = changes[r]; });
        return out;
    }

    var TAIL_UP = { 12: '..kbbbllllbbbkbk', 14: '..kbbbbbbbbbbk..' };
    var EYES_SHUT = { 6: 'kbbbbbbbbbbbbbbk', 7: 'kbbkkbbbbbbkkbbk' };
    var EYES_HAPPY = { 6: 'kbbbkbbbbbbkbbbk', 7: 'kbbkbkbbbbkbkbbk' };
    var EYES_WIDE = { 6: 'kbbwwbbbbbbwwbbk', 7: 'kbbwkbbbbbbwkbbk' };

    var SPRITES = {
        idleA: FRONT,
        idleB: withRows(FRONT, TAIL_UP),
        blink: withRows(FRONT, EYES_SHUT),
        sleep: withRows(FRONT, EYES_SHUT),
        sleepB: withRows(FRONT, Object.assign({}, EYES_SHUT, TAIL_UP)),
        happy: withRows(FRONT, EYES_HAPPY),
        happyB: withRows(FRONT, Object.assign({}, EYES_HAPPY, TAIL_UP)),
        held: withRows(FRONT, Object.assign({}, EYES_WIDE, {
            13: '...kkbbbbbbkk...',
            14: '....kbkkkkbk....',
            15: '....kbk..kbk....'
        }))
    };

    var SIDE = [
        '................',
        '................',
        '................',
        '.........kk.kk..',
        '........kbbkbbk.',
        '........kbbbbbbk',
        '........kbbbwkbk',
        '........kbbbkkbk',
        '.kkkkkkkkbbbblpk',
        '.kbbbbbbbkbbbbk.',
        '.kbbbbbbbbbk....',
        '.kbbllllllbbk...',
        '.kbbbbbbbbbbk...',
        '.kbk.kbk.kbk.kbk',
        '.kbk.....kbk....',
        '.kkk.....kkk....'
    ];
    var SIDE_B = withRows(SIDE, {
        14: '.....kbk.....kbk',
        15: '.....kkk.....kkk'
    });
    // The tail is a separate overlay so it can wag independent of the legs.
    var TAILS = [
        [[6, 0], [7, 0], [8, 0], [9, 0]],
        [[7, 1], [8, 0], [9, 0], [10, 0]]
    ];

    function sideSprite(legs, tail) {
        var grid = (legs ? SIDE_B : SIDE).map(function (r) { return r.split(''); });
        TAILS[tail].forEach(function (p) { grid[p[0]][p[1]] = 'd'; });
        return grid.map(function (r) { return r.join(''); });
    }
    SPRITES.walk0 = sideSprite(0, 0);
    SPRITES.walk1 = sideSprite(1, 1);
    SPRITES.walk2 = sideSprite(0, 1);
    SPRITES.walk3 = sideSprite(1, 0);

    // ── DOM ──────────────────────────────────────────────────────────────
    var root = document.createElement('div');
    root.id = 'shimeji';
    root.setAttribute('aria-hidden', 'true');
    root.innerHTML =
        '<div class="shimeji-bubble"></div>' +
        '<div class="shimeji-shadow"></div>' +
        '<canvas class="shimeji-sprite" width="16" height="16"></canvas>';
    document.body.appendChild(root);

    var canvas = root.querySelector('.shimeji-sprite');
    var bubble = root.querySelector('.shimeji-bubble');
    var shadow = root.querySelector('.shimeji-shadow');
    var ctx = canvas.getContext('2d');
    var currentSprite = null;

    function draw(name) {
        if (name === currentSprite) return;
        currentSprite = name;
        var rows = SPRITES[name];
        ctx.clearRect(0, 0, 16, 16);
        for (var y = 0; y < 16; y++) {
            for (var x = 0; x < 16; x++) {
                var c = rows[y].charAt(x);
                if (c !== '.') {
                    ctx.fillStyle = PALETTE[c];
                    ctx.fillRect(x, y, 1, 1);
                }
            }
        }
    }

    // ── State ────────────────────────────────────────────────────────────
    var reduceMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var x = 0, y = -SIZE, vx = 0, vy = 0;
    var dir = 1;                       // 1 = facing right, -1 = facing left
    var state = 'fall';
    var stateTime = 0, stateDuration = 0;
    var squash = 0;                    // >0 while squished from a landing
    var bubbleTimer = 0;
    var stayPut = false;               // true while the cat has been told to sit
    var hidden = recall('shimejiHidden') === '1';
    var menu = null;

    function groundY() { return window.innerHeight - SIZE - 2; }
    function maxX() { return window.innerWidth - SIZE; }
    function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }
    function rand(a, b) { return a + Math.random() * (b - a); }

    function say(text, ms) {
        bubble.textContent = text;
        bubble.classList.add('show');
        bubbleTimer = ms || 1400;
    }

    function setState(next, duration) {
        state = next;
        stateTime = 0;
        stateDuration = duration || 0;
        if (next === 'sleep') say('z z z', 2000);
    }

    function pickNext() {
        if (reduceMotion || stayPut) { setState('idle', 4000); return; }
        var r = Math.random();
        if (r < 0.5) {
            dir = Math.random() < 0.5 ? -1 : 1;
            setState('walk', rand(2000, 5000));
        } else if (r < 0.68) {
            setState('sleep', rand(6000, 11000));
        } else if (r < 0.82) {
            say(['meow!', 'mew~', 'nya!', '♥'][Math.floor(Math.random() * 4)], 1500);
            setState('idle', rand(1500, 3000));
        } else {
            setState('idle', rand(1500, 4000));
        }
    }

    // ── Dragging ─────────────────────────────────────────────────────────
    var dragging = false, moved = 0, offX = 0, offY = 0;
    var track = [];   // recent pointer samples for throw velocity
    var pressTimer = null;

    canvas.addEventListener('pointerdown', function (e) {
        if (e.button !== undefined && e.button !== 0) return;
        e.preventDefault();
        try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
        dragging = true;
        moved = 0;
        offX = e.clientX - x;
        offY = e.clientY - y;
        track = [{ t: performance.now(), x: e.clientX, y: e.clientY }];
        setState('held');
        root.classList.add('is-held');
        closeMenu();
        if (e.pointerType && e.pointerType !== 'mouse') {   // long-press opens the menu on touch
            var px = e.clientX, py = e.clientY;
            pressTimer = setTimeout(function () {
                if (!dragging || moved >= 6) return;
                dragging = false;
                root.classList.remove('is-held');
                setState('idle', 3000);
                openMenu(px, py);
            }, 600);
        }
    });

    canvas.addEventListener('pointermove', function (e) {
        if (!dragging) return;
        var nx = clamp(e.clientX - offX, 0, maxX());
        var ny = clamp(e.clientY - offY, 0, groundY());
        moved += Math.abs(nx - x) + Math.abs(ny - y);
        x = nx;
        y = ny;
        var now = performance.now();
        track.push({ t: now, x: e.clientX, y: e.clientY });
        while (track.length > 2 && now - track[0].t > 100) track.shift();
    });

    function release(e) {
        clearTimeout(pressTimer);
        if (!dragging) return;
        dragging = false;
        root.classList.remove('is-held');
        try { canvas.releasePointerCapture(e.pointerId); } catch (err) {}
        if (moved < 6) {                       // a tap, not a drag: be happy
            say(['meow!', '♥', 'purr~', 'nya!'][Math.floor(Math.random() * 4)], 1600);
            setState('happy', 1600);
            vx = vy = 0;
            if (y < groundY() - 1) setState('fall');
            return;
        }
        var first = track[0], last = track[track.length - 1];
        var dt = Math.max(last.t - first.t, 16) / 1000;
        vx = clamp((last.x - first.x) / dt, -900, 900);
        vy = clamp((last.y - first.y) / dt, -900, 900);
        setState('fall');
    }
    canvas.addEventListener('pointerup', release);
    canvas.addEventListener('pointercancel', release);
    canvas.addEventListener('dragstart', function (e) { e.preventDefault(); });
    canvas.addEventListener('contextmenu', function (e) {
        e.preventDefault();
        if (state === 'held') return;
        openMenu(e.clientX, e.clientY);
    });

    // ── Right-click menu ─────────────────────────────────────────────────
    function busy() { return state === 'held' || state === 'fall'; }

    function act(next, duration, line) {
        if (busy()) return;
        if (line) say(line, 1400);
        setState(next, duration);
    }

    var ACTIONS = [
        {
            label: function () { return stayPut ? 'Stand up & roam' : 'Sit down'; },
            run: function () {
                if (stayPut) { stayPut = false; say('okay!', 1200); if (!busy()) pickNext(); }
                else { stayPut = true; act('idle', 4000, '*sits*'); }
            }
        },
        { label: function () { return 'Take a nap'; }, run: function () { stayPut = false; act('sleep', 12000); } },
        { label: function () { return 'Walk around'; }, run: function () { stayPut = false; dir = Math.random() < 0.5 ? -1 : 1; act('walk', 8000, 'off we go!'); } },
        { label: function () { return 'Pet the cat'; }, run: function () { act('happy', 2200, '♥'); } },
        { label: function () { return 'Meow!'; }, run: function () { say(['meow!', 'mew~', 'nya!', 'mrrp?'][Math.floor(Math.random() * 4)], 1500); } }
    ];

    function closeMenu() {
        if (!menu) return;
        menu.remove();
        menu = null;
        document.removeEventListener('pointerdown', onOutside, true);
        document.removeEventListener('keydown', onMenuKey, true);
        window.removeEventListener('resize', closeMenu);
        window.removeEventListener('blur', closeMenu);
        window.removeEventListener('scroll', closeMenu, true);
    }
    function onOutside(e) { if (menu && !menu.contains(e.target)) closeMenu(); }
    function onMenuKey(e) {
        if (!menu) return;
        if (e.key === 'Escape') { closeMenu(); return; }
        if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
        e.preventDefault();
        var btns = Array.prototype.slice.call(menu.querySelectorAll('button'));
        var i = btns.indexOf(document.activeElement);
        i = e.key === 'ArrowDown' ? (i + 1) % btns.length : (i - 1 + btns.length) % btns.length;
        btns[i].focus();
    }

    function menuButton(text, cls, handler) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'shimeji-menu-item' + (cls ? ' ' + cls : '');
        b.setAttribute('role', 'menuitem');
        b.textContent = text;
        b.addEventListener('click', function () { closeMenu(); handler(); });
        return b;
    }

    function setSkin(next) {
        skin = next;
        Object.assign(PALETTE, next.c);
        currentSprite = null;
        store('shimejiSkin', next.id);
        say('new look!', 1300);
    }

    function openMenu(px, py) {
        closeMenu();
        menu = document.createElement('div');
        menu.className = 'shimeji-menu';
        menu.setAttribute('role', 'menu');

        ACTIONS.forEach(function (a) { menu.appendChild(menuButton(a.label(), '', a.run)); });

        var row = document.createElement('div');
        row.className = 'shimeji-menu-skins';
        var lab = document.createElement('span');
        lab.className = 'shimeji-menu-label';
        lab.textContent = 'Design';
        row.appendChild(lab);
        SKINS.forEach(function (k) {
            var sw = document.createElement('button');
            sw.type = 'button';
            sw.className = 'shimeji-swatch' + (k.id === skin.id ? ' is-active' : '');
            sw.title = k.name;
            sw.setAttribute('role', 'menuitem');
            sw.setAttribute('aria-label', 'Design: ' + k.name);
            sw.style.background = k.c.b;
            sw.style.borderColor = k.c.k;
            sw.addEventListener('click', function () { closeMenu(); setSkin(k); });
            row.appendChild(sw);
        });
        menu.appendChild(row);

        menu.appendChild(menuButton('Hide cat', 'is-danger', hideCat));

        document.body.appendChild(menu);
        var w = menu.offsetWidth, h = menu.offsetHeight;
        menu.style.left = clamp(px, 4, window.innerWidth - w - 4) + 'px';
        menu.style.top = clamp(py, 4, window.innerHeight - h - 4) + 'px';
        menu.querySelector('button').focus({ preventScroll: true });

        setTimeout(function () {
            document.addEventListener('pointerdown', onOutside, true);
            document.addEventListener('keydown', onMenuKey, true);
            window.addEventListener('resize', closeMenu);
            window.addEventListener('blur', closeMenu);
            window.addEventListener('scroll', closeMenu, true);
        }, 0);
    }

    // ── Hide / bring back ────────────────────────────────────────────────
    var summon = null;

    function showSummon() {
        if (summon) return;
        summon = document.createElement('button');
        summon.type = 'button';
        summon.className = 'shimeji-summon';
        summon.title = 'Bring the cat back';
        summon.setAttribute('aria-label', 'Bring the cat back');
        summon.textContent = '🐾';
        summon.addEventListener('click', showCat);
        document.body.appendChild(summon);
    }

    function hideCat() {
        hidden = true;
        root.style.display = 'none';
        store('shimejiHidden', '1');
        showSummon();
    }

    function showCat() {
        hidden = false;
        store('shimejiHidden', null);
        if (summon) { summon.remove(); summon = null; }
        root.style.display = '';
        x = rand(SIZE, Math.max(SIZE + 1, window.innerWidth - SIZE * 2));
        y = -SIZE * 2;
        vx = vy = 0;
        stayPut = false;
        setState('fall');
        say('meow!', 1400);
    }

    // ── Main loop ────────────────────────────────────────────────────────
    var last = performance.now();
    var WALK_SPEED = 44;
    var GRAVITY = 1900;

    function frame(now) {
        var dt = Math.min((now - last) / 1000, 0.05);
        last = now;
        if (hidden) { requestAnimationFrame(frame); return; }
        stateTime += dt * 1000;
        var t = now / 1000;
        var sprite;
        var bob = 0;

        if (bubbleTimer > 0) {
            bubbleTimer -= dt * 1000;
            if (bubbleTimer <= 0) bubble.classList.remove('show');
        }

        if (state === 'fall') {
            vy += GRAVITY * dt;
            x += vx * dt;
            y += vy * dt;
            if (x < 0) { x = 0; vx = Math.abs(vx) * 0.5; }
            if (x > maxX()) { x = maxX(); vx = -Math.abs(vx) * 0.5; }
            if (y < 0) { y = 0; vy = Math.abs(vy) * 0.4; }
            if (y >= groundY()) {
                y = groundY();
                if (vy > 420) {                      // bounce once on a hard landing
                    vy = -vy * 0.28;
                    vx *= 0.6;
                    squash = 1;
                } else {
                    vy = 0;
                    vx = 0;
                    squash = 1;
                    setState('idle', rand(1200, 2500));
                }
            }
            sprite = 'held';
        } else if (state === 'held') {
            sprite = 'held';
            // dangle: gentle sway while carried
            bob = Math.sin(t * 9) * 1.5;
        } else if (state === 'walk') {
            if (!menu) x += dir * WALK_SPEED * dt;
            if (x <= 0) { x = 0; dir = 1; }
            if (x >= maxX()) { x = maxX(); dir = -1; }
            var f = Math.floor(t * 6) % 4;
            sprite = 'walk' + f;
            bob = (f % 2) ? -PX / 2 : 0;
            if (stateTime > stateDuration) pickNext();
        } else if (state === 'sleep') {
            sprite = (Math.floor(t * 1.2) % 2) ? 'sleepB' : 'sleep';
            if (Math.floor(stateTime / 2200) !== Math.floor((stateTime - dt * 1000) / 2200)) say('z z z', 1800);
            if (stateTime > stateDuration) { say('*yawn*', 1400); setState('idle', 1600); }
        } else if (state === 'happy') {
            sprite = (Math.floor(t * 4) % 2) ? 'happyB' : 'happy';
            bob = -Math.abs(Math.sin(t * 8)) * 3;
            if (stateTime > stateDuration) setState('idle', rand(1000, 2000));
        } else {                                       // idle
            var phase = t % 4.2;
            if (phase > 3.95) sprite = 'blink';
            else sprite = (Math.floor(t * 1.4) % 2) ? 'idleB' : 'idleA';
            if (stateTime > stateDuration) pickNext();
        }

        draw(sprite);

        // landing squash eases back to normal
        if (squash > 0) squash = Math.max(0, squash - dt * 5);
        var sy = 1 - squash * 0.22, sx = 1 + squash * 0.14;
        var flip = state === 'walk' ? dir : (state === 'fall' && vx < 0 ? -1 : 1);
        canvas.style.transform = 'translateY(' + bob + 'px) scale(' + (flip * sx) + ',' + sy + ')';

        root.style.transform = 'translate3d(' + Math.round(x) + 'px,' + Math.round(y) + 'px,0)';

        // shadow stays on the ground and fades/shrinks as the cat rises
        var height = clamp((groundY() - y) / 240, 0, 1);
        shadow.style.transform = 'translateY(' + Math.round(groundY() - y) + 'px) scaleX(' + (1 - height * 0.5) + ')';
        shadow.style.opacity = String(0.28 - height * 0.18);

        requestAnimationFrame(frame);
    }

    window.addEventListener('resize', function () {
        x = clamp(x, 0, maxX());
        if (state !== 'held' && state !== 'fall' && y > groundY()) y = groundY();
        if (y < groundY() && state !== 'held' && state !== 'fall') setState('fall');
    });

    // Drop in from the top of the page on load.
    x = rand(SIZE, Math.max(SIZE + 1, window.innerWidth - SIZE * 2));
    y = -SIZE * 2;
    vy = 0;
    // Small public API (used by the About page's pet.exe window).
    window.shimeji = {
        sprites: { N: 16, palette: PALETTE, frames: SPRITES },
        pet: function () { if (hidden) showCat(); else act('happy', 2200, '\u2665'); },
        hop: function () { if (hidden) showCat(); else { stayPut = false; dir = Math.random() < 0.5 ? -1 : 1; act('walk', 6000, 'off we go!'); } },
        say: function (text) { if (!hidden) say(text, 1600); }
    };

    if (hidden) { root.style.display = 'none'; showSummon(); }
    requestAnimationFrame(function (n) { last = n; frame(n); });
})();
