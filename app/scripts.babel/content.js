var j = document.createElement('script');
j.src = chrome.extension.getURL('node_modules/jquery/dist/jquery.min.js');
(document.head || document.documentElement).appendChild(j);

var g = document.createElement('script');
g.src = chrome.extension.getURL('node_modules/gmail-js/src/gmail.js');
(document.head || document.documentElement).appendChild(g);

/*var s = document.createElement('script');
s.src = chrome.extension.getURL('main.js');
(document.head || document.documentElement).appendChild(s);
*/
