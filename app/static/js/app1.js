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
        `localhost:8000/journal_note_api?w=${w}&wid=${wid}`,{"method":"GET"}
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



function copy_link(e) {
    navigator.clipboard.writeText(e).then(
    alert("Copied the Link"));
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

