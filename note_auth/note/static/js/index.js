
// the function allows us to delete a note by receiving a noteId from X button
function deleteNote(noteId){
    // it fetchs first to /delete-note with a POST method and a noteId to submit that route
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})
    }).then((_res) => {  // after the response must redirect us to '/'
        window.location.href = '/';
    });
}