function post_note() {
    note_element = document.getElementById("note-text");
    rating_element = document.getElementById("note-rating");
    oid = document.getElementById("note-webhook-id");
    wid = document.getElementById("note-webhook-wid");
    fetch(
        "localhost:8000/journal_note_api" + wid, {
            "method": "POST",
            "body": JSON.stringify({
                "note": note_element.textContent.trim(),
                "rating": rating_element.textContent.trim(),
                "pk": oid
            })
        }
    )
}

function get_notes(wid, w) {
    fetch(
        `http://localhost:8000/journal_note_api?w=${w}&wid=${wid}`,{"method":"GET"}
    ).then((res) => res.json()
    ).then((data) => {
        message = data.message;
        const linkSource = `data:application/pdf;base64,${message}`;
        const downloadLink = document.createElement("a");
        const fileName = "Compiled Orders.pdf";
        downloadLink.href = linkSource;
        downloadLink.download = fileName;
        downloadLink.click();
    })
    
}

function get_note(wid, w) {
    fetch(
        `localhost:8000/journal_note_api?w=${w}&wid=${wid}`,{"method":"GET"}
    ).then((res) => res.json()
    ).then((data) => {
        message = data.message;
        note_element = document.getElementById("note-text");
        rating_element = document.getElementById("note-rating");
        note_element.innerText = message.note;
        rating_element.innerText = message.rating;
    })
}


function copy(event) {
    navigator.clipboard.writeText(document.getElementById('link').innerText).then(function() {
    // Create and show toast notification
    showToast("Copied to clipboard!");
}, function(err) {
    console.error('Could not copy text: ', err);
    showToast("Failed to copy text.");
});
}
   
function add_data(wid, w, n) {
    document.getElementById("editmodalwid").innerText = wid;
    document.getElementById("editmodalw").innerText = w;
    if (w == "discord") {
        document.getElementById("cid").innerText = "Chat Webhook Url";
    }
    document.getElementById("editmodalw").data = n;
}

function add_chat_id() {
    b = document.getElementById("editmodalw");
    var maxChats = b.data; // Change this to the maximum number of chats allowed
    var numChats = document.querySelectorAll('#editmodal input[type="text"]:not([hidden])').length;
    if (numChats >= maxChats) {
        showToast("Exceeded max number of chats, upgrade to add more");
        return;
    }
    var newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.className = 'form-control mb-1';
    newInput.name = 'chatid';
    newInput.required = true;
    document.querySelector('#editmodal form').insertBefore(newInput, document.querySelector('#editmodal .float-end'));
 }

function showToast(message) {
const toastContainer = document.createElement('div');
toastContainer.classList.add('toast-container', 'position-fixed', 'bottom-0', 'end-0', 'p-3');

const toastHTML = `
    <div class="toast" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="toast-header">
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">${message}</div>
    </div>
`;

toastContainer.innerHTML = toastHTML;
document.body.appendChild(toastContainer);

const toastElement = toastContainer.querySelector('.toast');
const toast = new bootstrap.Toast(toastElement, {
    autohide: true,
    delay: 2000
});

toast.show();

// Remove the toast from DOM after it's hidden
toastElement.addEventListener('hidden.bs.toast', () => {
    document.body.removeChild(toastContainer);
});
}
function toggle_note(pk, wid) {
    console.log("kk")
    id = document.getElementById("note-webhook-id");
    wid = document.getElementById("note-webhook-wid");
    id.setAttribute('value', pk);
    wid.setAttribute('value', wid);
    get_note(wid, pk)
    // var myModal = new Modal(document.getElementById('note-create'), options);
    // myModal.show();

}

