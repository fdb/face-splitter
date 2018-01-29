const FACE_INDEX_MIN = 1;
const FACE_INDEX_MAX = 121;

function choice(l) {
    return l[Math.floor(Math.random() * l.length)];
}

function rand_int(min, max) {
    return Math.round(min + Math.random() * (max - min));
}

function pad_zeroes(i, length=4) {
    s = '' + i;
    while (s.length < length) {
        s = '0' + s;
    }
    return s;
}

function make_image(url) {
    const img = document.createElement('img');
    img.src = url;
    document.getElementById('face-wrap').appendChild(img);
}

function make_face() {
    document.getElementById('face-wrap').innerHTML = '';
    const top_id = rand_int(FACE_INDEX_MIN, FACE_INDEX_MAX);
    const mid_id = rand_int(FACE_INDEX_MIN, FACE_INDEX_MAX);
    const bot_id = rand_int(FACE_INDEX_MIN, FACE_INDEX_MAX);

    const top_url = `resized/face_${top_id}_t.jpg`;
    const mid_url = `resized/face_${mid_id}_m.jpg`;
    const bot_url = `resized/face_${bot_id}_b.jpg`;

    make_image(top_url);
    make_image(mid_url);
    make_image(bot_url);
}


document.getElementById('face-wrap').addEventListener('click', make_face);
