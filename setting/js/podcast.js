class Podcast {
    episode_display(dv) {
        const current = dv.current();
        if (!current.url) {
            return;
        }
        const el_id = "dv-podcast";
        dv.el("iframe", "podcast", {
            attr: {
                id: el_id,
                width: "100%",
                height: "1000",
                scrolling: "yes",
                src: current.url,
                frameborders: "0",
            },
        });

        // setTimeout(this.scroll, 1000, el_id);
    }

    scroll(el_id) {
        console.log(el_id)
        // let frameWidow = document.getElementById(el_id).contentWindow;
        // console.log(frameWidow)
        // // frameWidow.document.scrollingElement.scrollTop = 100
        // frameWidow.scrollTo(0, 100)

        // var iframe = document.getElementById(el_id);

        // // 获取iframe的内容窗口对象
        // var iframeWindow = iframe.contentWindow || iframe.contentDocument.defaultView;

        // // 获取iframe的文档对象
        // var iframeDocument = iframeWindow.document;

        // // 滚动到指定位置，这里向下滚动100像素
        // iframeWindow.scrollBy(0, 100);

        // 在父页面（或发送消息的页面）：
        var iframe = document.getElementById(el_id);

        // 在子页面（或接收消息的页面）：
        window.addEventListener('message', function (event) {
            console.log(event)
            if (event.origin !== 'http://example.com') {
                // 确保消息来自预期的源
                return;
            }
            console.log('Message received:', event.data);
        }, false);
        iframe.contentWindow.postMessage('Hello from parent', 'http://example.com'); // 假设目标源是 http://example.com


    }
}