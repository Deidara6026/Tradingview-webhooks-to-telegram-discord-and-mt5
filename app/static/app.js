function post_note(id, rid, wid) {
    note_element = document.getElementById("note-msg-id");
    rating_element = document.getElementById("note-rating-id");
    webhook_element = document.getElementById("note-webhook-id");
    fetch(
        "localhost:8000/journal_note_api" + webhook_element, {
            "method": "POST",
            "body": JSON.stringify({
                "note": note_element.textContent.trim()
            })
        }
    )
}