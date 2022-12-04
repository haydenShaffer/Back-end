function deleteNote(noteId){
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({noteId: noteId}),
    }).then((_res) => {
        window.location.href="/"
    });
}

function deleteComments(commentsId){
    fetch('/delete-comments', {
        method: 'POST',
        body: JSON.stringify({commentsId: commentsId}),
    }).then((_res) => {
        window.location.href="/"
    });
}