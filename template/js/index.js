var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function () {
    $messages.mCustomScrollbar();
    setTimeout(function () {
        sendInitialMessage();
    }, 100);
});

function updateScrollbar() {
    $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
        scrollInertia: 10,
        timeout: 0
    });
}

function setDate() {
    d = new Date()
    if (m != d.getMinutes()) {
        m = d.getMinutes();
        $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
    }
}

function insertMessage() {
    msg = $('.message-input').val();
    if ($.trim(msg) == '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    $('.message-input').val(null);
    updateScrollbar();
    setTimeout(function () {
        fakeMessage(msg);
    }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function () {
    insertMessage();
});

$(window).on('keydown', function (e) {
    if (e.which == 13) {
        e.preventDefault();
        insertMessage();
        return false;
    }
});

var first_msg = [
    'Hi there!',
    'How can I help you?',
    'Hello!',
];

async function getResponse(query) {
    const response = await fetch("http://127.0.0.1:8000/search/query", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query }),
    });
    if (!response.ok) {
        const message = `An error has occurred: ${response.status}`;
        throw new Error(message);
    }

    const data = await response.json();
    return data.response;
}

function sendInitialMessage() {
    const initialMessage = first_msg[Math.floor(Math.random() * first_msg.length)];
    $('<div class="message new"><figure class="avatar"><img src="img/TS_Icon256.png" /></figure>' + initialMessage + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
}

async function fakeMessage(userMessage) {
    if ($('.message-input').val() != '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="img/TS_Icon256.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
    updateScrollbar();

    try {
        const response = await getResponse(userMessage);
        setTimeout(function () {
            $('.message.loading').remove();
            $('<div class="message new"><figure class="avatar"><img src="img/TS_Icon256.png" /></figure>' + response + '</div>').appendTo($('.mCSB_container')).addClass('new');
            setDate();
            updateScrollbar();
        }, 1000 + (Math.random() * 20) * 100);
    } catch (error) {
        console.error('Error:', error);
    }
}
