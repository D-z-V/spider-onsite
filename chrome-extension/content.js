window.onload = () => {
    chrome.runtime.onMessage.addListener((request, sender, resp) => {
        console.log(request.bg, request.fs)
        var elm = document.body.getElementsByTagName("*")
        console.log(elm)
        for (var i = 0; i < elm.length; i++) {
            elm[i].style.backgroundColor = request.bg;
            elm[i].style.fontSize = request.fs + "px";
        }
    });
}