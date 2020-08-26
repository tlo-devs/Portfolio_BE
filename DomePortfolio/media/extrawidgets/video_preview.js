function youtube_parser(url) {
    const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    const match = url.match(regExp);
    return (match&&match[7].length===11)? match[7] : false;
}

function embed_url(id) {
    return "https://www.youtube.com/embed/" + id.toString();
}
