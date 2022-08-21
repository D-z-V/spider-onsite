var btn = document.getElementsByTagName('button')[0];
btn.addEventListener('click', function(e) {
    var bg = document.getElementById('bg').value;
    var fs = document.getElementById('fs').value;
    console.log(fs, bg)
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {
            bg: bg,
            fs: fs
        });
    });
});