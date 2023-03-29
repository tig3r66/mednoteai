const msgerForm = get(".msger-inputarea");
const msgerInput = get(".msger-input");
const msgerChat = get(".msger-chat");

// Icons made by Freepik from www.flaticon.com
const BOT_IMG = "/static/images/neurogpt-x-logo.png";
const PERSON_IMG = "/static/images/person-img.png";
const BOT_NAME = "    MedNoteAI";
const PERSON_NAME = "Me";


document.addEventListener("DOMContentLoaded", function() {
    msgerInput.addEventListener("keydown", event => {
        if (event.keyCode === 13 && !event.shiftKey) {
            event.preventDefault();
            msgerForm.dispatchEvent(new Event("submit"));
        }
    });

    msgerForm.addEventListener("submit", event => {
        event.preventDefault();

        if (formSubmitted) return;
        formSubmitted = true;

        const msgText = msgerInput.value;
        if (!msgText) return;

        appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
        msgerInput.value = "";

        botResponse(msgText);
    });

    $.get("/get").done(function (data) {
        formSubmitted = false;

        const msgText = data;
        appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
    });
});


function botResponse(rawText) {
    // Add dots message
    const words = ["elastic", "collision", "bricks", "falling", "stretching"];
    const randomWord = words[Math.floor(Math.random() * words.length)];
    const dots = String.raw`<div class="stage"><div class="dot-${randomWord}"></div></div>`;

    appendMessage(BOT_NAME, BOT_IMG, "left", dots);

    $.get("/get", { msg: rawText }).done(function (data) {
        console.log(rawText);
        console.log(data);
        const msgText = data;

        // Clear dots message
        const dotsMessage = document.querySelector(".left-msg:last-child");
        dotsMessage.innerHTML = "";

        // Add response message
        appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
        formSubmitted = false;
    });
}


function appendMessage(name, img, side, text) {
    // Simple solution for small apps
    if (!text) return;
    const msgHTML = `
<div class="msg ${side}-msg">
    <div class="msg-img" style="background-image: url(${img})"></div>

    <div class="msg-bubble">
    <div class="msg-info">
        <div class="msg-info-name">${name}</div>
        <div class="msg-info-time">${formatDate(new Date())}</div>
    </div>

    <div class="msg-text" id="#response">${text}</div>
    </div>
</div>
`;

    msgerChat.insertAdjacentHTML("beforeend", msgHTML);
    msgerChat.scrollTop += 500;
}


// Utils
function get(selector, root = document) {
    return root.querySelector(selector);
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();

    return `${h.slice(-2)}:${m.slice(-2)}`;
}


const fileInput = document.getElementById('file');
const fileLabel = document.getElementById('file-label');
const form = document.querySelector('form');

fileInput.addEventListener('change', (event) => {
    const fname = event.target.files[0].name;
    fileLabel.innerHTML = 'Uploading...';

    const form = document.querySelector('form');
    const formData = new FormData(form);
    fetch('/upload', {
        method: 'POST',
        body: formData
        })
    .then(response => {
        if (response.ok) {
            appendMessage(PERSON_NAME, PERSON_IMG, "right", `<a href="static/upload/${fname}" target="_blank">${fname}</a> uploaded successfully.`);
            appendMessage(BOT_NAME, BOT_IMG, "left", "To create notes from your upload, please type !process. If this is a research paper, type !paper. Note that this may take a few minutes.");
            fileLabel.innerText = 'Upload file';
        } else {
            appendMessage(BOT_NAME, BOT_IMG, "left", "File upload failed. Please upload a valid mp4 OR PDF file.");
        }
    })
    .catch(error => console.error(error));
});
