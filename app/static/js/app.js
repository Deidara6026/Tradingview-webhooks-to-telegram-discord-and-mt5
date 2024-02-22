import { Modal } from './bundle.js'

function post_note(wid) {
    note_element = document.getElementById("note-msg-id");
    rating_element = document.getElementById("note-rating-id");
    webhook_element = document.getElementById("note-webhook-id");
    fetch(
        "localhost:8000/journal_note_api" + webhook_element, {
            "method": "POST",
            "body": JSON.stringify({
                "note": note_element.textContent.trim(),
                "rating": rating_element.textContent.trim(),
                "pk": wid
            })
        }
    )
}

function get_note(wid, w) {
    fetch(
        "localhost:8000/journal_note_api?w=w&wid=wid",{"method":"GET"}
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

function copy_link(e) {
    navigator.clipboard.writeText(e).then(
    alert("Copied the Link"));
}

function toggle_note(pk) {
    console.log("kk")
    id = document.getElementById("note-webhook-id");
    id.setAttribute('value', pk);
    var myModal = new Modal(document.getElementById('note-create'), options);
    myModal.show();

}